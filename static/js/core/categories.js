document.querySelector('.categories-accordion-container').addEventListener('click', function(event) {
  if (event.target.closest('.category-type-accordion')) {
    let typeAccordion = event.target.closest('.category-type-accordion');
    expand(typeAccordion);
  }

  if (event.target.closest('.category-category-accordion')) {
    let categoryAccordion = event.target.closest('.category-category-accordion');
    expand(categoryAccordion);
    updateAllParentPanels(categoryAccordion);
  }

  if (event.target.closest('.category-accordion')) {
    let categoryAccordion = event.target.closest('.category-accordion');
    expand(categoryAccordion);
    updateAllParentPanels(categoryAccordion);
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
  let parentPanel = element.closest('.category-type-accordion-panel, .category-category-accordion-panel, .category-accordion-panel');
  
  if (parentPanel) {
    setTimeout(() => {
      parentPanel.style.display = 'block';
      let scrollHeight = parentPanel.scrollHeight;
      parentPanel.style.display = '';
      parentPanel.style.maxHeight = scrollHeight + "px";

      let parentAccordion = parentPanel.previousElementSibling;
      if (parentAccordion && (
          parentAccordion.classList.contains('category-type-accordion') ||
          parentAccordion.classList.contains('category-category-accordion') ||
          parentAccordion.classList.contains('category-accordion'))) {
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
      const form = modal.querySelector(`[name="category-${button.name}-form"]`)
      form.id = button.id

      window.addEventListener('click', function(event) {
        if (event.target === modal) {
          modal.style.display = "none";
        }
      });

    });
  });

document.querySelector("[name='category-add-form']").addEventListener('submit', async function(event){
  event.preventDefault();

  var formData = new FormData();
  formData.append('type', document.querySelector('#category-add-type').value);
  formData.append('name', document.querySelector('#category-add-name').value);

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

document.querySelector("[name='category-edit-form']").addEventListener('submit', async function(event){
  event.preventDefault();

  var formData = new FormData();
  formData.append('categoryID', this.id)
  formData.append('name', document.querySelector('#category-edit-name').value);

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

document.querySelector("[name='category-remove-form']").addEventListener('submit', async function(event){
  event.preventDefault();

  var formData = new FormData();
  formData.append('category', this.id)

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

document.querySelectorAll('.category-button.edit').forEach(button => {
  button.addEventListener('click', async function(){

    var formData = new FormData();
    formData.append('category', this.id)

    let csrfToken = getToken();

    await fetch(`data/`, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken },
      body: formData,
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        let info = ['name']

        info.forEach(input => {
          let editInfo = document.querySelector(`#category-edit-${input}`)
          editInfo.value = data.categoryData[input]
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