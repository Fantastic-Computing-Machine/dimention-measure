const form = document.forms['org_details_form'];
const elements = form.elements;

for (const element of elements) {
  element.disabled = true;
}

function enableOrganizationForm() {
  const form = document.forms['org_details_form'];
  const elements = form.elements;

  for (const element of elements) {
    element.disabled = false;
  }
}
