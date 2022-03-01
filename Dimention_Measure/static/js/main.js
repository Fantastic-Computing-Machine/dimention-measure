var length = document.getElementById("id_length");
var width = document.getElementById("id_width");
var rate = document.getElementById("id_rate");


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

        document.getElementById("sqm").value = 0.0;
        // <!-- if you change "N/A" here then change the value in records.html file also -->
        document.getElementById("sqft").value = 0.0;
    } else {
        var sqfeet = len * wid * 10.764;
        document.getElementById("sqft").value = sqfeet;

        var amount = sqfeet * rt
        document.getElementById("amount").value = amount;
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
