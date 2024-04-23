import frappe


def before_save(doc, method) -> None:
    for row in doc.barcodes:
        if not row.custom_hash:
            row.custom_hash = row.barcode
