"""
Generate database schema diagrams from SQL DDL or JSON schema definitions.

Produces publication-quality diagrams using Graphviz.
Supports:
- SQL CREATE TABLE statements → ER diagram
- JSON schema definition files → ER diagram
- CSV column definitions → simple table diagram

Outputs black-and-white or color diagrams suitable for thesis/report inclusion.

Usage:
    python scripts/generate_schema_diagram.py --input schema.sql --output diagram.png
    python scripts/generate_schema_diagram.py --input schema.json --output diagram.png --color
    python scripts/generate_schema_diagram.py --csv mydata.csv --output table_diagram.png
"""

import argparse
import json
import os
import re
import sys

try:
    import graphviz
except ImportError:
    print("Graphviz not installed. Install with: pip install graphviz")
    print("Also need Graphviz system package: https://graphviz.org/download/")
    sys.exit(1)

# ── Default styling ──────────────────────────────────────────────────────────

BW_ATTRS = dict(
    engine="dot",
    graph_attr={
        "rankdir": "TB",
        "fontname": "Arial",
        "fontsize": "12",
        "bgcolor": "white",
        "pad": "0.3",
        "nodesep": "0.5",
        "ranksep": "0.8",
        "splines": "spline",
        "dpi": "150",
    },
    node_attr={
        "shape": "none",
        "fontname": "Arial",
        "fontsize": "11",
    },
    edge_attr={
        "fontname": "Arial",
        "fontsize": "9",
        "color": "#000000",
        "arrowsize": "0.7",
    },
)

COLOR_ATTRS = dict(
    engine="dot",
    graph_attr={
        "rankdir": "TB",
        "fontname": "Arial",
        "fontsize": "12",
        "bgcolor": "white",
        "pad": "0.3",
        "nodesep": "0.5",
        "ranksep": "0.8",
        "splines": "spline",
        "dpi": "150",
    },
    node_attr={
        "shape": "none",
        "fontname": "Arial",
        "fontsize": "11",
    },
    edge_attr={
        "fontname": "Arial",
        "fontsize": "9",
        "color": "#555555",
        "arrowsize": "0.7",
    },
)

TABLE_COLORS = {
    "header_bg": "#2c3e50",
    "header_fg": "white",
    "alt_row_1": "#f8f9fa",
    "alt_row_2": "#ffffff",
    "fk_text": "#7f8c8d",
    "key_text": "#e74c3c",
}


def create_table_node(graph, table_name: str, columns: list, color: bool = False):
    """
    Create an HTML-label table node in the graph.

    columns: list of (col_name, col_type, role)
    where role is 'PK', 'FK', 'PK,FK', or ''
    """
    rows = []
    colors = TABLE_COLORS

    if color:
        header_bg = "#3498db"
    else:
        header_bg = "#000000"

    # Header row
    rows.append(
        f'<TR><TD COLSPAN="2" BGCOLOR="{header_bg}" ALIGN="CENTER">'
        f'<FONT COLOR="white" POINT-SIZE="11"><B>{table_name}</B></FONT>'
        f"</TD></TR>"
    )

    for i, (col, dtype, role) in enumerate(columns):
        bg = colors["alt_row_1"] if i % 2 == 0 else colors["alt_row_2"]

        # Build prefix/suffix markers
        prefix = ""
        suffix = ""
        if "PK" in role or "FK" in role:
            markers = []
            if "PK" in role:
                markers.append("PK")
            if "FK" in role:
                markers.append("FK")
            prefix = f'<FONT POINT-SIZE="9" COLOR="{colors["key_text"]}">{" ".join(markers)} </FONT>'
            suffix = ""  # Will be wrapped inside bold if PK

        # Bold primary keys
        if "PK" in role:
            col_display = f"<B>{prefix}{col}{suffix}</B>"
        else:
            col_display = f"{prefix}{col}{suffix}"

        dtype_display = (
            f'<FONT POINT-SIZE="9" COLOR="{colors["fk_text"]}">{dtype}</FONT>'
        )

        rows.append(
            f"<TR>"
            f'<TD BGCOLOR="{bg}" ALIGN="LEFT" BORDER="0" WIDTH="160">'
            f"{col_display}</TD>"
            f'<TD BGCOLOR="{bg}" ALIGN="LEFT" BORDER="0" WIDTH="120">'
            f"{dtype_display}</TD>"
            f"</TR>"
        )

    label = (
        '<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4">'
        + "".join(rows)
        + "</TABLE>>"
    )
    graph.node(table_name, label=label)


def add_foreign_key(graph, src: str, dst: str, label: str = "1:N"):
    """Add a foreign key edge between two tables."""
    graph.edge(src, dst, label=f" {label} ", arrowhead="crow", arrowtail="odot",
               dir="both", penwidth="1.5", arrowsize="1.0",
               constraint="false", weight="10")


def parse_sql_ddl(sql_path: str) -> dict:
    """Parse SQL CREATE TABLE statements into table definitions."""
    with open(sql_path, "r", encoding="utf-8") as f:
        content = f.read()

    tables = {}
    # Extract CREATE TABLE blocks
    pattern = re.compile(
        r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(?:`?(\w+)`?\.)?`?(\w+)`?\s*\((.*?)\)\s*(?:ENGINE|;)",
        re.DOTALL | re.IGNORECASE,
    )

    for match in pattern.finditer(content):
        schema = match.group(1) or ""
        table = match.group(2)
        body = match.group(3)

        columns = []
        fk_refs = []

        for line in body.split("\n"):
            line = line.strip()
            if not line or line.startswith("--") or line.startswith("#"):
                continue
            if line.startswith("KEY") or line.startswith("INDEX") or line.startswith("UNIQUE"):
                continue
            if line.startswith("PRIMARY KEY"):
                match_pk = re.search(r"\(`?(\w+)`?\)", line)
                if match_pk:
                    pk_col = match_pk.group(1)
                    for i, (c, t, r) in enumerate(columns):
                        if c == pk_col:
                            columns[i] = (c, t, "PK")
                continue
            if line.startswith("FOREIGN KEY"):
                match_fk = re.search(r"FOREIGN\s+KEY\s*\(`?(\w+)`?\)\s*REFERENCES\s+`?(\w+)`?\s*\(`?(\w+)`?\)", line, re.IGNORECASE)
                if match_fk:
                    fk_col = match_fk.group(1)
                    ref_table = match_fk.group(2)
                    ref_col = match_fk.group(3)
                    fk_refs.append((fk_col, ref_table, ref_col))
                    for i, (c, t, r) in enumerate(columns):
                        if c == fk_col:
                            new_role = "FK" if not r else f"{r},FK"
                            columns[i] = (c, t, new_role)
                continue

            # Parse column definition
            col_match = re.match(r"`?(\w+)`?\s+(\w+(?:\s*\([^)]*\))?)", line)
            if col_match:
                col_name = col_match.group(1)
                col_type = col_match.group(2)
                role = ""
                if "PRIMARY" in line.upper() or "AUTO_INCREMENT" in line.upper():
                    role = "PK"
                columns.append((col_name, col_type, role))

        table_name = f"{schema}_{table}" if schema else table
        tables[table_name] = {"columns": columns, "fk_refs": fk_refs}

    return tables


def parse_json_schema(json_path: str) -> dict:
    """Parse a JSON schema definition into table definitions.

    Expected format:
    {
      "tables": [
        {
          "name": "table_name",
          "columns": [
            {"name": "id", "type": "INTEGER", "role": "PK"},
            {"name": "name", "type": "VARCHAR(100)", "role": ""}
          ],
          "foreign_keys": [
            {"column": "fk_col", "references": "other_table", "ref_column": "id"}
          ]
        }
      ]
    }
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    tables = {}
    for table_def in data.get("tables", []):
        name = table_def["name"]
        columns = [(c["name"], c["type"], c.get("role", "")) for c in table_def.get("columns", [])]
        fk_refs = [(fk["column"], fk["references"], fk.get("ref_column", "id"))
                    for fk in table_def.get("foreign_keys", [])]
        tables[name] = {"columns": columns, "fk_refs": fk_refs}

    return tables


def parse_csv_header(csv_path: str) -> dict:
    """Create a simple table diagram from a CSV file (columns only)."""
    import csv

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

    table_name = os.path.splitext(os.path.basename(csv_path))[0]
    columns = [(h, "text", "") for h in header]

    return {table_name: {"columns": columns, "fk_refs": []}}


def generate_diagram(
    tables: dict,
    output_path: str,
    color: bool = False,
    title: str = "",
) -> str:
    """Generate a Graphviz diagram from parsed table definitions."""
    attrs = COLOR_ATTRS if color else BW_ATTRS
    dot = graphviz.Digraph(**attrs)

    # Add title if specified
    if title:
        dot.attr(label=title, labelloc="t", fontsize="16")

    # Create table nodes
    for table_name, table_def in tables.items():
        create_table_node(dot, table_name, table_def["columns"], color)

    # Add foreign key edges
    for table_name, table_def in tables.items():
        for fk_col, ref_table, ref_col in table_def.get("fk_refs", []):
            if ref_table in tables:
                add_foreign_key(dot, table_name, ref_table)

    # Render
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    dot.render(output_path, format="png", cleanup=True)
    return output_path + ".png"


def main():
    parser = argparse.ArgumentParser(
        description="Generate database schema diagrams for publications"
    )
    parser.add_argument(
        "-i", "--input", required=True,
        help="Input file (.sql, .json, or .csv)"
    )
    parser.add_argument(
        "-o", "--output", default="schema_diagram",
        help="Output path (without extension, default: schema_diagram)"
    )
    parser.add_argument(
        "--color", action="store_true",
        help="Generate color diagram instead of black-and-white"
    )
    parser.add_argument(
        "--title", default="",
        help="Optional diagram title"
    )
    parser.add_argument(
        "--target-width", type=int, default=1877,
        help="Target width in pixels (default: 1877 = 159mm at 300 DPI)"
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: File not found: {args.input}")
        sys.exit(1)

    ext = os.path.splitext(args.input)[1].lower()
    try:
        if ext == ".sql":
            tables = parse_sql_ddl(args.input)
        elif ext == ".json":
            tables = parse_json_schema(args.input)
        elif ext == ".csv":
            tables = parse_csv_header(args.input)
        else:
            print(f"Unsupported file type: {ext}. Use .sql, .json, or .csv")
            sys.exit(1)
    except Exception as e:
        print(f"Error parsing input: {e}")
        sys.exit(1)

    if not tables:
        print("No tables found in input.")
        sys.exit(1)

    print(f"Found {len(tables)} table(s):")
    for name, defn in tables.items():
        print(f"  {name}: {len(defn['columns'])} columns, {len(defn.get('fk_refs', []))} FK(s)")

    try:
        output = generate_diagram(tables, args.output, args.color, args.title)
        print(f"\nDiagram saved to: {output}")
    except Exception as e:
        print(f"Error generating diagram: {e}")
        print("Make sure Graphviz is installed system-wide: https://graphviz.org/download/")
        sys.exit(1)


if __name__ == "__main__":
    main()
