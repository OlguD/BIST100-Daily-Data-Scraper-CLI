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


def main(name, start_date, end_date, prettify, export_to_excel, export_to_csv, multiple):
    if not start_date:
        print("Lütfen --start argümanını sağlayın.")
        return

    a = scraper.Scraper()

    if multiple:
        if end_date:
            raw_map = a.fetch_multiple_symbols(start_date, end_date)
        else:
            raw_map = a.fetch_multiple_symbols(start_date)

        processed_map = {}
        any_success = False
        for sym, raw in (raw_map or {}).items():
            proc = a.process_data(raw)
            processed_map[sym] = proc
            if proc and proc.get("status"):
                any_success = True

        if not any_success:
            print("Hiç veri bulunamadı veya hata oluştu (multiple mode)")
            print(processed_map)
            return

        result = {
            "multiple": True,
            "data": processed_map,
            "status": True
        }

    else:
        if not name:
            print("Lütfen --stock-name argümanını sağlayın.")
            return

        if end_date:
            data = a.fetch_data(name, start_date, end_date)
        else:
            data = a.fetch_data(name, start_date)

        result = a.process_data(data)

    if not result or not result.get("status"):
        print("Veri yok veya hata")
        print(result)
        return

    list_for_print = []
    if isinstance(result, dict) and result.get("multiple"):
        for sym, proc in (result.get("data") or {}).items():
            items = proc.get("data") or []
            for it in items:
                try:
                    converter = getattr(it, "to_dict", None)
                    row = converter() if callable(converter) else getattr(it, "__dict__", dict())
                except Exception:
                    row = {"raw": str(it)}

                if isinstance(row, dict):
                    row.setdefault("symbol", sym)
                list_for_print.append(row)
    else:
        items = result.get("data") if isinstance(result, dict) else []
        for it in (items or []):
            try:
                converter = getattr(it, "to_dict", None)
                row = converter() if callable(converter) else getattr(it, "__dict__", dict())
            except Exception:
                row = {"raw": str(it)}
            list_for_print.append(row)

    is_multiple = isinstance(result, dict) and result.get("multiple")
    if not is_multiple:
        if prettify:
            print(json.dumps(list_for_print, ensure_ascii=False, indent=2))
        else:
            print({"status": result.get("status"), "rows": len(list_for_print)})

    if export_to_excel:
        Export.export_to_excel(export_to_excel, list_for_print)

    if export_to_csv:
        Export.export_to_csv(export_to_csv, list_for_print)

if __name__ == "__main__":
    args = parser.args
    name = _get_arg(args, "stock_name")
    start_date = _get_arg(args, "start")
    end_date = _get_arg(args, "end")
    prettify = _get_arg(args, "prettify", False)
    export_to_excel = _get_arg(args, "export_to_excel")
    export_to_csv = _get_arg(args, "export_to_csv")
    fetch_multiple = _get_arg(args, "multiple")
    main(name, start_date, end_date, prettify, export_to_excel, export_to_csv, fetch_multiple)