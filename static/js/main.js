var length = document.getElementById("length");
var width = document.getElementById("width");
var rate = document.getElementById("rate");


function areas() {
    var first_number = parseFloat(length.value);
    if (isNaN(first_number)) { first_number = 0; }

    var second_number = parseFloat(width.value);
    if (isNaN(second_number)) { second_number = 0; }

    var third_number = parseFloat(rate.value);
    if (isNaN(third_number)) { third_number = 0; }

    var sqmtr = first_number * second_number;
    document.getElementById("sqm").value = sqmtr;

    var sqfeet = first_number * second_number * 10.764;
    document.getElementById("sqft").value = sqfeet;

    var amount = sqfeet * third_number
    document.getElementById("amount").value = amount;
}

var meter = document.getElementById("mt");
var feet = document.getElementById("ft");

function mtr_ft() {
    var first_number = parseFloat(meter.value);
    if (isNaN(first_number)) { first_number = 0; }

    var to_ft = first_number * 3.28;
    document.getElementById("ft").value = to_ft;
}

function ft_mtr() {
    var first_number = parseFloat(feet.value);
    if (isNaN(first_number)) { first_number = 0; }

    var to_mt = first_number * 0.3048;
    document.getElementById("mt").value = to_mt;
}