/*  ==========================================================
  ACCORDIONS - Accordions functions
  ========================================================== */ 

/* Add 'onclick' to accordions */
document.querySelector('.stock-accordion-container').addEventListener('click', function(event){

  if (event.target.closest('.stock-accordion')){
    let stockAccordion = event.target.closest('.stock-accordion');
    expand(stockAccordion);
  }

  if (event.target.closest('.stock-product-accordion')){
    let productAccordion = event.target.closest('.stock-product-accordion');
    let maxHeight = expand(productAccordion); 
    
    let stockAccordionPanel = productAccordion.closest('.stock-accordion-panel');
    stockAccordionPanel.style.maxHeight = stockAccordionPanel.scrollHeight + maxHeight;
  }

});

/* Expand function */
function expand(accordion){

  accordion.classList.toggle('active');
  let panel = accordion.nextElementSibling;
  if(panel.style.maxHeight){
    panel.style.maxHeight = null;
  }else{
    panel.style.maxHeight = panel.scrollHeight + "px";
  }

  return panel.style.maxHeight

}

/*  ==========================================================
  MODALS - Modals functions   
  ========================================================== */ 

/* Function to open the modals dynamically */
function openModal(button) {

  const modal = document.getElementById(`modal-${button.name}`);
  modal.style.display = 'block';

  if (button.name === 'edit') {
    editData(button);
  }

  document.getElementById('confirm-' + button.name).onclick = function () {
    submit(button);
  };

  window.onclick = function (event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  };

}

function editData(button){

  const accordionData = button.closest('.stock-accordion');
  const stockData = accordionData.querySelectorAll(".stock-accordion-text");

  var date = stockData[0] ? stockData[0].id : '';
  var supplier = stockData[1] ? stockData[1].id : '';
  var receiver = stockData[2] ? stockData[2].id : '';
  var price = stockData[3] ? stockData[3].id.replace(",", ".") : '';

  document.getElementById('stock-edit-supplier').value = supplier;
  document.getElementById('stock-edit-receiver').value = receiver;
  document.getElementById('stock-edit-date').value = date;
  document.getElementById('stock-edit-price').value = price;

  const productsContainer = document.getElementById('products-container');
  productsContainer.innerHTML = '';

  fetch(`restock/edit/load-product/${button.id}/`)
  .then(response => response.json())
  .then(data => {
    createProduct(data);
  })
  .catch(error => console.error('Erro ao carregar categorias e produtos:', error));
  

}

/* Function that gets the csrf token from the cookies */
function getToken() {
  let csrfToken = null;
  const cookies = document.cookie.split(';');
  cookies.forEach(cookie => {
    const [name, value] = cookie.trim().split('=');
    if (name === 'csrftoken') {
      csrfToken = decodeURIComponent(value);
    }
  });
  return csrfToken;
}

/* Function to submit the forms */
function submit(button) {
  let csrfToken = getToken(); 
  const form = document.getElementById(`restock_${button.name}_form`);
  const path = `restock/${button.name}${button.id ? '/' + button.id : ''}/`;

  const options = {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken  
    }
  };

  if (button.name !== 'remove') {
    options.body = new FormData(form);
  }

  fetch(path, options)
    .then(response => response.json())
    .then(data => {
      console.log(data);
      alert(data.message);
      location.reload();
    })
    .catch(error => console.error("Erro:", error));
}

/* Function to add products at edit modal */
document.getElementById('add-product').addEventListener("click", createProduct);

function createProduct(data){

  fetch(`restock/edit/add-product/`)
  .then(response => response.json())
  .then(data => {
    var categories_products = data
  })
  .catch(error => console.error('Erro ao carregar categorias e produtos:', error));

  const productsContainer = document.getElementById('products-container');

  data.forEach(item => {
    const product = document.createElement('div');
    product.classList.add('product-content');
    productsContainer.appendChild(product);

    const select = document.createElement('select');
    data.forEach(category => {
      const optgroup = document.createElement('optgroup');
      optgroup.label = category.name;

      category.product.forEach(product => {
        const option = document.createElement('option');
        option.value = data.current_product;
        option.textContent = product.name;
        optgroup.appendChild(option);
      });

      select.appendChild(optgroup);
    });

    product.appendChild(select);

    const productQuantity = document.createElement('input');
    productQuantity.type = 'number';
    productQuantity.value = item.quantity;
    product.appendChild(productQuantity);

    const productPrice = document.createElement('input');
    productPrice.type = 'number';
    productPrice.value = item.batch_price;
    product.appendChild(productPrice);

  });
  
}
