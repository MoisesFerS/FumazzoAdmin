document.querySelector('.suppliers-accordion-container').addEventListener('click', function(event) {
  if (event.target.closest('.supplier-type-accordion')) {
    let typeAccordion = event.target.closest('.supplier-type-accordion');
    expand(typeAccordion);
  }

  if (event.target.closest('.supplier-supplier-accordion')) {
    let supplierAccordion = event.target.closest('.supplier-supplier-accordion');
    expand(supplierAccordion);
    updateAllParentPanels(supplierAccordion);
  }

  if (event.target.closest('.supplier-accordion')) {
    let supplierAccordion = event.target.closest('.supplier-accordion');
    expand(supplierAccordion);
    updateAllParentPanels(supplierAccordion);
  }
});

function expand(accordion) {
  accordion.classList.toggle('active');
  let panel = accordion.nextElementSibling;

  panel.style.display = 'block';
  let scrollHeight = panel.scrollHeight;
  panel.style.display = ''; 

  if (panel.style.maxHeight) {
    panel.style.maxHeight = null; 
  } else {
    panel.style.maxHeight = scrollHeight + "px"; 
  }
}

function updateAllParentPanels(element) {
  let parentPanel = element.closest('.supplier-type-accordion-panel, .supplier-supplier-accordion-panel, .supplier-accordion-panel');
  
  if (parentPanel) {
    setTimeout(() => {
      parentPanel.style.display = 'block';
      let scrollHeight = parentPanel.scrollHeight;
      parentPanel.style.display = '';
      parentPanel.style.maxHeight = scrollHeight + "px";

      let parentAccordion = parentPanel.previousElementSibling;
      if (parentAccordion && (
          parentAccordion.classList.contains('supplier-type-accordion') ||
          parentAccordion.classList.contains('supplier-supplier-accordion') ||
          parentAccordion.classList.contains('supplier-accordion'))) {
        updateAllParentPanels(parentAccordion);
      }
    }, 250);
  }
}

/*  ============================================================
    MODALS - Modals functions   
    ============================================================ */ 

/* Function to open the modals dynamically */
document.querySelectorAll("[name='add'], [name='edit'], [name='remove']")
  .forEach(button => {
    button.addEventListener('click', function (event) {
        
      const modal = document.getElementById(`modal-${button.name}`);
      modal.style.display = 'block';
      const form = modal.querySelector(`[name="supplier-${button.name}-form"]`)
      form.id = button.id

      window.addEventListener('click', function(event) {
        if (event.target === modal) {
          modal.style.display = "none";
        }
      });

    });
  });

document.querySelector("[name='supplier-add-form']").addEventListener('submit', async function(event){
  event.preventDefault();

  var formData = new FormData();
  formData.append('phone', document.querySelector('#supplier-add-phone').value);
  formData.append('name', document.querySelector('#supplier-add-name').value);
  formData.append('address', document.querySelector('#supplier-add-address').value);
  formData.append('email', document.querySelector('#supplier-add-email').value);

  let csrfToken = getToken(); 

  await fetch(`add/`, {
    method: 'POST',
    headers: { 'X-CSRFToken': csrfToken }, 
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if(data.status == 'success'){
      location.reload(); 
    } else {          
      message.style.display = 'block';        
      message.querySelector('#message-text').innerHTML = data.message; 
      message.querySelector('#message-error').innerHTML = data.error;
      setTimeout(() => {
        message.style.display = 'none'; 
      }, 3000);
    }
  }); 
});

document.querySelector("[name='supplier-edit-form']").addEventListener('submit', async function(event){
  event.preventDefault();

  var formData = new FormData();
  formData.append('supplierID', this.id)
  formData.append('name', document.querySelector('#supplier-edit-name').value);
  formData.append('address', document.querySelector('#supplier-edit-address').value);
  formData.append('phone', document.querySelector('#supplier-edit-phone').value);
  formData.append('email', document.querySelector('#supplier-edit-email').value);

  let csrfToken = getToken(); 

  await fetch(`edit/`, {
    method: 'POST',
    headers: { 'X-CSRFToken': csrfToken }, 
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if(data.status == 'success'){
      location.reload(); 
    } else {          
      message.style.display = 'block';        
      message.querySelector('#message-text').innerHTML = data.message; 
      message.querySelector('#message-error').innerHTML = data.error;
      setTimeout(() => {
        message.style.display = 'none'; 
      }, 3000);
    }
  }); 
});

document.querySelector("[name='supplier-remove-form']").addEventListener('submit', async function(event){
  event.preventDefault();

  var formData = new FormData();
  formData.append('supplier', this.id)

  let csrfToken = getToken(); 
  
  await fetch(`remove/`, {
    method: 'POST',
    headers: { 'X-CSRFToken': csrfToken }, 
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if(data.status == 'success'){
      location.reload(); 
    } else {          
      message.style.display = 'block';        
      message.querySelector('#message-text').innerHTML = data.message; 
      message.querySelector('#message-error').innerHTML = data.error;
      setTimeout(() => {
        message.style.display = 'none'; 
      }, 3000);
    }
  }); 

});

document.querySelectorAll('.supplier-button.edit').forEach(button => {
  button.addEventListener('click', async function(){

    var formData = new FormData();
    formData.append('supplier', this.id)

    let csrfToken = getToken();

    await fetch(`data/`, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken },
      body: formData,
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        let info = ['name', 'phone', 'email', 'address']

        info.forEach(input => {
          let editInfo = document.querySelector(`#supplier-edit-${input}`)
          editInfo.value = data.supplierData[input]
        });

      } else {
        message.style.display = 'block';
        message.querySelector('#message-text').innerHTML = data.message;
        message.querySelector('#message-error').innerHTML = data.error;
        setTimeout(() => {
          message.style.display = 'none';
        }, 3000);
      }      
    });
  });
});