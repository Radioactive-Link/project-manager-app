/**
 * Used to create dynamic forms for the one to many relationships.
 */
function initDynamicFormset(config) {
    const {
        addBtnId,
        formsetId,
        totalFormsId,
        templateId,
        formClass,
        deleteBtnClass
    } = config;

    const addBtn = document.getElementById(addBtnId);
    const formsetDiv = document.getElementById(formsetId);
    const totalForms = document.getElementById(totalFormsId);
    const template = document.getElementById(templateId).innerHTML;

    // add form
    addBtn.addEventListener('click', () => {
        const formIndex = parseInt(totalForms.value);
        const newFormHtml = template.replace(/__prefix__/g, formIndex);

        const wrapper = document.createElement("div");
        wrapper.innerHTML = newFormHtml;

        formsetDiv.appendChild(wrapper.firstElementChild);

        totalForms.value = formIndex + 1;
    });

    // delete form
    document.addEventListener("click", function(e) {
        if (e.target.classList.contains(deleteBtnClass)) {
            const formDiv = e.target.closest(`.${formClass}`);
            const deleteInput = formDiv.querySelector("input[type='checkbox'][name$='-DELETE']");

            if (deleteInput) {
                deleteInput.checked = true;
                formDiv.style.display = "none";
            } else {
                formDiv.remove();
            }
        }
    });
}