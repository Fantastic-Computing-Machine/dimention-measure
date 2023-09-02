console.log("cal_areas.js loaded");

var length_feet = document.getElementById("id_length_feet");
var length_inches = document.getElementById("id_length_inches");

var width_feet = document.getElementById("id_width_feet");
var width_inches = document.getElementById("id_width_inches");

var rate = document.getElementById("id_rate");

function calculateAmount() {
    var rt = parseFloat(rate.value);

    if (isNaN(rt)) { rt = 0; }
    var amount = document.getElementById("sqft").value * rt
    document.getElementById("amount").value = amount;
}



// jquery to check if #id_length_feet','#id_length_inches' are both filled then enable the new_dimension button
$(document).ready(function () {
    $('#id_length_feet, #id_length_inches').keyup(function () {
        if ($('#id_length_feet').val().length != 0 || $('#id_length_inches').val().length != 0) {
            $('#add_new_dimension').prop('disabled', false);
        } else {
            $('#add_new_dimension').prop('disabled', true);
        }
    });
});



function areas() {
    // Find area of the lengths provided.
    var len_feet = parseFloat(length_feet.value);
    var len_inches = parseFloat(length_inches.value);
    var wid_feet = parseFloat(width_feet.value);
    var wid_inches = parseFloat(width_inches.value);
    // var wid = parseFloat(width.value);
    // var rt = parseFloat(rate.value);
    var flag = false;

    if (isNaN(len_feet)) { len_feet = 0; }
    if (isNaN(len_inches)) { len_inches = 0; }
    if (isNaN(wid_feet)) { wid_feet = 1; flag = true; }
    if (isNaN(wid_inches)) { wid_inches = 1; flag = true; }
    // if (isNaN(wid)) { wid = 1; flag = true; }

    var sqft = (len_feet + (len_inches / 12)) * (wid_feet + (wid_inches / 12));
    document.getElementById("sqft").value = sqft.toFixed(4);

    var sqmtr = sqft / 10.7639104;
    document.getElementById("sqm").value = sqmtr.toFixed(4);
    calculateAmount()
}