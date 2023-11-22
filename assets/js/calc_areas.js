console.log("cal_areas.js loaded");
$(document).ready(function () {
    
    // initial area and amount calculation
    areas();
    calculateAmount();

    // calculate area and amount on change of length and width 
    $('#id_length_feet, #id_length_inches, #id_width_feet, #id_width_inches').on('input',function () {
        areas();
    });

    $('#id_rate').on('input',function () {
        calculateAmount();
    });
});

function calculateAmount() {
    var rt = parseFloat(document.getElementById("id_rate").value);
    if (isNaN(rt)) { rt = 0; }
    var amount = document.getElementById("id_sqft").value * rt
    document.getElementById("amount").value = amount;
}

function areas() {
    // Find area of the lengths provided.
    var len_feet = parseFloat(document.getElementById("id_length_feet").value);
    var len_inches = parseFloat(document.getElementById("id_length_inches").value);
    var wid_feet = parseFloat(document.getElementById("id_width_feet").value);
    var wid_inches = parseFloat(document.getElementById("id_width_inches").value);

    var is_running_feet = false;

    if (isNaN(len_feet)) { len_feet = 0; }
    if (isNaN(len_inches)) { len_inches = 0; }
    if (isNaN(wid_feet) || wid_feet == 0){ wid_feet = 0; } 
    if(isNaN(wid_inches) || wid_inches == 0) { wid_inches = 0; }

    if (wid_feet == 0 && wid_inches == 0) {is_running_feet = true;}
    
    if (is_running_feet) {
        var running_sqft = (len_feet + (len_inches / 12));
        var running_mtr = running_sqft / 10.7639104;
        document.getElementById("id_sqft").value = running_sqft.toFixed(4);
        document.getElementById("id_sqm").value = running_mtr.toFixed(4);
    }
    else {
        var sqft = (len_feet + (len_inches / 12)) * (wid_feet + (wid_inches / 12));
        var sqmtr = sqft / 10.7639104;
        document.getElementById("id_sqft").value = sqft.toFixed(4);
        document.getElementById("id_sqm").value = sqmtr.toFixed(4);
    }
    
    calculateAmount();
}
