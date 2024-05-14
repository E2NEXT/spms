
frappe.ui.form.on('Sales Order', {
    refresh(frm) {
        // Set page length to show all items
        frm.get_field("items").grid.grid_pagination.page_length = 99_999;

        frappe.require([
            'assets/spms/node_modules/onscan.js/onscan.js',
        ], () => {
            // Enable scan events for the entire document
            onScan.attachTo(document);

            let debounceTimeout;
            const debounceDelay = 200; // 300 ms delay for debouncing

            document.addEventListener('scan', async (event) => {
                clearTimeout(debounceTimeout);
                debounceTimeout = setTimeout(async () => {
                    const { scanCode: sScanned, qty: iQty } = event.detail;

                    const existingItem = frm.doc.items.find(item => item.custom_barcode_label == sScanned);
                    if (existingItem) {
                        existingItem.qty += 1;
                        await updateItem(existingItem, frm);
                    } else {
                        try {
                            const respItem = await searchItemByBarcode(sScanned);
                            if (respItem) {
                                const row = frm.add_child('items', {
                                    custom_barcode_label: sScanned,
                                    item_code: respItem.parent,
                                    item_name: respItem.parent,
                                    description: respItem.parent,
                                    qty: iQty,
                                    uom: respItem.uom
                                });
                                await updateItem(row, frm);
                            }
                        } catch (error) {
                            console.error('Error searching item by barcode:', error);
                        }
                    }
                }, debounceDelay);
            });
        });
    },
});

// Function to update item in the table
async function updateItem(item, frm) {
    await frm.script_manager.trigger('item_code', item.doctype, item.name);
    frm.refresh_field("items");

    const element = document.querySelector(`[data-name="${item.name}"]`);
    if (element) {
        element.focus();
        element.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
        element.style.border = '1px solid blue';

        setTimeout(() => { element.style.border = 'none'; }, 5000);
    } else {
        console.log('Element with data-name attribute not found');
    }
}

// Function to search item by barcode
function searchItemByBarcode(barcode) {
    return new Promise((resolve, reject) => {
        frappe.call({
            method: 'spms.methods.utils.search_item_by_barcode',
            args: { barcode, parent_doc: "Item" },
            callback(r) {
                if (r.message) {
                    resolve(r.message);
                } else {
                    reject(new Error('Item not found'));
                }
            }
        });
    });
}
