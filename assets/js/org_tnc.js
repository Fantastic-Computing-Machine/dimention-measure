const form = document.forms['org_details_form'];
const elements = form.elements;

function enableOrganizationForm() {
//   const form = document.forms['org_details_form'];
//   const elements = form.elements;
  for (const element of elements) {
    element.disabled = false;
  }
}

if (document.getElementsByName('field_alerts').length > 0) {
    enableOrganizationForm();
}
else {
    for (const element of elements) {
        element.disabled = true;
        }
}

