// class LRUCache {
//     constructor(limit = 100) {
//         this.cache = new Map();
//         this.limit = limit;
//     }

//     get(key) {
//         if (!this.cache.has(key)) {
//             return null;
//         }
//         const value = this.cache.get(key);
//         // Move the accessed key to the end to show it is recently used
//         this.cache.delete(key);
//         this.cache.set(key, value);
//         return value;
//     }

//     set(key, value) {
//         if (this.cache.has(key)) {
//             // Delete the key so that it can be added to the end of the Map
//             this.cache.delete(key);
//         } else if (this.cache.size >= this.limit) {
//             // Delete the first item in the Map (least recently used)
//             const firstKey = this.cache.keys().next().value;
//             this.cache.delete(firstKey);
//         }
//         this.cache.set(key, value);
//     }
// }

frappe.ui.form.on('Sales Team', {
    refresh(frm) {
        frm.doc.sales_team.forEach(element => {
            element.incentives = frm.doc.net_total * (element.commission_rate / 100);
        });
        frm.refresh_field('sales_team');
    }
});


//////////////////////////////////////////////////////

// frappe.ui.form.on('Sales Invoice', {
//     refresh(frm) {
//         // Set page length to show all items
//         frappe.db.get_single_value('SPMS Settings', 'max_child_table_rows')
//             .then(max_rows => {

//                 if (max_rows == 0) {
//                     frm.get_field("items").grid.grid_pagination.page_length = 50; // Default 50
//                 } else {
//                     frm.get_field("items").grid.grid_pagination.page_length = max_rows;
//                 }
//             })

//         frappe.require([
//             'assets/spms/node_modules/onscan.js/onscan.js',
//         ], () => {
//             // Enable scan events for the entire document
//             onScan.attachTo(document);
//             document.addEventListener('scan', async (event) => {
//                 const { scanCode: sScanned, qty: iQty } = event.detail;

//                 const existingItem = frm.doc.items.find(item => item.custom_barcode_label == sScanned);
//                 if (existingItem) {
//                     existingItem.qty += 1;
//                     updateItem(existingItem, frm);
//                 } else {
//                     const respItem = await searchItemByBarcode(sScanned);
//                     if (respItem) {
//                         const row = frm.add_child('items', {
//                             custom_barcode_label: sScanned,
//                             item_code: respItem.parent,
//                             item_name: respItem.parent,
//                             description: respItem.parent,
//                             qty: iQty,
//                             uom: respItem.uom
//                         });
//                         updateItem(row, frm);
//                     }
//                 }
//             });
//         });
//     },
// });

// // Function to update item in the table
// function updateItem(item, frm) {
//     frm.script_manager.trigger('item_code', item.doctype, item.name);
//     frm.refresh_field("items");
//     const element = document.querySelector(`[data-name="${item.name}"]`);
//     if (element) {
//         element.focus();
//         element.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
//         element.style.border = '1px solid blue';

//         setTimeout(() => { element.style.border = 'none'; }, 5000);
//     } else {
//         console.log('Element with data-name attribute not found');
//     }
// }

// // Function to search item by barcode
// function searchItemByBarcode(barcode) {
//     return new Promise((resolve, reject) => {
//         frappe.call({
//             method: 'spms.methods.utils.search_item_by_barcode',
//             args: { barcode, parent_doc: "Item" },
//             callback(r) {
//                 if (r.message) {
//                     resolve(r.message);
//                 } else {
//                     reject(new Error('Item not found'));
//                 }
//             }
//         });
//     });
// }



////////////////////////////////////////////////////////////////////

// frappe.ui.form.on('Sales Invoice', {
//     refresh(frm) {
//         // Set page length to show all items
//         frappe.db.get_single_value('SPMS Settings', 'max_child_table_rows')
//             .then(max_rows => {

//                 if (max_rows == 0) {
//                     frm.get_field("items").grid.grid_pagination.page_length = 50; // Default 50
//                 } else {
//                     frm.get_field("items").grid.grid_pagination.page_length = max_rows;
//                 }
//             })

//         frappe.require([
//             'assets/spms/node_modules/onscan.js/onscan.js',
//         ], () => {
//             // Enable scan events for the entire document
//             onScan.attachTo(document);
//             document.addEventListener('scan', async (event) => {
//                 const { scanCode: sScanned, qty: iQty } = event.detail;

//                 const existingItem = frm.doc.items.find(item => item.custom_barcode_label == sScanned);
//                 if (existingItem) {
//                     existingItem.qty += 1;
//                     await updateItem(existingItem, frm);
//                 } else {
//                     const respItem = await searchItemByBarcode(sScanned);
//                     if (respItem) {
//                         const row = frm.add_child('items', {
//                             custom_barcode_label: sScanned,
//                             item_code: respItem.parent,
//                             item_name: respItem.parent,
//                             description: respItem.parent,
//                             qty: iQty,
//                             uom: respItem.uom
//                         });
//                         await updateItem(row, frm);
//                     }
//                 }
//             });
//         });
//     },
// });

// // Function to update item in the table
// async function updateItem(item, frm) {
//     frm.script_manager.trigger('item_code', item.doctype, item.name);
//     await frm.refresh_field("items");

//     const pageLength = frm.get_field("items").grid.grid_pagination.page_length;
//     const pageIndex = Math.floor(item.idx / pageLength);

//     frm.get_field("items").grid.grid_pagination.go_to_page(pageIndex+1);

//     setTimeout(() => {
//         const element = document.querySelector(`[data-name="${item.name}"]`);
//         if (element) {
//             element.focus();
//             element.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
//             element.style.border = '2px solid blue';
//             element.style.backgroundColor = 'lightyellow';

//             setTimeout(() => {
//                 element.style.border = 'none';
//                 element.style.backgroundColor = 'transparent';
//             }, 5000);
//         } else {
//             console.log('Element with data-name attribute not found');
//         }
//     }, 300);
// }

// // Function to search item by barcode
// function searchItemByBarcode(barcode) {
//     return new Promise((resolve, reject) => {
//         frappe.call({
//             method: 'spms.methods.utils.search_item_by_barcode',
//             args: { barcode, parent_doc: "Item" },
//             callback(r) {
//                 if (r.message) {
//                     resolve(r.message);
//                 } else {
//                     reject(new Error('Item not found'));
//                 }
//             }
//         });
//     });
// }

////////////////////////////////////////////////////////////////////

// frappe.ui.form.on('Sales Invoice', {
//     refresh(frm) {
//         // Set page length to show all items
//         frappe.db.get_single_value('SPMS Settings', 'max_child_table_rows')
//             .then(max_rows => {
//                 frm.get_field("items").grid.grid_pagination.page_length = max_rows || 50;
//             });

//         // Preload item barcode data
//         preloadItemData(frm);

//         frappe.require([
//             'assets/spms/node_modules/onscan.js/onscan.js',
//         ], () => {
//             // Enable scan events for the entire document
//             onScan.attachTo(document);
//             document.addEventListener('scan', async (event) => {
//                 const { scanCode: sScanned, qty: iQty } = event.detail;
//                 await handleBarcodeScan(sScanned, iQty, frm);
//             });
//         });
//     },
// });

// const itemCache = {};

// // Preload item barcode data
// async function preloadItemData(frm) {
//     const itemBarcodes = await frappe.call({
//         method: 'spms.methods.utils.get_all_item_barcodes',
//     });

//     if (itemBarcodes.message) {
//         itemBarcodes.message.forEach(item => {
//             itemCache[item.barcode] = item;
//         });
//     }
// }

// async function handleBarcodeScan(sScanned, iQty, frm) {
//     const existingItem = frm.doc.items.find(item => item.custom_barcode_label == sScanned);
//     if (existingItem) {
//         existingItem.qty += 1;
//         await updateItem(existingItem, frm);
//     } else {
//         let respItem = itemCache[sScanned];
//         if (!respItem) {
//             respItem = await searchItemByBarcode(sScanned);
//             if (respItem) {
//                 itemCache[sScanned] = respItem;
//             }
//         }

//         if (respItem) {
//             const row = frm.add_child('items', {
//                 custom_barcode_label: sScanned,
//                 item_code: respItem.parent,
//                 item_name: respItem.parent,
//                 description: respItem.parent,
//                 qty: iQty,
//                 uom: respItem.uom
//             });
//             await updateItem(row, frm);
//         }
//     }
// }

// // Function to update item in the table
// async function updateItem(item, frm) {
//     frm.script_manager.trigger('item_code', item.doctype, item.name);
//     await frm.refresh_field("items");

//     const pageLength = frm.get_field("items").grid.grid_pagination.page_length;
//     const pageIndex = Math.floor(item.idx / pageLength);

//     frm.get_field("items").grid.grid_pagination.go_to_page(pageIndex + 1);

//     setTimeout(() => {
//         const element = document.querySelector(`[data-name="${item.name}"]`);
//         if (element) {
//             element.focus();
//             element.scrollIntoView({ behavior: 'auto', block: 'center', inline: 'center' });
//             element.style.border = '2px solid blue';
//             element.style.backgroundColor = 'lightyellow';

//             setTimeout(() => {
//                 element.style.border = 'none';
//                 element.style.backgroundColor = 'transparent';
//             }, 5000);
//         } else {
//             console.log('Element with data-name attribute not found');
//         }
//     }, 300);
// }

// // Function to search item by barcode
// function searchItemByBarcode(barcode) {
//     return new Promise((resolve, reject) => {
//         frappe.call({
//             method: 'spms.methods.utils.search_item_by_barcode',
//             args: { barcode, parent_doc: "Item" },
//             callback(r) {
//                 if (r.message) {
//                     resolve(r.message);
//                 } else {
//                     reject(new Error('Item not found'));
//                 }
//             }
//         });
//     });
// }



///////////////////////////////////////////////////////////////////////


// const itemCache = new LRUCache(500); // Limit the cache size to 500 items

// frappe.ui.form.on('Sales Invoice', {
//     refresh(frm) {
//         // Set page length to show all items
//         frappe.db.get_single_value('SPMS Settings', 'max_child_table_rows')
//             .then(max_rows => {
//                 frm.get_field("items").grid.grid_pagination.page_length = max_rows || 50;
//             });

//         frappe.require([
//             'assets/spms/node_modules/onscan.js/onscan.js',
//         ], () => {
//             // Enable scan events for the entire document
//             onScan.attachTo(document);
//             document.addEventListener('scan', async (event) => {
//                 const { scanCode: sScanned, qty: iQty } = event.detail;
//                 await handleBarcodeScan(sScanned, iQty, frm);
//             });
//         });
//     },
// });

// async function handleBarcodeScan(sScanned, iQty, frm) {
//     const existingItem = frm.doc.items.find(item => item.custom_barcode_label == sScanned);
//     if (existingItem) {
//         existingItem.qty += 1;
//         await updateItem(existingItem, frm);
//     } else {
//         let respItem = itemCache.get(sScanned);
//         if (!respItem) {
//             respItem = await searchItemByBarcode(sScanned);
//             if (respItem) {
//                 itemCache.set(sScanned, respItem);
//             }
//         }

//         if (respItem) {
//             const row = frm.add_child('items', {
//                 custom_barcode_label: sScanned,
//                 item_code: respItem.parent,
//                 item_name: respItem.parent,
//                 description: respItem.parent,
//                 qty: iQty,
//                 uom: respItem.uom
//             });
//             await updateItem(row, frm);
//         }
//     }
// }

// // Function to update item in the table
// async function updateItem(item, frm) {
//     frm.script_manager.trigger('item_code', item.doctype, item.name);
//     await frm.refresh_field("items");

//     const pageLength = frm.get_field("items").grid.grid_pagination.page_length;
//     const pageIndex = Math.floor(item.idx / pageLength);

//     frm.get_field("items").grid.grid_pagination.go_to_page(pageIndex + 1);

//     setTimeout(() => {
//         const element = document.querySelector(`[data-name="${item.name}"]`);
//         if (element) {
//             element.focus();
//             element.scrollIntoView({ behavior: 'auto', block: 'center', inline: 'center' });
//             element.style.border = '2px solid blue';
//             element.style.backgroundColor = 'lightyellow';

//             setTimeout(() => {
//                 element.style.border = 'none';
//                 element.style.backgroundColor = 'transparent';
//             }, 5000);
//         } else {
//             console.log('Element with data-name attribute not found');
//         }
//     }, 300);
// }

// // Function to search item by barcode
// function searchItemByBarcode(barcode) {
//     return new Promise((resolve, reject) => {
//         frappe.call({
//             method: 'spms.methods.utils.search_item_by_barcode',
//             args: { barcode, parent_doc: "Item" },
//             callback(r) {
//                 if (r.message) {
//                     resolve(r.message);
//                 } else {
//                     reject(new Error('Item not found'));
//                 }
//             }
//         });
//     });
// }



///////////////////////////////////////////////////////////


// const itemCache = new LRUCache(500); // Limit the cache size to 500 items
// let lastScannedItem = null; // Track the last scanned item

// frappe.ui.form.on('Sales Invoice', {

//     onload(frm) {
//         // Set page length to show all items
//         frappe.db.get_single_value('SPMS Settings', 'max_child_table_rows')
//             .then(max_rows => {
//                 frm.get_field("items").grid.grid_pagination.page_length = max_rows || 50;
//             });
//     },
//     refresh(frm) {
//         frappe.require([
//             'assets/spms/node_modules/onscan.js/onscan.js',
//         ], () => {
//             // Enable scan events for the entire document
//             onScan.attachTo(document);
//             document.addEventListener('scan', async (event) => {
//                 const { scanCode: sScanned, qty: iQty } = event.detail;
//                 await handleBarcodeScan(sScanned, iQty, frm);
//             });
//         });
//     },
// });

// async function handleBarcodeScan(sScanned, iQty, frm) {
//     const existingItem = frm.doc.items.find(item => item.custom_barcode_label == sScanned);
//     if (existingItem) {
//         existingItem.qty += 1;
//         await updateItem(existingItem, frm);
//     } else {
//         let respItem = itemCache.get(sScanned);
//         if (!respItem) {
//             respItem = await searchItemByBarcode(sScanned);
//             if (respItem) {
//                 itemCache.set(sScanned, respItem);
//             }
//         }

//         if (respItem) {
//             const row = frm.add_child('items', {
//                 custom_barcode_label: sScanned,
//                 item_code: respItem.parent,
//                 item_name: respItem.parent,
//                 description: respItem.parent,
//                 qty: iQty,
//                 uom: respItem.uom
//             });
//             await updateItem(row, frm);
//         }
//     }
// }

// // Function to update item in the table
// function updateItem(item, frm) {
//     frm.script_manager.trigger('item_code', item.doctype, item.name);
//     frm.refresh_field("items");

//     if (lastScannedItem !== item.custom_barcode_label) {
//         const pageLength = frm.get_field("items").grid.grid_pagination.page_length;
//         const pageIndex = Math.floor(item.idx / pageLength);

//         frm.get_field("items").grid.grid_pagination.go_to_page(pageIndex + 1);

//         setTimeout(() => {
//             const element = document.querySelector(`[data-name="${item.name}"]`);
//             if (element) {
//                 element.focus();
//                 element.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
//                 element.style.border = '1px solid blue';
//                 element.style.backgroundColor = 'lightyellow';

//                 setTimeout(() => {
//                     element.style.border = 'none';
//                     element.style.backgroundColor = 'transparent';
//                 }, 5000);
//             } else {
//                 console.log('Element with data-name attribute not found');
//             }
//         }, 300);

//         lastScannedItem = item.custom_barcode_label;
//     }
// }

// // Function to search item by barcode
// function searchItemByBarcode(barcode) {
//     return new Promise((resolve, reject) => {
//         frappe.call({
//             method: 'spms.methods.utils.search_item_by_barcode',
//             args: { barcode, parent_doc: "Item" },
//             callback(r) {
//                 if (r.message) {
//                     resolve(r.message);
//                 } else {
//                     reject(new Error('Item not found'));
//                 }
//             }
//         });
//     });
// }


//////////////////////////////////////////////////////////////////////////////////////
class LRUCache {
    constructor(limit = 100, cacheName = 'lru-cache') {
        this.cache = new Map();
        this.limit = limit;
        this.cacheName = cacheName;
        this.init();
    }

    async init() {
        this.cacheStorage = await caches.open(this.cacheName);
        const keys = await this.cacheStorage.keys();
        for (const request of keys) {
            const response = await this.cacheStorage.match(request);
            if (response) {
                const value = await response.json();
                this.cache.set(request.url, value);
                if (this.cache.size >= this.limit) {
                    break;
                }
            }
        }
    }

    async get(key) {
        if (this.cache.has(key)) {
            const value = this.cache.get(key);
            // Move the accessed key to the end to show it is recently used
            this.cache.delete(key);
            this.cache.set(key, value);
            return value;
        }

        const request = new Request(key);
        const response = await this.cacheStorage.match(request);
        if (response) {
            const value = await response.json();
            this.set(key, value); // Update in-memory cache
            return value;
        }

        return null;
    }

    async set(key, value) {
        if (this.cache.has(key)) {
            this.cache.delete(key);
        } else if (this.cache.size >= this.limit) {
            const firstKey = this.cache.keys().next().value;
            this.cache.delete(firstKey);
            await this.cacheStorage.delete(new Request(firstKey));
        }

        this.cache.set(key, value);

        const response = new Response(JSON.stringify(value));
        await this.cacheStorage.put(new Request(key), response);
    }
}


const itemCache = new LRUCache(500, 'item-cache'); // Limit the cache size to 500 items
let lastScannedItem = null; // Track the last scanned item

frappe.ui.form.on('Sales Invoice', {
    onload(frm) {
        // Set page length to show all items
        frappe.db.get_single_value('SPMS Settings', 'max_child_table_rows')
            .then(max_rows => {
                frm.get_field("items").grid.grid_pagination.page_length = max_rows || 50;
            });

        // Preload the first 300 items into the cache
        frappe.call({
            method: 'spms.methods.utils.get_initial_item_barcodes',
            args: { limit: 500 },
            callback(r) {
                if (r.message) {
                    r.message.forEach(item => {
                        itemCache.set(item.barcode, item);
                    });
                }
            }
        });
    },
    refresh(frm) {
        frappe.require([
            'assets/spms/node_modules/onscan.js/onscan.js',
        ], () => {
            // Enable scan events for the entire document
            onScan.attachTo(document);9
            
            document.addEventListener('scan', async (event) => {
                const { scanCode: sScanned, qty: iQty } = event.detail;
                await handleBarcodeScan(sScanned, iQty, frm);
            });
        });
    },
});

async function handleBarcodeScan(sScanned, iQty, frm) {
    const existingItem = frm.doc.items.find(item => item.custom_barcode_label == sScanned);
    if (existingItem) {
        existingItem.qty += 1;
        await updateItem(existingItem, frm);
    } else {
        let respItem = await itemCache.get(sScanned);
        if (!respItem) {
            respItem = await searchItemByBarcode(sScanned);
            if (respItem) {
                await itemCache.set(sScanned, respItem);
            }
        }

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
    }
}

// Function to update item in the table
function updateItem(item, frm) {
    frm.script_manager.trigger('item_code', item.doctype, item.name);
    frm.refresh_field("items");

    if (lastScannedItem !== item.custom_barcode_label) {
        const pageLength = frm.get_field("items").grid.grid_pagination.page_length;
        const pageIndex = Math.floor(item.idx / pageLength);

        frm.get_field("items").grid.grid_pagination.go_to_page(pageIndex + 1);

        setTimeout(() => {
            const element = document.querySelector(`[data-name="${item.name}"]`);
            if (element) {
                element.focus();
                element.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
                element.style.border = '1px solid blue';
                element.style.backgroundColor = 'lightyellow';

                setTimeout(() => {
                    element.style.border = 'none';
                    element.style.backgroundColor = 'transparent';
                }, 5000);
            } else {
                console.log('Element with data-name attribute not found');
            }
        }, 300);

        lastScannedItem = item.custom_barcode_label;
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
