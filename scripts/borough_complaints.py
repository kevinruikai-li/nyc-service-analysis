import argparse
import csv
import sys
from datetime import datetime

parser = argparse.ArgumentParser(description='Number of each complaint type per borough for a given (creation) date range')
parser.add_argument('-i', '--input', type=str, required=True, help='The input csv file path')
parser.add_argument('-s', '--start', type=str, required=True, help='The start date in YYYY-MM-DD format')
parser.add_argument('-e', '--end', type=str, required=True, help='The end date in YYYY-MM-DD format')
parser.add_argument('-o', '--output', type=str, required=False, help='The output csv file path')

args = parser.parse_args()
start_date = datetime.fromisoformat(args.start).date()
end_date = datetime.fromisoformat(args.end).date()

with open(args.input, mode='r', newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    header = reader.fieldnames

    counts = {}
    for row in reader:
        date_format = "%m/%d/%Y %I:%M:%S %p"
        created_date = datetime.strptime(row.get("Created Date", "").strip(), date_format).date()
        if not (start_date <= created_date <= end_date):
            continue
        complaint = (row.get("Complaint Type") or "").strip() or "UNKNOWN"
        borough = (row.get("Borough") or "").strip() or "UNKNOWN"

        counts[(complaint, borough)] = counts.get((complaint, borough), 0) + 1

    out_fh = None
    try:
        if args.output:
            out_fh = open(args.output, "w", newline="", encoding="utf-8")
        else:
            out_fh = sys.stdout

        writer = csv.writer(out_fh)
        writer.writerow(["complaint type", "borough", "count"])
        for (complaint, borough), cnt in sorted(counts.items(), key=lambda x: (x[0], -x[1])):
            writer.writerow([complaint, borough, cnt])

    finally:
        if args.output and out_fh is not None:
            out_fh.close()