document.querySelector('.products-accordion-container').addEventListener('click', function(event) {
  if (event.target.closest('.product-type-accordion')) {
    let typeAccordion = event.target.closest('.product-type-accordion');
    expand(typeAccordion);
  }

  if (event.target.closest('.product-category-accordion')) {
    let categoryAccordion = event.target.closest('.product-category-accordion');
    expand(categoryAccordion);
    updateAllParentPanels(categoryAccordion);
  }

  if (event.target.closest('.product-accordion')) {
    let productAccordion = event.target.closest('.product-accordion');
    expand(productAccordion);
    updateAllParentPanels(productAccordion);
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
  let parentPanel = element.closest('.product-type-accordion-panel, .product-category-accordion-panel, .product-accordion-panel');
  
  if (parentPanel) {
    setTimeout(() => {
      parentPanel.style.display = 'block';
      let scrollHeight = parentPanel.scrollHeight;
      parentPanel.style.display = '';
      parentPanel.style.maxHeight = scrollHeight + "px";

      let parentAccordion = parentPanel.previousElementSibling;
      if (parentAccordion && (
          parentAccordion.classList.contains('product-type-accordion') ||
          parentAccordion.classList.contains('product-category-accordion') ||
          parentAccordion.classList.contains('product-accordion'))) {
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
      const form = modal.querySelector(`[name="product-${button.name}-form"]`)
      form.id = button.id

      window.addEventListener('click', function(event) {
        if (event.target === modal) {
          modal.style.display = "none";
        }
      });

    });
  });

document.getElementById('product-add-type').addEventListener('change', function () {
  const categoriesSelect = document.getElementById('product-add-categories');
  categoriesSelect.disabled = false;
  const priceInput = document.getElementById('product-sell-price');
  fetch(`add/get-categories/${this.value}/`)
    .then(response => response.json())
    .then(data => {      

      this.value == 4 ? priceInput.style.display = 'block' : priceInput.style.display = 'none';
        
      categoriesSelect.innerHTML = '';

      data.data.forEach(category => {
        const option = document.createElement('option'); 
        option.textContent = category.name;
        option.value = category.id;
        categoriesSelect.appendChild(option);
      });
    })
    .catch(error => console.error('Erro ao carregar categorias:', error));
});

document.querySelector("[name='product-add-form']").addEventListener('submit', async function(event){
  event.preventDefault();

  var formData = new FormData();
  formData.append('category', document.querySelector('#product-add-categories').value);
  formData.append('name', document.querySelector('#product-add-name').value);
  let sellPrice = document.querySelector('#product-add-price').value
  sellPrice ? formData.append('price', sellPrice) : null;
  let imageFile = document.querySelector('#product-add-image').files[0];
  formData.append('image', imageFile ? imageFile : null);

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

document.querySelector("[name='product-edit-form']").addEventListener('submit', async function(event){
  event.preventDefault();

  var formData = new FormData();
  formData.append('productID', this.id)
  formData.append('name', document.querySelector('#product-edit-name').value);
  formData.append('price', document.querySelector('#product-edit-price').value);
  let imageFile = document.querySelector('#product-new-image').files[0];
  formData.append('image', imageFile ? imageFile : null);

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

document.querySelector("[name='product-remove-form']").addEventListener('submit', async function(event){
  event.preventDefault();

  var formData = new FormData();
  formData.append('product', this.id)

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

document.querySelector("[name='product-remove-form']").addEventListener('submit', async function(event){
  event.preventDefault();

  var formData = new FormData();
  formData.append('product', this.id)

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

document.querySelectorAll('.product-button.edit').forEach(button => {
  button.addEventListener('click', async function(){

    var formData = new FormData();
    formData.append('product', this.id)

    let csrfToken = getToken();

    const editPrice = document.getElementById('product-edit-price-container');

    await fetch(`data/`, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken },
      body: formData,
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        let info = ['name', 'price', 'image']

        info.forEach(input => {
          let editInfo = document.querySelector(`#product-edit-${input}`)
          if(input == 'image'){
            editInfo.src = data.productData[input]
          } else {
            editInfo.value = data.productData[input]
          }

          if(input == 'price'){
            data.productData[input] ? editPrice.style.display = 'block' : editPrice.style.display = 'none'; 
          }

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