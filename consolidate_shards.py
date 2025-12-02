import argparse
import os
from pathlib import Path
import csv

HOSP_DIR = Path(r"C:\Users\shawn\OneDrive\Documents\PITT MDS\Case Studies in Data Science\ICU_Capstone\data\hosp")
ICU_DIR  = Path(r"C:\Users\shawn\OneDrive\Documents\PITT MDS\Case Studies in Data Science\ICU_Capstone\data\hosp")
OUT_DIR  = Path(r"C:\Users\shawn\OneDrive\Documents\PITT MDS\Case Studies in Data Science\ICU_Capstone\data\flat_csv")

HOSP_SHARDED = ["diagnoses_icd.csv", "hcpcsevents.csv", "procedures_icd.csv", "provider.csv"]
ICU_SHARDED  = ["caregiver.csv"]

def list_member_files(folder: Path):
    # Return all regular files inside the sharded "csv" folder (ignore subfolders)
    return sorted([p for p in folder.iterdir() if p.is_file()])

def sniff_max_cols(files):
    """
    Determine max number of comma-separated columns across shards.
    If a file has content, read its lines; otherwise treat the FILENAME as the row.
    """
    max_cols = 0
    for fp in files:
        size = fp.stat().st_size
        if size > 0:
            with fp.open("r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.rstrip("\r\n")
                    if not line:
                        continue
                    max_cols = max(max_cols, len(line.split(",")))
        else:
            # filename encodes the row
            name_row = fp.name  # e.g., "10002428,25797028,2155-07-14,G0378,1,Hospital"
            if name_row:
                max_cols = max(max_cols, len(name_row.split(",")))
    return max_cols

def consolidate_folder_to_csv(folder: Path, out_csv: Path, header=None):
    """
    Consolidate shard files in 'folder' into a single CSV at 'out_csv'.
    Supports shards where the data is in the FILENAME (0 KB files) or in file contents.
    """
    files = list_member_files(folder)
    if not files:
        print(f"  - Skipping empty folder: {folder}")
        return

    max_cols = sniff_max_cols(files)
    if max_cols == 0:
        print(f"  - No rows found in: {folder}")
        return

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as outf:
        writer = csv.writer(outf)
        # Write header
        if header:
            writer.writerow(header)
        else:
            writer.writerow([f"col_{i+1}" for i in range(max_cols)])

        # Stream rows
        for fp in files:
            size = fp.stat().st_size
            if size > 0:
                with fp.open("r", encoding="utf-8", errors="replace") as f:
                    for line in f:
                        line = line.rstrip("\r\n")
                        if not line:
                            continue
                        row = line.split(",")
                        row += [""] * (max_cols - len(row))
                        writer.writerow(row)
            else:
                # Use filename as the row
                row = fp.name.split(",")
                row += [""] * (max_cols - len(row))
                writer.writerow(row)

    print(f"  ✓ Wrote {out_csv}")

def maybe_fix_table(base_dir: Path, table_name: str, out_root: Path):
    """
    If base_dir/<table_name> is a folder => consolidate parts into out_root/<table_name>.
    If base_dir/<table_name> is a normal file => skip (already flat).
    """
    src_folder = base_dir / table_name
    src_file   = base_dir / table_name  # if someone already gave a real file

    out_csv = out_root / table_name

    if src_folder.exists() and src_folder.is_dir():
        print(f"* Consolidating folder: {src_folder}")
        # If a 'real' header file exists inside (rare), try to use it as header
        header = None
        header_candidate = src_folder / table_name  # e.g., admissions.csv/admissions.csv
        if header_candidate.exists() and header_candidate.is_file():
            with header_candidate.open("r", encoding="utf-8", errors="replace") as f:
                first_line = f.readline().rstrip("\n\r")
                if first_line:
                    header = first_line.split(",")

        consolidate_folder_to_csv(src_folder, out_csv, header=header)
        return

    if src_file.exists() and src_file.is_file():
        print(f"* Found flat file already: {src_file} (skipping)")
        return

    print(f"* WARNING: {table_name} not found in {base_dir} (skipping)")

def main():
    ap = argparse.ArgumentParser(description="Consolidate sharded MIMIC demo CSV folders into single CSVs.")
    ap.add_argument("--hosp", type=str, required=True, help="Path to the hosp module directory")
    ap.add_argument("--icu",  type=str, required=True, help="Path to the icu module directory")
    ap.add_argument("--out",  type=str, default="flat_csv", help="Output directory for flat CSVs (created if missing)")
    args = ap.parse_args()

    hosp_dir = Path(args.hosp)
    icu_dir  = Path(args.icu)
    out_root = Path(args.out)

    hosp_out = out_root / "hosp"
    icu_out  = out_root / "icu"
    hosp_out.mkdir(parents=True, exist_ok=True)
    icu_out.mkdir(parents=True, exist_ok=True)

    print("\n=== HOSP module ===")
    for name in HOSP_SHARDED:
        maybe_fix_table(hosp_dir, name, hosp_out)

    print("\n=== ICU module ===")
    for name in ICU_SHARDED:
        maybe_fix_table(icu_dir, name, icu_out)

    print(f"\nDone. Flat CSVs (if created) are in: {out_root}\n")

if __name__ == "__main__":
    main()