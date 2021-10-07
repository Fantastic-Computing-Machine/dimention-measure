var length = document.getElementById("length");
var width = document.getElementById("width");
var rate = document.getElementById("rate");


function areas() {
    var len = parseFloat(length.value);
    var wid = parseFloat(width.value);
    var rt = parseFloat(rate.value);
    var flag = false;

    if (isNaN(len)) { len = 0; }
    if (isNaN(wid)) { wid = 1; flag = true; }
    if (isNaN(rt)) { rt = 0; }

    var sqmtr = len * wid;
    document.getElementById("sqm").value = sqmtr;

    if (flag == true) {
        var sqfeet = len * wid * 3.28;
        document.getElementById("sqft").value = sqfeet;

        var amount = sqfeet * rt
        document.getElementById("amount").value = amount;

        document.getElementById("sqm").value = 'N/A';
        // <!-- if you change "N/A" here then change the value in records.html file also -->
        document.getElementById("sqft").value = 'N/A';
    } else {
        var sqfeet = len * wid * 10.764;
        document.getElementById("sqft").value = sqfeet;

        var amount = sqfeet * rt
        document.getElementById("amount").value = amount;
    }
}

var update_length = document.getElementById("update_length");
var update_width = document.getElementById("update_width");
var update_rate = document.getElementById("update_rate");

function update_areas() {
    var len = parseFloat(update_length.value);
    var wid = parseFloat(update_width.value);
    var rt = parseFloat(update_rate.value);
    var flag = false;

    if (isNaN(len)) { len = 0; }
    if (isNaN(wid)) { wid = 1; flag = true; }
    if (isNaN(rt)) { rt = 0; }

    var sqmtr = len * wid;
    document.getElementById("update_sqm").value = sqmtr;

    if (flag == true) {
        var sqfeet = len * wid * 3.28;
        document.getElementById("update_sqft").value = sqfeet;

        var amount = sqfeet * rt
        document.getElementById("update_amount").value = amount;

        document.getElementById("update_sqm").value = 'N/A';
        // <!-- if you change "N/A" here then change the value in records.html file also -->
        document.getElementById("update_sqft").value = 'N/A';
    } else {
        var sqfeet = len * wid * 10.764;
        document.getElementById("update_sqft").value = sqfeet;

        var amount = sqfeet * rt
        document.getElementById("update_amount").value = amount;
    }
}


var meter = document.getElementById("mt");
var feet = document.getElementById("ft");

function mtr_ft() {
    var len = parseFloat(meter.value);
    if (isNaN(len)) { len = 0; }

    var to_ft = len * 3.28;
    document.getElementById("ft").value = to_ft;
}

function ft_mtr() {
    var len = parseFloat(feet.value);
    if (isNaN(len)) { len = 0; }

    var to_mt = len * 0.3048;
    document.getElementById("mt").value = to_mt;
}
