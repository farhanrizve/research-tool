FROM python:3.12-slim AS base

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    texlive-latex-base \
    texlive-latex-extra \
    latexmk \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY pyproject.toml README.md ./
COPY src/ src/
RUN pip install --no-cache-dir ".[all]"

# Web UI
COPY web/ web/

EXPOSE 8000

CMD ["uvicorn", "research_tool.api.app:create_app", "--host", "0.0.0.0", "--port", "8000", "--factory"]
