"""RAG-based knowledge base for indexing and retrieving research papers."""

from __future__ import annotations

import json
import hashlib
from pathlib import Path
from typing import Any, Optional

import chromadb
from chromadb.config import Settings


class KnowledgeBase:
    """Local-first vector store for research papers using ChromaDB.

    Stores paper chunks with embeddings for semantic search.
    Falls back to simple in-memory search if ChromaDB is unavailable.
    """

    def __init__(self, project_dir: Path, collection_name: str = "research_papers"):
        self.project_dir = Path(project_dir)
        self.project_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.project_dir / ".knowledge"
        self.collection_name = collection_name

        try:
            self.client = chromadb.PersistentClient(
                path=str(self.db_path),
                settings=Settings(anonymized_telemetry=False),
            )
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"},
            )
            self._use_vector = True
        except Exception:
            # Fallback: simple keyword-based search
            self._use_vector = False
            self._fallback_store: list[dict[str, Any]] = []
            self._load_fallback()

    def _load_fallback(self) -> None:
        """Load fallback store from disk."""
        store_file = self.project_dir / ".knowledge_fallback.json"
        if store_file.exists():
            self._fallback_store = json.loads(store_file.read_text(encoding="utf-8"))

    def _save_fallback(self) -> None:
        """Save fallback store to disk."""
        store_file = self.project_dir / ".knowledge_fallback.json"
        store_file.write_text(
            json.dumps(self._fallback_store, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
        """Split text into overlapping chunks for indexing."""
        if not text:
            return []
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start = end - overlap
        return chunks

    def _make_id(self, paper_title: str, chunk_idx: int = 0) -> str:
        """Generate a deterministic ID for a paper chunk."""
        raw = f"{paper_title}::{chunk_idx}"
        return hashlib.md5(raw.encode()).hexdigest()[:16]

    def index_paper(self, title: str, abstract: str = "", full_text: str = "",
                    authors: Optional[list[str]] = None, year: Optional[int] = None,
                    doi: str = "", url: str = "", source: str = "") -> int:
        """Index a paper for semantic search.

        Returns the number of chunks indexed.
        """
        # Combine abstract and full text for indexing
        content = f"{title}\n\n{abstract}"
        if full_text:
            content += f"\n\n{full_text}"

        chunks = self._chunk_text(content)
        if not chunks:
            return 0

        metadata_base = {
            "title": str(title),
            "authors": json.dumps(authors or []),
            "year": int(year) if year else 0,
            "doi": str(doi or ""),
            "url": str(url or ""),
            "source": str(source or ""),
        }

        if self._use_vector:
            self.collection.add(
                documents=chunks,
                ids=[self._make_id(title, i) for i in range(len(chunks))],
                metadatas=[{**metadata_base, "chunk_idx": i} for i in range(len(chunks))],
            )
        else:
            for i, chunk in enumerate(chunks):
                self._fallback_store.append({
                    "id": self._make_id(title, i),
                    "document": chunk,
                    "metadata": {**metadata_base, "chunk_idx": i},
                })
            self._save_fallback()

        return len(chunks)

    def search(self, query: str, k: int = 10) -> list[dict[str, Any]]:
        """Semantic search across indexed papers.

        Returns a list of results with document text, metadata, and distance.
        """
        if self._use_vector:
            results = self.collection.query(
                query_texts=[query],
                n_results=min(k, self.collection.count() or 1),
            )
            output = []
            if results and results["documents"]:
                for doc, meta, dist in zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0],
                ):
                    output.append({
                        "text": doc,
                        "metadata": meta,
                        "distance": dist,
                    })
            return output
        else:
            # Fallback: simple keyword matching
            query_lower = query.lower()
            scored = []
            for item in self._fallback_store:
                doc_lower = item["document"].lower()
                # Simple score: count keyword occurrences
                score = sum(1 for word in query_lower.split() if word in doc_lower)
                if score > 0:
                    scored.append({**item, "score": score})
            scored.sort(key=lambda x: x["score"], reverse=True)
            return scored[:k]

    def get_paper_count(self) -> int:
        """Return the number of indexed papers."""
        if self._use_vector:
            return self.collection.count()
        return len(self._fallback_store)

    def get_unique_papers(self) -> list[dict[str, Any]]:
        """Return metadata for all unique indexed papers."""
        if self._use_vector:
            all_data = self.collection.get()
            seen = set()
            papers = []
            for meta in all_data.get("metadatas", []):
                title = meta.get("title", "")
                if title and title not in seen:
                    seen.add(title)
                    papers.append({
                        "title": title,
                        "authors": json.loads(meta.get("authors", "[]")),
                        "year": meta.get("year"),
                        "doi": meta.get("doi", ""),
                        "source": meta.get("source", ""),
                    })
            return papers
        else:
            seen = set()
            papers = []
            for item in self._fallback_store:
                title = item["metadata"].get("title", "")
                if title and title not in seen:
                    seen.add(title)
                    papers.append({
                        "title": title,
                        "authors": json.loads(item["metadata"].get("authors", "[]")),
                        "year": item["metadata"].get("year"),
                        "doi": item["metadata"].get("doi", ""),
                        "source": item["metadata"].get("source", ""),
                    })
            return papers

    def clear(self) -> None:
        """Clear all indexed data."""
        if self._use_vector:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"},
            )
        else:
            self._fallback_store = []
            self._save_fallback()
