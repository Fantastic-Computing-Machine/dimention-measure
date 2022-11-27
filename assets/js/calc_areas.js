console.log("dimension.js loaded");

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