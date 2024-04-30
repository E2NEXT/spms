/*----------------------
 | Payment Entry Handlers
 -----------------------*/

// Event handler for total_paid field
/*----------------------
 | total_paid
 | Author: Osama Muhammed Abd | E2NEXT
 | Description: Handles changes in the total_paid field.
 | Dependencies: custom_total_paid, discount_percentage, paid_amount
 ----------------------*/
 frappe.ui.form.on('Payment Entry', {
    total_paid(frm) {
        // Check if total_paid is greater than 0
        if (frm.doc.total_paid > 0) {
            // If discount_percentage is not provided
            if (!frm.doc.discount_percentage) {
                // Set paid_amount to custom_total_paid
                frm.set_value("paid_amount", frm.doc.custom_total_paid);
            } else {
                // Calculate paid_amount based on discount_percentage
                var total = frm.doc.custom_total_paid * (1 - (frm.doc.discount_percentage / 100));
                frm.set_value("paid_amount", total);
            }
        }
    },
});

// Event handler for custom_discount_percentage field
/*----------------------
 | custom_discount_percentage
 | Author: Osama Muhammed Abd | E2NEXT
 | Description: Handles changes in the custom_discount_percentage field.
 | Dependencies: custom_total_paid, custom_discount_percentage, custom_discount_amount, paid_amount
 ----------------------*/
frappe.ui.form.on('Payment Entry', {
    custom_discount_percentage(frm) {
        // Check if custom_discount_percentage is greater than 0
        if (frm.doc.custom_discount_percentage > 0) {
            // Calculate custom_discount_amount
            frm.set_value("custom_discount_amount", frm.doc.custom_total_paid * (frm.doc.custom_discount_percentage / 100));
            // Calculate paid_amount based on custom_discount_percentage
            var total = frm.doc.custom_total_paid * (1 - (frm.doc.custom_discount_percentage / 100));
            frm.set_value("paid_amount", total);
        }
    },
});

// Event handler for custom_discount_amount field
/*----------------------
 | custom_discount_amount
 | Author: Osama Muhammed Abd | E2NEXT
 | Description: Handles changes in the custom_discount_amount field.
 | Dependencies: custom_total_paid, custom_discount_amount, paid_amount
 ----------------------*/
frappe.ui.form.on('Payment Entry', {
    custom_discount_amount(frm) {
        // Check if custom_discount_amount is greater than 0
        if (frm.doc.custom_discount_amount > 0) {
            // Calculate custom_discount_percentage
            frm.set_value("custom_discount_percentage", (frm.doc.custom_discount_amount / frm.doc.custom_total_paid) * 100);
            // Calculate paid_amount based on custom_discount_amount
            var total = frm.doc.custom_total_paid - frm.doc.custom_discount_amount;
            frm.set_value("paid_amount", total);
        }
    },
});
