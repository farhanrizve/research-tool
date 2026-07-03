"""
CSV cleaning utility for research datasets.

Features:
- Remove columns by index or name pattern
- Remove empty/near-empty rows
- Strip whitespace from all fields
- Fill missing values with defaults
- Rename columns
- Reorder columns
- Output encoding conversion

Usage:
    python scripts/clean_csv.py <input.csv> --drop-cols 0,1
    python scripts/clean_csv.py <input.csv> --drop-empty-rows --output cleaned.csv
    python scripts/clean_csv.py <input.csv> --strip --fill-missing "N/A"
    python scripts/clean_csv.py <input.csv> --rename "Old Name:New Name"
"""

import csv
import os
import re
import sys
import argparse


def load_csv(filepath: str, encoding: str = "utf-8") -> tuple:
    """Load a CSV file and return (header, rows)."""
    with open(filepath, "r", encoding=encoding) as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
    return header, rows


def save_csv(header: list, rows: list, filepath: str, encoding: str = "utf-8-sig"):
    """Save data to CSV with UTF-8 BOM (for Excel compatibility)."""
    with open(filepath, "w", newline="", encoding=encoding) as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def drop_columns(header: list, rows: list, indices: list[int]) -> tuple:
    """Drop columns by index (0-based)."""
    keep = [i for i in range(len(header)) if i not in indices]
    new_header = [header[i] for i in keep]
    new_rows = []
    for row in rows:
        new_rows.append([row[i] for i in keep if i < len(row)])
    return new_header, new_rows


def drop_columns_by_pattern(header: list, rows: list, pattern: str) -> tuple:
    """Drop columns whose names match a regex pattern."""
    compiled = re.compile(pattern, re.IGNORECASE)
    keep = [i for i, h in enumerate(header) if not compiled.search(h)]
    return drop_columns(header, rows, [i for i in range(len(header)) if i not in keep])


def keep_columns(header: list, rows: list, indices: list[int]) -> tuple:
    """Keep only specified column indices."""
    new_header = [header[i] for i in indices]
    new_rows = []
    for row in rows:
        new_rows.append([row[i] for i in indices if i < len(row)])
    return new_header, new_rows


def keep_columns_by_pattern(header: list, rows: list, pattern: str) -> tuple:
    """Keep only columns whose names match a regex pattern."""
    compiled = re.compile(pattern, re.IGNORECASE)
    keep = [i for i, h in enumerate(header) if compiled.search(h)]
    return keep_columns(header, rows, keep)


def drop_empty_rows(header: list, rows: list, threshold: int = 1) -> tuple:
    """Drop rows with fewer than threshold non-empty fields."""
    new_rows = []
    dropped = 0
    for row in rows:
        filled = sum(1 for v in row if v.strip())
        if filled >= threshold:
            new_rows.append(row)
        else:
            dropped += 1
    return header, new_rows, dropped


def strip_fields(header: list, rows: list) -> tuple:
    """Strip whitespace from all fields."""
    new_rows = []
    for row in rows:
        new_rows.append([v.strip() for v in row])
    return header, new_rows


def fill_missing(header: list, rows: list, fill_value: str = "") -> tuple:
    """Fill empty fields with a specified value."""
    new_rows = []
    for row in rows:
        new_rows.append([v if v.strip() else fill_value for v in row])
    return header, new_rows


def rename_columns(header: list, renames: dict) -> list:
    """Rename columns using a mapping dict {old: new}."""
    new_header = [renames.get(h, h) for h in header]
    return new_header


def reorder_columns(header: list, rows: list, order: list[int]) -> tuple:
    """Reorder columns by specified index order."""
    new_header = [header[i] for i in order]
    new_rows = []
    for row in rows:
        new_rows.append([row[i] for i in order if i < len(row)])
    return new_header, new_rows


def filter_rows(header: list, rows: list, column: int, pattern: str) -> tuple:
    """Keep only rows where specified column matches a regex pattern."""
    compiled = re.compile(pattern, re.IGNORECASE)
    new_rows = [row for row in rows if column < len(row) and compiled.search(row[column])]
    return header, new_rows, len(rows) - len(new_rows)


def main():
    parser = argparse.ArgumentParser(
        description="Clean and transform CSV data files for research"
    )
    parser.add_argument("input", help="Path to input CSV file")
    parser.add_argument("-o", "--output", help="Output CSV path (default: overwrites input)")
    parser.add_argument(
        "--drop-cols",
        help="Comma-separated column indices to drop (e.g., '0,1,5')",
    )
    parser.add_argument(
        "--drop-pattern",
        help="Drop columns matching this regex pattern",
    )
    parser.add_argument(
        "--keep-cols",
        help="Comma-separated column indices to keep (e.g., '0,2,4')",
    )
    parser.add_argument(
        "--keep-pattern",
        help="Keep only columns matching this regex pattern",
    )
    parser.add_argument(
        "--drop-empty-rows",
        action="store_true",
        help="Drop rows with no data",
    )
    parser.add_argument(
        "--min-filled",
        type=int,
        default=1,
        help="Minimum filled fields to keep a row (default: 1)",
    )
    parser.add_argument(
        "--strip", action="store_true", help="Strip whitespace from all fields"
    )
    parser.add_argument(
        "--fill-missing", help="Fill empty fields with this value"
    )
    parser.add_argument(
        "--rename",
        nargs="+",
        help="Rename columns: 'Old Name:New Name' 'Old2:New2'",
    )
    parser.add_argument(
        "--reorder",
        help="Comma-separated new column order indices (e.g., '2,0,1')",
    )
    parser.add_argument(
        "--filter",
        nargs=2,
        metavar=("COLUMN_INDEX", "PATTERN"),
        help="Keep rows where column matches pattern. Usage: --filter 0 'keyword'",
    )
    parser.add_argument("--encoding", default="utf-8", help="Input encoding (default: utf-8)")
    parser.add_argument(
        "--dry-run", action="store_true", help="Print changes without saving"
    )
    parser.add_argument("--summary", action="store_true", help="Print summary of changes")

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

    original = (list(header), [list(r) for r in rows])

    # Apply transformations in order
    changes = []

    if args.drop_cols:
        indices = [int(i.strip()) for i in args.drop_cols.split(",")]
        header, rows = drop_columns(header, rows, indices)
        changes.append(f"Dropped columns: {indices}")

    if args.drop_pattern:
        header, rows = drop_columns_by_pattern(header, rows, args.drop_pattern)
        changes.append(f"Dropped columns matching pattern: {args.drop_pattern}")

    if args.keep_cols:
        indices = [int(i.strip()) for i in args.keep_cols.split(",")]
        header, rows = keep_columns(header, rows, indices)
        changes.append(f"Kept only columns: {indices}")

    if args.keep_pattern:
        header, rows = keep_columns_by_pattern(header, rows, args.keep_pattern)
        changes.append(f"Kept only columns matching pattern: {args.keep_pattern}")

    if args.drop_empty_rows:
        header, rows, dropped = drop_empty_rows(header, rows, args.min_filled)
        changes.append(f"Dropped {dropped} empty/near-empty rows")

    if args.strip:
        header, rows = strip_fields(header, rows)
        changes.append("Stripped whitespace from all fields")

    if args.fill_missing:
        header, rows = fill_missing(header, rows, args.fill_missing)
        changes.append(f"Filled empty fields with '{args.fill_missing}'")

    if args.rename:
        renames = {}
        for r in args.rename:
            if ":" in r:
                old, new = r.split(":", 1)
                renames[old.strip()] = new.strip()
        header = rename_columns(header, renames)
        changes.append(f"Renamed columns: {renames}")

    if args.reorder:
        order = [int(i.strip()) for i in args.reorder.split(",")]
        header, rows = reorder_columns(header, rows, order)
        changes.append(f"Reordered columns to: {order}")

    if args.filter:
        col, pattern = int(args.filter[0]), args.filter[1]
        header, rows, filtered = filter_rows(header, rows, col, pattern)
        changes.append(f"Filtered out {filtered} rows (kept pattern '{pattern}' in col {col})")

    # Summary
    changed = (header != original[0]) or (rows != original[1])
    if args.summary or args.dry_run:
        print("=" * 60)
        print(f"CLEAN SUMMARY: {os.path.basename(args.input)}")
        print("=" * 60)
        print(f"Original:  {len(original[1])} rows × {len(original[0])} cols")
        print(f"Cleaned:   {len(rows)} rows × {len(header)} cols")
        print(f"Changes:   {len(changes)}")
        for c in changes:
            print(f"  • {c}")
        print(f"Modified:  {'Yes' if changed else 'No'}")
        print("=" * 60)

    # Save
    if args.dry_run:
        print("\nDry run — no file written.")
    elif args.output:
        save_csv(header, rows, args.output)
        print(f"Saved to: {args.output}")
    elif changed:
        save_csv(header, rows, args.input)
        print(f"Overwritten: {args.input}")
    else:
        print("No changes needed.")


if __name__ == "__main__":
    main()
