document.querySelector('.meal-accordion-container').addEventListener('click', function(event) {
  if (event.target.closest('.meal-type-accordion')) {
    let typeAccordion = event.target.closest('.meal-type-accordion');
    expand(typeAccordion);
  }

  if (event.target.closest('.meal-category-accordion')) {
    let categoryAccordion = event.target.closest('.meal-category-accordion');
    expand(categoryAccordion);
    requestAnimationFrame(() => updateParentPanelHeight(categoryAccordion));
  }

  if (event.target.closest('.meal-accordion')) {
    let mealAccordion = event.target.closest('.meal-accordion');
    expand(mealAccordion);
    requestAnimationFrame(() => updateParentPanelHeight(mealAccordion));
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

function updateParentPanelHeight(accordion) {
  let parentPanel = accordion.closest('.meal-type-accordion-pannel');
  if (parentPanel) {
    setTimeout(() => {
      parentPanel.style.display = 'block';
      let scrollHeight = parentPanel.scrollHeight;
      parentPanel.style.display = ''; 
      parentPanel.style.maxHeight = scrollHeight + "px";
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

      window.addEventListener('click', function(event) {
        if (event.target === modal) {
          modal.style.display = "none";
        }
      });

    });
  });

document.getElementById('meal-add-type').addEventListener('change', function () {
  fetch(`add/get-categories/${this.value}/`)
    .then(response => response.json())
    .then(data => {
      const categoriesSelect = document.getElementById('meal-add-categories');
      
      categoriesSelect.innerHTML = '';
      const defaultOption = document.createElement('option');

      data.data.forEach(category => {
        const option = document.createElement('option'); 
        option.textContent = category.name;
        option.value = category.id;
        categoriesSelect.appendChild(option);
      });
    })
    .catch(error => console.error('Erro ao carregar categorias:', error));
});

document.getElementById('meal-add-form').addEventListener('submit', async function(event){
  event.preventDefault();

  var formData = new FormData();
  formData.append('category', document.querySelector('#meal-add-categories').value);
  formData.append('name', document.querySelector('#meal-add-name').value);
  formData.append('description', document.querySelector('#meal-add-description').value);
  formData.append('price', document.querySelector('#meal-add-price').value);
  formData.append('image', document.querySelector('#meal-add-image').files[0]); 

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
