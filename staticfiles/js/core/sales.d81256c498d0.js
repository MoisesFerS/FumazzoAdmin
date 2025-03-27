/*  ============================================================
    MODALS - Modals functions   
    ============================================================ */ 

/* Function to open the modals dynamically */
document.querySelectorAll("[name='add'], .remove")
  .forEach(button => {
    button.addEventListener('click', function (event) {
      var task = button.name ? 'add' : 'remove'
      const modal = document.getElementById(`modal-${task}`);
      modal.style.display = 'block';
      const form = modal.querySelector(`[name="sale-${task}-form"]`)
      form.id = button.id

      window.addEventListener('click', function(event) {
        if (event.target === modal) {
          modal.style.display = "none";
        }
      });

    });
  });

document.querySelector("[name='sale-add-form']").addEventListener('submit', async function(event){
  event.preventDefault();

  var formData = new FormData();
  formData.append('code', document.querySelector('#sale-add-code').value);
  formData.append('type', document.querySelector('#sale-add-type').value);
  formData.append('discount', document.querySelector('#sale-add-discount').value);
  formData.append('date', document.querySelector('#sale-add-date').value);

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

document.querySelector("[name='sale-remove-form']").addEventListener('submit', async function(event){
  event.preventDefault();

  var formData = new FormData();
  formData.append('sale', this.id)

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