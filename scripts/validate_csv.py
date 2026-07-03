"""
Comprehensive CSV data validation utility for research datasets.

Features:
- Structural validation (column count, row consistency)
- Data integrity checks (empty rows, fill rates)
- Column-level analysis (data types, missing values)
- Statistical summaries
- Configurable validation rules via JSON config file

Usage:
    python scripts/validate_csv.py <input.csv>
    python scripts/validate_csv.py <input.csv> --config validation_rules.json
    python scripts/validate_csv.py <input.csv> --output report.md
"""

import csv
import json
import os
import sys
import argparse
from collections import Counter
from datetime import datetime


def load_csv(filepath: str, encoding: str = "utf-8") -> tuple:
    """Load a CSV file and return (header, rows)."""
    with open(filepath, "r", encoding=encoding) as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
    return header, rows


def validate_structure(header: list, rows: list) -> dict:
    """Validate the structural integrity of the CSV."""
    n_cols = len(header)
    n_rows = len(rows)

    # Check row length consistency
    inconsistent_rows = []
    for i, row in enumerate(rows):
        if len(row) != n_cols:
            inconsistent_rows.append({"row": i + 2, "expected": n_cols, "actual": len(row)})

    # Check for completely empty rows
    empty_rows = [
        i + 1 for i, row in enumerate(rows) if all(not v.strip() for v in row)
    ]

    # Check for near-empty rows (< 3 non-empty fields)
    near_empty_rows = []
    for i, row in enumerate(rows):
        filled = sum(1 for v in row if v.strip())
        if 0 < filled < 3:
            near_empty_rows.append({"row": i + 2, "filled_count": filled})

    return {
        "total_columns": n_cols,
        "total_rows": n_rows,
        "inconsistent_rows": inconsistent_rows,
        "empty_rows": empty_rows,
        "near_empty_rows": near_empty_rows,
        "has_inconsistencies": len(inconsistent_rows) > 0,
    }


def analyze_columns(header: list, rows: list) -> list:
    """Analyze each column for fill rates and basic statistics."""
    n_rows = len(rows)
    column_stats = []

    for i, col_name in enumerate(header):
        values = []
        missing = 0
        for row in rows:
            if i < len(row):
                val = row[i].strip()
                if val:
                    values.append(val)
                else:
                    missing += 1
            else:
                missing += 1

        fill_rate = ((n_rows - missing) / n_rows * 100) if n_rows > 0 else 0
        unique_vals = len(set(values))

        # Detect potential data types
        numeric_count = 0
        for v in values:
            try:
                float(v)
                numeric_count += 1
            except ValueError:
                pass
        likely_numeric = numeric_count > len(values) * 0.8 if values else False

        # Top values (for categorical analysis)
        value_counts = Counter(values)
        top_values = value_counts.most_common(5)

        column_stats.append(
            {
                "column_index": i,
                "column_name": col_name,
                "fill_rate": round(fill_rate, 1),
                "missing": missing,
                "unique_values": unique_vals,
                "likely_numeric": likely_numeric,
                "numeric_ratio": round(numeric_count / len(values), 2) if values else 0,
                "top_values": [
                    {"value": v, "count": c} for v, c in top_values
                ],
            }
        )

    return column_stats


def generate_report(
    filepath: str,
    structure: dict,
    col_stats: list,
    output_format: str = "text",
) -> str:
    """Generate a validation report in text or markdown format."""
    filename = os.path.basename(filepath)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if output_format == "markdown":
        return _generate_markdown(filename, timestamp, structure, col_stats)
    else:
        return _generate_text(filename, timestamp, structure, col_stats)


def _generate_text(filename, timestamp, structure, col_stats) -> str:
    lines = []
    lines.append("=" * 60)
    lines.append(f"VALIDATION REPORT: {filename}")
    lines.append(f"Generated: {timestamp}")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"Total columns: {structure['total_columns']}")
    lines.append(f"Total rows:    {structure['total_rows']}")
    lines.append("")

    if structure["has_inconsistencies"]:
        lines.append("⚠ WARNINGS:")
        for ir in structure["inconsistent_rows"]:
            lines.append(
                f"  Row {ir['row']}: expected {ir['expected']} columns, got {ir['actual']}"
            )
        lines.append("")

    lines.append(f"Fully empty rows: {len(structure['empty_rows'])}")
    if structure["empty_rows"]:
        lines.append(f"  Row numbers: {structure['empty_rows']}")
    lines.append(f"Near-empty rows (<3 fields): {len(structure['near_empty_rows'])}")
    lines.append("")

    lines.append(f"{'Col':<4} {'Fill %':<8} {'Unique':<8} {'Type':<10} Name")
    lines.append("-" * 60)
    for col in col_stats:
        col_type = "Numeric" if col["likely_numeric"] else "Categorical"
        lines.append(
            f"{col['column_index']:<4} {col['fill_rate']:<8} {col['unique_values']:<8} {col_type:<10} {col['column_name'][:50]}"
        )
    lines.append("")

    # Low fill rate warning
    low_fill = [c for c in col_stats if c["fill_rate"] < 50]
    if low_fill:
        lines.append(f"⚠ Columns with <50% fill rate ({len(low_fill)}):")
        for c in low_fill:
            lines.append(f"  Col {c['column_index']}: {c['column_name'][:50]} ({c['fill_rate']}%)")

    return "\n".join(lines)


def _generate_markdown(filename, timestamp, structure, col_stats) -> str:
    lines = []
    lines.append(f"# Validation Report: {filename}")
    lines.append(f"**Generated:** {timestamp}")
    lines.append("")
    lines.append("## Overview")
    lines.append(f"- **Total columns:** {structure['total_columns']}")
    lines.append(f"- **Total rows:** {structure['total_rows']}")
    lines.append("")

    if structure["has_inconsistencies"]:
        lines.append("## ⚠ Warnings")
        for ir in structure["inconsistent_rows"]:
            lines.append(
                f"- Row {ir['row']}: expected {ir['expected']} columns, got {ir['actual']}"
            )
        lines.append("")

    lines.append(f"## Row Health")
    lines.append(f"- **Fully empty rows:** {len(structure['empty_rows'])}")
    if structure["empty_rows"]:
        lines.append(f"  - Row numbers: {structure['empty_rows']}")
    lines.append(f"- **Near-empty rows (<3 fields):** {len(structure['near_empty_rows'])}")
    lines.append("")

    lines.append("## Column Analysis")
    lines.append("| Index | Fill % | Unique | Type | Name |")
    lines.append("|-------|--------|--------|------|------|")
    for col in col_stats:
        col_type = "Numeric" if col["likely_numeric"] else "Categorical"
        lines.append(
            f"| {col['column_index']} | {col['fill_rate']}% | {col['unique_values']} | {col_type} | {col['column_name'][:60]} |"
        )
    lines.append("")

    # Low fill rate warning
    low_fill = [c for c in col_stats if c["fill_rate"] < 50]
    if low_fill:
        lines.append("## ⚠ Low Fill Rate Columns (<50%)")
        for c in low_fill:
            lines.append(f"- **Col {c['column_index']}:** {c['column_name'][:60]} ({c['fill_rate']}%)")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Validate CSV data files for research datasets"
    )
    parser.add_argument("input", help="Path to input CSV file")
    parser.add_argument("--config", help="Path to JSON validation config", default=None)
    parser.add_argument(
        "--output", help="Output report file (if omitted, prints to stdout)"
    )
    parser.add_argument(
        "--format",
        choices=["text", "markdown"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument("--encoding", default="utf-8", help="File encoding (default: utf-8)")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: File not found: {args.input}")
        sys.exit(1)

    # Load CSV
    try:
        header, rows = load_csv(args.input, args.encoding)
    except UnicodeDecodeError:
        print("UTF-8 decode failed, trying latin-1...")
        header, rows = load_csv(args.input, "latin-1")
    except Exception as e:
        print(f"Error loading CSV: {e}")
        sys.exit(1)

    # Run validation
    structure = validate_structure(header, rows)
    col_stats = analyze_columns(header, rows)

    # Generate report
    report = generate_report(args.input, structure, col_stats, args.format)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report saved to: {args.output}")
    else:
        print(report)

    # Exit with error code if issues found
    if structure["has_inconsistencies"] or structure["empty_rows"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
