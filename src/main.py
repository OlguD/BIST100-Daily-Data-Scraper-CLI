from scraper import scraper
import json
from utils import parser
from utils.export import Export


def _get_arg(args_obj, name, default=None):
    """Helper: accept argparse.Namespace or dict-like and return value safely."""
    if args_obj is None:
        return default
    # Namespace-like
    try:
        return getattr(args_obj, name)
    except Exception:
        pass
    # Mapping-like fallback
    try:
        return args_obj[name]
    except Exception:
        return default


def main(name, start_date, end_date, prettify, export_to_excel, export_to_csv):
    if not name or not start_date:
        print("Lütfen --stock-name ve --start argümanlarını sağlayın.")
        return

    a = scraper.Scraper()
    # fetch_data accepts optional end_date
    if end_date:
        data = a.fetch_data(name, start_date, end_date)
    else:
        data = a.fetch_data(name, start_date)

    result = a.process_data(data)

    if not result or not result.get("status"):
        print("Veri yok veya hata")
        print(result)
        return

    # Safe prettify
    if prettify:
        items = result.get("data") or []
        list_dict = []
        for it in items:
            try:
                converter = getattr(it, "to_dict", None)
                if callable(converter):
                    list_dict.append(converter())
                else:
                    list_dict.append(getattr(it, "__dict__", dict()))
            except Exception:
                list_dict.append(str(it))

        print(json.dumps(list_dict, ensure_ascii=False, indent=2))

    # final raw print
    else:
        print(result)

    if export_to_excel:
        data_for_export = result.get("data") if isinstance(result, dict) else result
        Export.export_to_excel(export_to_excel, data_for_export)

    if export_to_csv:
        data_for_export = result.get("data") if isinstance(result, dict) else result
        Export.export_to_csv(export_to_csv, data_for_export)

if __name__ == "__main__":
    # parser.args is an argparse.Namespace; accept both Namespace or dict
    args = parser.args
    # argparse stores names without the leading dashes as attributes
    name = _get_arg(args, "stock_name") or _get_arg(args, "stock-name") or _get_arg(args, "--stock-name")
    start_date = _get_arg(args, "start")
    end_date = _get_arg(args, "end")
    prettify = _get_arg(args, "prettify", False)
    export_to_excel = _get_arg(args, "export_to_excel") or _get_arg(args, "export-to-excel") or _get_arg(args, "--export-to-excel")
    export_to_csv = _get_arg(args, "export_to_csv") or _get_arg(args, "export-to-csv") or _get_arg(args, "--export-to-csv")
    main(name, start_date, end_date, prettify, export_to_excel, export_to_csv)