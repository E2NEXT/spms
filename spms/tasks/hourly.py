import frappe

def barcode_index():
    # Check if the index already exists
    index_exists = frappe.db.sql("""
        SELECT COUNT(1)
        FROM INFORMATION_SCHEMA.STATISTICS
        WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = 'tabItem Barcode'
        AND INDEX_NAME = 'barcode'
    """)[0][0]

    if not index_exists:
        # Create index if it does not exist
        frappe.db.sql("ALTER TABLE `tabItem Barcode` ADD INDEX `barcode` (barcode)")
        frappe.db.commit()
