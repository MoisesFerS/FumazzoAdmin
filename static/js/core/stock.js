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

/* Function that gets the csrf token from the cookies */
function getToken() {
  return document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1] || '';
}


/* Get the selects info */
let selectItems = [];

fetch(`edit/get-products/`)
.then(response => response.json())
.then(data => {
  selectItems = data
})
.catch(error => console.error('Erro ao carregar categorias e produtos:', error));


/* ===== ADD MODAL ===== */

/* Function to add an entry to the database */
document.getElementById('confirm-add').addEventListener('click', async function () {

  const form = this.closest('.modal-add-form');
  var addData = form.querySelectorAll('#stock-add-supplier, #stock-add-receiver, #stock-add-date');
  
  let data = {
    date: addData[0]?.value,
    supplier: addData[1]?.value,
    receiver: addData[2]?.value,
  };

  if (!data.date) {
    alert("Preencha todos os campos.");
    return;
  }

  let csrfToken = getToken();

  await fetch(`add/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
      },
    body: JSON.stringify(data)
  });

  location.reload(); 

});

/* ===== EDIT MODAL ===== */

/* Loads the edit information  */
document.querySelectorAll("[name='edit']")
  .forEach(edit => {
    edit.addEventListener('click', function (){

      const accordionData = edit.closest('.stock-accordion');
      const stockData = accordionData.querySelectorAll(".stock-accordion-text");

      var date = stockData[0] ? stockData[0].id : '';
      var supplier = stockData[1] ? stockData[1].id : '';
      var receiver = stockData[2] ? stockData[2].id : '';
      var price = stockData[3] ? stockData[3].id.replace(",", ".") : '';

      document.getElementById('stock-edit-supplier').value = supplier;
      document.getElementById('stock-edit-receiver').value = receiver;
      document.getElementById('stock-edit-date').value = date;

      document.querySelector('.modal-edit-form').id = edit.id;
      const productsContainer = document.getElementById('products-container');
      productsContainer.innerHTML = '';

      fetch(`edit/load-product/${edit.id}/`)
      .then(response => response.json())
      .then(data => {
        data.forEach(data => createProduct(data));
      })
      .catch(error => console.error('Erro ao carregar categorias e produtos:', error));

    });

  });

/* Function to send the information from edit modal to backend */
document.getElementById('confirm-edit').addEventListener('click', async function () {

  const form = this.closest('.modal-edit-form');
  var editData = form.querySelectorAll('#stock-edit-supplier, #stock-edit-receiver, #stock-edit-date');

  var edit = {
    supplier: editData[0]?.value,
    receiver: editData[1]?.value,
    date: editData[2]?.value,
  };

  if (!edit.supplier || !edit.receiver || !edit.date) {
    alert("Preencha todos os campos.");
    return;
  }

  var products = [];
  let hasError = false;

  form.querySelectorAll('.product-content').forEach(product => {
    
    var productData = {
      item: product.querySelector("#product-item")?.value || '',
      quantity: product.querySelector("#product-quantity")?.value || '',
      price: product.querySelector("#product-price")?.value || '',
    };

    if (!productData.item || !productData.quantity || !productData.price) {
      alert(`Preencha todos os campos de todos os produtos.`);
      hasError = true
    } else if (productData.quantity < 0 || productData.price < 0) {
      alert(`Os valores não podem ser negativos.`);
      hasError = true
    } else {
      products.push(productData);
    }

  });

  if (hasError) return;

  let data = {
    edit: edit,
    products: products,
  };

  let csrfToken = getToken();

  await fetch(`edit/save/${form.id}/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
      },
    body: JSON.stringify(data)
  });

  location.reload(); 
});

/* Function to add products in edit modal */
document.getElementById('add-product').addEventListener("click", createProduct);

function createProduct(data=null){

  const productsContainer = document.getElementById('products-container');

  const product = document.createElement('div');
  product.classList.add('product-content');
  productsContainer.appendChild(product);

  const select = document.createElement('select');
  select.classList.add('product-select')
  select.id = "product-item"

  selectItems.forEach(item => {
    
    const optgroup = document.createElement('optgroup');
    optgroup.label = item.categories; 

    item.products.forEach(product => {
      const option = document.createElement('option');
      option.value = product.id;
      option.textContent = product.name; 

      if (data.current_product == product.id) {
        option.selected = true;
      }

      optgroup.appendChild(option);
    });

    select.appendChild(optgroup);
    
  });

  product.appendChild(select);

  const productQuantity = document.createElement('input');
  productQuantity.id = "product-quantity";
  productQuantity.classList.add('product-input');
  productQuantity.type = 'number';
  productQuantity.value = data.quantity ? data.quantity : '';
  product.appendChild(productQuantity);

  const productPrice = document.createElement('input');
  productPrice.id = "product-price";
  productPrice.classList.add('product-input');
  productPrice.type = 'number';
  productPrice.value = data.price ? data.price : '';
  product.appendChild(productPrice);

  const removeProduct = document.createElement('button');
  removeProduct.classList.add('product-button-remove');
  removeProduct.innerText = 'X';
  removeProduct.addEventListener('click', function (){
    removeProduct.closest('.product-content').remove()
  })
  product.appendChild(removeProduct);

}

/* ===== REMOVE MODAL ===== */

/* Function to remove an entry */
document.querySelectorAll("[name='remove']")
  .forEach(remove => {
    remove.addEventListener('click', function (){

      document.getElementById('confirm-remove').addEventListener('click', async function (){

        let csrfToken = getToken();
        
        await fetch(`remove/${remove.id}/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json',
                      'X-CSRFToken': csrfToken,
            },        
        });

        location.reload(); 

      });
    });
  });