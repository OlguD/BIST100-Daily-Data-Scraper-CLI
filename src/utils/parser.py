import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--stock-name", required=True, help="Stock Name from BIST100")
parser.add_argument("--start", required=True, help="Start date (day-month-year)")
parser.add_argument("--end", required=False, default=None, help="End date (default today (day-month-year))")
parser.add_argument("--prettify", required=False, action=argparse.BooleanOptionalAction, help="End date (default today)")
parser.add_argument("--export-to-excel", required=False, help="Write file path you want to save excel file")
parser.add_argument("--export-to-csv", required=False, help="Write file path you want to save csv file")
args = parser.parse_args()
