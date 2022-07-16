document.getElementById('id_company_name').disabled = true;
document.getElementById('id_manager_name').disabled = true;
document.getElementById('id_email').disabled = true;
document.getElementById('id_phoneNumber').disabled = true;
document.getElementById('id_address_1').disabled = true;
document.getElementById('id_address_2').disabled = true;
document.getElementById('id_landmark').disabled = true;
document.getElementById('id_town_city').disabled = true
document.getElementById('id_zip_code').disabled = true;
document.getElementById('id_state').disabled = true;
document.getElementById('save_organization_details').disabled = true;


function edit_organization_form() {
    document.getElementById('id_company_name').disabled = false;
    document.getElementById('id_manager_name').disabled = false;
    document.getElementById('id_email').disabled = false;
    document.getElementById('id_phoneNumber').disabled = false;
    document.getElementById('id_address_1').disabled = false;
    document.getElementById('id_address_2').disabled = false;
    document.getElementById('id_landmark').disabled = false;
    document.getElementById('id_town_city').disabled = false;
    document.getElementById('id_zip_code').disabled = false;
    document.getElementById('id_state').disabled = false;
    document.getElementById('save_organization_details').disabled = false;
}
