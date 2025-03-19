document.querySelector('.tickets-accordion-container').addEventListener('click', function(event) {
  if (event.target.closest('.ticket-type-accordion')) {
    let typeAccordion = event.target.closest('.ticket-type-accordion');
    expand(typeAccordion);
  }

  if (event.target.closest('.ticket-ticket-accordion')) {
    let ticketAccordion = event.target.closest('.ticket-ticket-accordion');
    expand(ticketAccordion);
    updateAllParentPanels(ticketAccordion);
  }

  if (event.target.closest('.ticket-accordion')) {
    let ticketAccordion = event.target.closest('.ticket-accordion');
    expand(ticketAccordion);
    updateAllParentPanels(ticketAccordion);
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
  let parentPanel = element.closest('.ticket-type-accordion-panel, .ticket-ticket-accordion-panel, .ticket-accordion-panel');

  if (parentPanel) {
    setTimeout(() => {
      parentPanel.style.display = 'block';
      let scrollHeight = parentPanel.scrollHeight;
      parentPanel.style.display = '';
      parentPanel.style.maxHeight = scrollHeight + "px";

      let parentAccordion = parentPanel.previousElementSibling;
      if (parentAccordion && (
        parentAccordion.classList.contains('ticket-type-accordion') ||
        parentAccordion.classList.contains('ticket-ticket-accordion') ||
        parentAccordion.classList.contains('ticket-accordion'))) {
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
    const form = modal.querySelector(`[name="ticket-${button.name}-form"]`)
    form.id = button.id

    window.addEventListener('click', function(event) {
      if (event.target === modal) {
        modal.style.display = "none";
      }
    });

  });
});

document.querySelector("[name='ticket-add-form']").addEventListener('submit', async function(event){
  event.preventDefault();

  var formData = new FormData();
  formData.append('sector', document.querySelector('#ticket-add-sector').value);
  formData.append('reason', document.querySelector('#ticket-add-reason').value);
  formData.append('priority', document.querySelector('#ticket-add-priority').value);
  formData.append('category', document.querySelector('#ticket-add-category').value);
  formData.append('description', document.querySelector('#ticket-add-description').value);

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

document.querySelector("[name='ticket-remove-form']").addEventListener('submit', async function(event){
  event.preventDefault();

  var formData = new FormData();
  formData.append('ticket', this.id)

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

document.querySelectorAll('.ticket-status-select')
  .forEach(select =>{
    select.addEventListener('change', async function(){

    var formData = new FormData();
    formData.append('ticket', select.value);
    formData.append('status', document.querySelector('.ticket-status-select').value);

    let csrfToken = getToken(); 

    await fetch(`status/`, {
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
});