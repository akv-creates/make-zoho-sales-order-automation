#!/usr/bin/env python3
"""Fill in your own IDs so the blueprints are ready to import into Make.

    python3 tools/fill_placeholders.py \
        --zoho-org 60012345678 \
        --spreadsheet "https://docs.google.com/spreadsheets/d/1AbC.../edit" \
        [--drive-folder FOLDER_ID_OR_URL [--drive-subfolder SUBFOLDER_ID_OR_URL]]

Writes ready-to-import copies to ./my-scenarios/ (your originals are not touched) and tells you what is
still left to do by hand (the connections). Standard library only, no installs.
"""
import argparse, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "scenarios"
OUT = ROOT / "my-scenarios"


def sheet_id(v):
    m = re.search(r"/d/([A-Za-z0-9_-]+)", v)
    return m.group(1) if m else v.strip().strip("/")


def folder_id(v):
    m = re.search(r"/folders/([A-Za-z0-9_-]+)", v)
    return m.group(1) if m else v.strip().strip("/")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--zoho-org", required=True, help="Zoho Books Organization ID (Settings > Organization Profile)")
    ap.add_argument("--spreadsheet", required=True, help="Google Sheet URL or ID (form responses + 'Errors' tab)")
    ap.add_argument("--drive-folder", help="Drive folder URL/ID where form uploads land (only for photo/PDF orders)")
    ap.add_argument("--drive-subfolder", help="Optional sub-folder URL/ID inside that folder")
    a = ap.parse_args()

    OUT.mkdir(exist_ok=True)
    left_over = set()
    for src in sorted(SRC.rglob("*.blueprint.json")):
        text = src.read_text(encoding="utf-8")
        text = text.replace("YOUR_ZOHO_ORG_ID", a.zoho_org.strip())
        text = text.replace("/YOUR_SPREADSHEET_ID", "/" + sheet_id(a.spreadsheet))
        if a.drive_folder:
            fid = folder_id(a.drive_folder)
            if a.drive_subfolder:
                text = text.replace("/YOUR_DRIVE_FOLDER_ID/YOUR_DRIVE_SUBFOLDER_ID",
                                    "/%s/%s" % (fid, folder_id(a.drive_subfolder)))
            else:
                text = text.replace("/YOUR_DRIVE_FOLDER_ID/YOUR_DRIVE_SUBFOLDER_ID", "/" + fid)
        json.loads(text)  # make sure we still have valid JSON
        dest = OUT / src.name
        dest.write_text(text, encoding="utf-8")
        left_over |= set(re.findall(r"YOUR_[A-Z_]+", text))
        print("wrote", dest.relative_to(ROOT))

    print("\nNext: import the files from my-scenarios/ into Make, then pick your connections in each module.")
    if left_over:
        print("Still placeholders (fine if you do not use the photo/PDF route):", ", ".join(sorted(left_over)))


if __name__ == "__main__":
    sys.exit(main())
