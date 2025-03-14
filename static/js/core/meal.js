const buttons = document.querySelectorAll('button')

fetch(`get-ingredients/`)
  .then(response => response.json())
  .then(data => {
    const ingredientsSelect = document.getElementById('meal-add-ingredients');

    data.data.forEach(data => {
      const optgroup = document.createElement('optgroup');
      optgroup.label = data.category; 
      data.ingredients.forEach(ingredient =>{
        const option = document.createElement('option');
        option.value = ingredient.id;
        option.textContent = ingredient.name; 
        optgroup.appendChild(option);
      });
      ingredientsSelect.appendChild(optgroup);
    });
  })
  .catch(error => console.error('Erro ao carregar categorias:', error));

document.querySelector('.meal-accordion-container').addEventListener('click', function(event) {
  if (event.target.closest('.meal-type-accordion')) {
    let typeAccordion = event.target.closest('.meal-type-accordion');
    expand(typeAccordion);
  }

  if (event.target.closest('.meal-category-accordion')) {
    let categoryAccordion = event.target.closest('.meal-category-accordion');
    expand(categoryAccordion);
    updateAllParentPanels(categoryAccordion);
  }

  if (event.target.closest('.meal-accordion')) {
    let mealAccordion = event.target.closest('.meal-accordion');
    expand(mealAccordion);
    updateAllParentPanels(mealAccordion);
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
  let parentPanel = element.closest('.meal-type-accordion-pannel, .meal-category-accordion-pannel, .meal-accordion-pannel');
  
  if (parentPanel) {
    setTimeout(() => {
      parentPanel.style.display = 'block';
      let scrollHeight = parentPanel.scrollHeight;
      parentPanel.style.display = '';
      parentPanel.style.maxHeight = scrollHeight + "px";

      let parentAccordion = parentPanel.previousElementSibling;
      if (parentAccordion && (
          parentAccordion.classList.contains('meal-type-accordion') ||
          parentAccordion.classList.contains('meal-category-accordion') ||
          parentAccordion.classList.contains('meal-accordion'))) {
        updateAllParentPanels(parentAccordion);
      }
    }, 250);
  }
}

/*  ============================================================
    MODALS - Modals functions   
    ============================================================ */ 

/* Function to open the modals dynamically */
document.querySelectorAll("[name='add'], [name='edit'], [name='ingredient'], [name='remove']")
  .forEach(button => {
    button.addEventListener('click', function (event) {
        
      const modal = document.getElementById(`modal-${button.name}`);
      modal.style.display = 'block';
      const form = modal.querySelector(`[name="meal-${button.name}-form"]`)
      form.id = button.id

      window.addEventListener('click', function(event) {
        if (event.target === modal) {
          modal.style.display = "none";
        }
      });

    });
  });

document.getElementById('meal-add-type').addEventListener('change', function () {
  const categoriesSelect = document.getElementById('meal-add-categories');
  categoriesSelect.disabled = false;
  fetch(`add/get-categories/${this.value}/`)
    .then(response => response.json())
    .then(data => {

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

document.querySelector("[name='meal-add-form']").addEventListener('submit', async function(event){
  event.preventDefault();

  var formData = new FormData();
  formData.append('category', document.querySelector('#meal-add-categories').value);
  formData.append('name', document.querySelector('#meal-add-name').value);
  formData.append('description', document.querySelector('#meal-add-description').value);
  formData.append('price', document.querySelector('#meal-add-price').value);
  let imageFile = document.querySelector('#meal-add-image').files[0];
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

document.querySelector("[name='meal-edit-form']").addEventListener('submit', async function(event){
  event.preventDefault();

  var formData = new FormData();
  formData.append('mealID', this.id)
  formData.append('name', document.querySelector('#meal-edit-name').value);
  formData.append('description', document.querySelector('#meal-edit-description').value);
  formData.append('price', document.querySelector('#meal-edit-price').value);
  let imageFile = document.querySelector('#meal-new-image').files[0];
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


document.querySelector("[name='meal-remove-form']").addEventListener('submit', async function(event){
  event.preventDefault();

  var formData = new FormData();
  formData.append('meal', this.id)

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

document.querySelector("[name='meal-ingredient-form']").addEventListener('submit', async function(event){
  event.preventDefault();

  var formData = new FormData();
  formData.append('meal', this.id);
  formData.append('ingredient', this.querySelector('#meal-add-ingredients').value);

  let csrfToken = getToken(); 
  
  await fetch(`ingredient/add/`, {
    method: 'POST',
    headers: { 'X-CSRFToken': csrfToken }, 
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if(data.status == 'success'){
      let ingredientsContainer = document.querySelector(`.meal-ingredients-container[id="${data.ingredient.mealID}"]`);
      
      let mealIngredient = document.createElement('div')
      mealIngredient.classList.add('meal-ingredient')

      let ingredientImage = document.createElement('img')
      ingredientImage.src = data.ingredient.image
      ingredientImage.classList.add('ingredient-image')
      mealIngredient.append(ingredientImage)

      let ingredientLabel = document.createElement('p')
      ingredientLabel.innerHTML = data.ingredient.name
      ingredientLabel.classList.add('ingredient-label')
      ingredientLabel.classList.add('subtitle')
      mealIngredient.append(ingredientLabel)

      let qunatityContainer = document.createElement('div')
      qunatityContainer.classList.add('ingredient-quantity-container')

      let ingredientQuantity = document.createElement('p')
      ingredientQuantity.innerHTML = data.ingredient.quantity
      ingredientQuantity.classList.add('ingredient-quantity')
      ingredientQuantity.classList.add('subtitle')
      qunatityContainer.append(ingredientQuantity)

      let buttonTypes = ['ingredient-increment', 'ingredient-subtract', 'ingredient-remove'];

      buttonTypes.forEach(action => {
        let ingredientButton = document.createElement('button');
        ingredientButton.classList.add(`${action}-button`);  
        ingredientButton.name = action;  
        ingredientButton.id = data.ingredient.id
        qunatityContainer.append(ingredientButton);
      });

      mealIngredient.append(qunatityContainer)
      ingredientsContainer.append(mealIngredient)

      const modal = document.getElementById(`modal-ingredient`);
      modal.style.display = 'none';

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

document.querySelectorAll('.meal-ingredients-container')
.forEach(mealContent => {
  mealContent.addEventListener('click', async function(event) {
    const target = event.target;

    if (target && target.tagName === 'BUTTON' && target.name) {
      const action = target.name.split('-')[1]; 
      handleButtonClick(target, action);
    }

  });
});

async function handleButtonClick(button, action) {
  const buttons = button.closest('.meal-ingredient').querySelectorAll('button');
  buttons.forEach(btn => btn.disabled = true);

  const meal = button.closest('.meal-accordion-pannel');
  const ingredient = button.id; 
  const ingredientContainer = button.closest('.meal-ingredient');

  const data = {
    meal: meal.id,
    ingredient: ingredient,
  };

  let csrfToken = getToken();

  await fetch(`ingredient/${action}/`, {
    method: 'POST',
    headers: { 'X-CSRFToken': csrfToken },
    body: JSON.stringify(data),
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      if (action === 'remove') {
        ingredientContainer.remove(); 
      } else {
        ingredientContainer.querySelector('.ingredient-quantity').innerHTML = data.quantity;
      }
    } else {
      message.style.display = 'block';
      message.querySelector('#message-text').innerHTML = data.message;
      message.querySelector('#message-error').innerHTML = data.error;
      setTimeout(() => {
        message.style.display = 'none';
      }, 3000);
    }
    buttons.forEach(btn => btn.disabled = false); 
  });
}

document.querySelectorAll('.meal-button.edit').forEach(button => {
  button.addEventListener('click', async function(){

    var formData = new FormData();
    formData.append('meal', this.id)

    let csrfToken = getToken();

    await fetch(`data/`, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken },
      body: formData,
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        let info = ['name', 'description', 'price', 'image']

        info.forEach(input => {
          let editInfo = document.querySelector(`#meal-edit-${input}`)
          if(input == 'image'){
            editInfo.src = data.mealData[input]
          } else {
            editInfo.value = data.mealData[input]
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
      buttons.forEach(btn => btn.disabled = false); 
    });
  });
});