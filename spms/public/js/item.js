frappe.ui.form.on('Item', {
    refresh(frm) {
        frm.add_custom_button('Generate Barcode', () => {
            const ean13Barcode = generate_ean13();
            const child = frm.add_child('barcodes');
            frappe.model.set_value(child.doctype, child.name, 'barcode', ean13Barcode);
            frm.refresh_field('barcodes');
        });

        frm.add_custom_button('Print Barcode', () => {
            // Get the barcodes from the child table
            var barcodes = frm.doc.barcodes || [];

            // Create HTML content for barcode buttons
            var dialogContent = '<div id="barcode-buttons">';
            barcodes.forEach(function (barcode) {
                dialogContent += '<button class="barcode-button btn btn-primary" data-barcode="' + barcode.barcode + '">' + barcode.barcode + '</button>';
            });
            dialogContent += '</div>';

            // Create the dialog
            var dialog = new frappe.ui.Dialog({
                title: 'Print Barcode',
                fields: [
                    {
                        fieldname: 'barcode_buttons',
                        label: 'Select Barcode',
                        fieldtype: 'HTML',
                        options: dialogContent
                    }
                ],
                primary_action_label: 'Print',
                primary_action: function () {
                    // Get the selected barcode
                    var selectedButton = dialog.get_field('barcode_buttons').$wrapper.find('.barcode-button.active');
                    var selectedBarcode = selectedButton ? selectedButton.attr('data-barcode') : null;

                    if (selectedBarcode) {
                        // Get the current site URL
                        frappe.call({
                            method: 'spms.methods.utils.get_base_url',
                            callback: function (response) {
                                var baseUrl = response.message;

                                // Generate the URL parameters
                                var doctype = 'Item';
                                var name = frm.doc.name;
                                var format = 'Barcode 35mm x 15mm';
                                var no_letterhead = '1';
                                var letterhead = 'No Letterhead';
                                var settings = '{}';
                                var _lang = 'en';
                                var barcode = selectedBarcode;

                                // Generate the complete URL
                                var url = baseUrl + '/printview?' +
                                    'doctype=' + encodeURIComponent(doctype) +
                                    '&name=' + encodeURIComponent(name) +
                                    '&format=' + encodeURIComponent(format) +
                                    '&no_letterhead=' + encodeURIComponent(no_letterhead) +
                                    '&letterhead=' + encodeURIComponent(letterhead) +
                                    '&settings=' + encodeURIComponent(settings) +
                                    '&_lang=' + encodeURIComponent(_lang) +
                                    '&barcode=' + encodeURIComponent(barcode);

                                // Open the URL in a new window
                                window.open(url, '_blank');
                            }
                        });
                    }

                    // Close the dialog
                    dialog.hide();
                }
            });

            // Show the dialog
            dialog.show();

            // Add click event listener to barcode buttons
            dialog.$wrapper.find('.barcode-button').on('click', function () {
                // Remove active class from all buttons
                dialog.$wrapper.find('.barcode-button').removeClass('active');
                // Add active class to the clicked button
                $(this).addClass('active');
                // Add primary class to the clicked button
                $(this).addClass('btn-primary');
            });

            // Add margin between barcode buttons
            dialog.$wrapper.find('.barcode-button').css('margin-right', '5px');
        });

    }
});

function generate_ean13() {
    let productCode = Math.floor(Math.random() * 1000000000).toString().padStart(9, '0');
    let barcode = productCode;
    return barcode + calculate_check_digit(barcode);
}

function calculate_check_digit(barcode) {
    const digits = barcode.split('').map(Number);
    let evenSum = 0, oddSum = 0;

    digits.forEach((digit, index) => {
        if (index % 2 === 0) {
            oddSum += digit;
        } else {
            evenSum += digit;
        }
    });

    const totalSum = oddSum * 3 + evenSum;
    const nextTen = Math.ceil(totalSum / 10) * 10;
    const checkDigit = nextTen - totalSum;
    return checkDigit;
}
