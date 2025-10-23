import argparse


parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--stock-name", dest="stock_name", required=False, help="Stock Name from BIST100")
group.add_argument("--multiple", dest="multiple", required=False, action="store_true", help="Fetch every symbol in BIST100")

parser.add_argument("--start", required=True, help="Start date (day-month-year)")
parser.add_argument("--end", required=False, default=None, help="End date (default today (day-month-year))")
parser.add_argument("--prettify", required=False, action=argparse.BooleanOptionalAction, help="Pretty-print JSON output")
parser.add_argument("--export-to-excel", dest="export_to_excel", required=False, help="Write file path you want to save excel file")
parser.add_argument("--export-to-csv", dest="export_to_csv", required=False, help="Write file path you want to save csv file")

args = parser.parse_args()
