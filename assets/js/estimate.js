console.log("estimate.js loaded");

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

document.getElementById('forQuantity').disabled = true;

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