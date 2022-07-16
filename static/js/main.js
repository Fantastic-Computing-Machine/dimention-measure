console.log("main.js loaded");

var length = document.getElementById("id_length");
var width = document.getElementById("id_width");
var rate = document.getElementById("id_rate");

function calculateAmount() {
    var rt = parseFloat(rate.value);

    if (isNaN(rt)) { rt = 0; }
    var amount = document.getElementById("sqft").value * rt
    document.getElementById("amount").value = amount;
}

function areas() {
    // Find area of the lengths provided.
    var len = parseFloat(length.value);
    var wid = parseFloat(width.value);
    // var rt = parseFloat(rate.value);
    var flag = false;

    if (isNaN(len)) { len = 0; }
    if (isNaN(wid)) { wid = 1; flag = true; }
    // if (isNaN(rt)) { rt = 0; }

    var sqmtr = len * wid;
    document.getElementById("sqm").value = sqmtr;

    if (flag == true) {
        var sqfeet = len * wid * 3.28;
        document.getElementById("sqft").value = sqfeet;

        // var amount = sqfeet * rt
        // document.getElementById("amount").value = amount;

        document.getElementById("sqm").value = 0.0;
        // <!-- if you change "N/A" here then change the value in records.html file also -->
        document.getElementById("sqft").value = 0.0;
    } else {
        var sqfeet = len * wid * 10.764;
        document.getElementById("sqft").value = sqfeet;

        // var amount = sqfeet * rt
        // document.getElementById("amount").value = amount;
    }

    // calculateAmount()
}

var meter = document.getElementById("mt");
var feet = document.getElementById("ft");

function mtr_ft() {
    // Unit conversion meter to feet
    var len = parseFloat(meter.value);
    if (isNaN(len)) { len = 0; }

    var to_ft = len * 3.28;
    document.getElementById("ft").value = to_ft;
}

function ft_mtr() {
    // Unit conversion feet to meter
    var len = parseFloat(feet.value);
    if (isNaN(len)) { len = 0; }

    var to_mt = len * 0.3048;
    document.getElementById("mt").value = to_mt;
}

$(document).ready(function () {
    $(".delete_button").hover(function () {
        $(this).children('img').attr('src', 'https://img.icons8.com/ios/50/000000/delete-forever--v2.gif');

    }, function () {
        $(this).children('img').attr("src", "https://img.icons8.com/ios/50/000000/delete-forever--v2.png");


    });
});

$(document).ready(function () {
    $(".setting").hover(function () {
        $(this).children('img').attr('src', 'https://img.icons8.com/ios/28/000000/settings--v2.gif');

    }, function () {
        $(this).children('img').attr("src", "https://img.icons8.com/ios/28/000000/settings--v2.png");


    });
});

// Dynamically change the year in the footer
document.getElementById("current_year").innerHTML = new Date().getFullYear();


function area_enable() {
    document.getElementById('id_length').disabled = false;
    document.getElementById('id_length').required = true;

    document.getElementById('id_width').disabled = false;

    document.getElementById('forQuantity').disabled = true;
    document.getElementById('forQuantity').value = '';

    document.getElementById('sqm').hidden = false;
    document.getElementById('sqft').hidden = false;

    document.getElementById('sqm_box').hidden = false;
    document.getElementById('sqft_box').hidden = false;

    document.getElementById('quantityBox').hidden = '';
}


function quantity_enable() {
    document.getElementById('id_length').value = '';
    document.getElementById('id_length').disabled = true;

    document.getElementById('id_width').value = '';
    document.getElementById('id_width').disabled = true;

    document.getElementById('sqm').value = '';
    document.getElementById('sqm').hidden = true;
    document.getElementById('sqm_box').hidden = true;
    document.getElementById('forQuantity').required = true;

    document.getElementById('sqft').value = '';
    document.getElementById('sqft').hidden = true;
    document.getElementById('sqft_box').hidden = true;

    document.getElementById('areaBox').hidden = '';

    document.getElementById('forQuantity').disabled = false;
}

$(document).ready(function () {
    $("#id_discount").on('input', function () {
        if ($(this).val() < 0 || $(this).val() > 100) {
            $('#DiscountError').prop('hidden', false);
            $('#discountChangeSubmit').prop('disabled', true);
        }
        else {
            $('#DiscountError').prop('hidden', true);
            $('#discountChangeSubmit').prop('disabled', false);
        }
    });
});

// $(document).ready(function(){
//     check();
//     });

//     function check() {
//         var Q1 = $("#flexRadioDefault1").val();
//         var Q2 = $("#flexRadioDefault2").val();

//         // window.print(Q1);
//         // window.print(Q2);
//     }


// function edit_organization_form() {
//     console.log("Admin method");
//     document.getElementById('id_company_name').disabled = false;
//     document.getElementById('id_manager_name').disabled = false;
//     document.getElementById('id_email').disabled = false;
//     document.getElementById('id_phoneNumber').disabled = false;
//     document.getElementById('id_address_1').disabled = false;
//     document.getElementById('id_address_2').disabled = false;
//     document.getElementById('id_landmark').disabled = false;
//     document.getElementById('id_town_city').disabled = false;
//     document.getElementById('id_zip_code').disabled = false;
//     document.getElementById('id_state').disabled = false;
//     document.getElementById('save_organization_details').disabled = false;
// }