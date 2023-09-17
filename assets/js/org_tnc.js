const form = document.forms['org_details_form'];
const elements = form.elements;

for (let i = 0; i < elements.length; i++) {
  elements[i].disabled = true;
}

function edit_organization_form() {
    const form = document.forms['org_details_form'];
    const elements = form.elements;

    for (let i = 0; i < elements.length; i++) {
    elements[i].disabled = false;
    }
}
