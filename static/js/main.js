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

     calculateAmount()
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

function enableNewitemPage() {
    console.log("enableNewitemPage2");
    document.getElementById('flexRadioDefault1').disabled = false;
    document.getElementById('id_length').disabled = false;
    document.getElementById('id_width').disabled = false;
    document.getElementById('flexRadioDefault2').disabled = false;
    document.getElementById('forQuantity').disabled = false;
    document.getElementById('id_discount').disabled = false;
    document.getElementById('id_rate').disabled = false;
    document.getElementById('id_unit').disabled = false;
    document.getElementById('id_room').disabled = false;
    document.getElementById('id_room_item').disabled = false;
    document.getElementById('id_room_item_description').disabled = false;
}

$(document).ready(function () {
    $("#edit_update_estimate").click(function () {
        var Q1 = $("#forQuantity").val();
        var Q2 = $("#id_length").val();
        var Q3 = $("#id_width").val();
        if (Q1 != undefined && Q1 != "") {
            $('#flexRadioDefault2').prop('checked', true);
            $('#flexRadioDefault1').prop('checked', false);
            $('#flexRadioDefault1').prop('disable', true);
            $('#id_length').prop('disabled', true);
            $('#id_width').prop('disabled', true);
            $('#sqm_box').prop('hidden', true);
            $('#sqft_box').prop('hidden', true);
            // this is comment

        }
        else {
            console.log("for area");
            $('#flexRadioDefault2').prop('disable', true);
            $('#flexRadioDefault1').prop('checked', true);
            $('#flexRadioDefault2').prop('checked', false);
            $('#forQuantity').prop('disabled', true);
        }
    });
});

$(document).ready(function () {
    $('.checkboxSelector').change(function() {
        if ($('.checkboxSelector:checked').length) {
            $('#delete_button').prop('disabled', false);
        } else {
            $('#delete_button').prop('disabled', true);
        }
    });
});

function deleteThisItem(item_id, project_id, item_project_name)
{
    console.log("deleted "+ item_id);
    document.getElementsByName("deleteElementModelForm").getAttribute('action') = "{% url 'delete_estimate_row' "+item_id+" "+project_id+" "+item_project_name+" %}" ;
}