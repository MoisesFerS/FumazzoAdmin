document.querySelector('.notifications-accordion-container').addEventListener('click', function(event) {
  if (event.target.closest('.notification-sector-accordion')) {
    let sectorAccordion = event.target.closest('.notification-sector-accordion');
    expand(sectorAccordion);
  }

  if (event.target.closest('.notification-accordion')) {
    let notificationAccordion = event.target.closest('.notification-accordion');
    expand(notificationAccordion);
    updateAllParentPanels(notificationAccordion);
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
  let parentPanel = element.closest('.notification-sector-accordion-panel, .notification-accordion-panel');
  
  if (parentPanel) {
    setTimeout(() => {
      parentPanel.style.display = 'block';
      let scrollHeight = parentPanel.scrollHeight;
      parentPanel.style.display = '';
      parentPanel.style.maxHeight = scrollHeight + "px";

      let parentAccordion = parentPanel.previousElementSibling;
      if (parentAccordion && (
          parentAccordion.classList.contains('notification-sector-accordion') ||
          parentAccordion.classList.contains('notification-accordion'))) {
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
      const form = modal.querySelector(`[name="notification-${button.name}-form"]`)
      form.id = button.id

      window.addEventListener('click', function(event) {
        if (event.target === modal) {
          modal.style.display = "none";
        }
      });

    });
  });

document.querySelector("[name='notification-add-form']").addEventListener('submit', async function(event){
  event.preventDefault();

  var formData = new FormData();
  formData.append('message', document.querySelector('#notification-add-message').value);
  formData.append('sender', this.id)

  let sectorID = document.querySelector('#notification-add-sector').value
  formData.append('sector', sectorID ? sectorID : null);

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

document.querySelector("[name='notification-edit-form']").addEventListener('submit', async function(event){
  event.preventDefault();

  var formData = new FormData();
  formData.append('notificationID', this.id)
  formData.append('message', document.querySelector('#notification-edit-message').value);
  formData.append('sector', document.querySelector('#notification-edit-sector').value);

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

document.querySelector("[name='notification-remove-form']").addEventListener('submit', async function(event){
  event.preventDefault();

  var formData = new FormData();
  formData.append('notification', this.id)

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

document.querySelectorAll('.notification-button.edit').forEach(button => {
  button.addEventListener('click', async function(){

    var formData = new FormData();
    formData.append('notification', this.id)

    let csrfToken = getToken();

    await fetch(`data/`, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken },
      body: formData,
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        let info = ['message', 'sector']

        info.forEach(input => {
          let editInfo = document.querySelector(`#notification-edit-${input}`)
          editInfo.value = data.notificationData[input]
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