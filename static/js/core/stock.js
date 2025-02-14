/* ##### ACCORDION ##### */

var accordionRows = document.querySelectorAll(".stock-accordion, .stock-product-accordion");

for (var i = 0; i < accordionRows.length; i++) {
    accordionRows[i].onclick = function() {
        this.classList.toggle("active");
        var panel = this.nextElementSibling;
        
        if (panel.style.maxHeight) {
            panel.style.maxHeight = null;
        } else {
            panel.style.maxHeight = panel.scrollHeight + "px";
            
            var parentPanel = this.closest('.stock-accordion-panel');
            if (parentPanel) {
                parentPanel.style.maxHeight = parentPanel.scrollHeight + panel.scrollHeight + "px";
            }
        }
    }
}

/* ##### MODAL ##### */

/* Define csrfToken como uma variável global */
let csrfToken = null;

/* Função para abrir o modal dinamicamente com base no ID */
function openModal(button) {

    csrfToken = getToken(); 

    /* Obter o ID do botão clicado, o ID é usado para abrir modais dinamicamente */
    const modal = document.getElementById(button.name + '-modal');

    /* Colocar o modal à frente da página */
    modal.style.display = 'block';

    /* Se o modal for de Editar, obter as informações da linha do accordion */
    if (button.name === 'edit') {

        /* Obter a linha do accordion onde o botão de editar está localizado */
        const accordionRow = button.closest('.accordion-row');

        /* Obter as informações da linha */
        const supplier = accordionRow.querySelector(".row-supplier").id;
        const receiver = accordionRow.querySelector(".row-receiver").id;
        const price = accordionRow.querySelector(".row-price").textContent.replace(',', '.');
        const rawDate = accordionRow.querySelector(".row-date").textContent;

        /* Formatar a data */
        const [day, month, year] = rawDate.split('/');
        const formattedDate = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;

        /* Definir os valores nos inputs com as informações da linha do accordion */
        document.getElementById('edit-supplier').value = supplier;
        document.getElementById('edit-receiver').value = receiver;
        document.getElementById('edit-date').value = formattedDate;
        document.getElementById('edit-price').value = price;

    }

    /* Obter o botão 'confirmar' de cada modal para chamar a função respectiva */
    document.getElementById('confirm-' + button.name).onclick = function () {
        submit(button);
    };

    /* Quando o usuário clicar fora do modal, ele fecha */
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };

}

/* Função para obter o CSRF Token */
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

/* Função para submeter o formulário */
function submit(button) {
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

/* Teste de adicionar produto */
document.getElementById('add-product').onclick = function () {
    fetch('restock/edit/add-product/')
    .then(response => response.json())
    .then(data => {

        const productsContainer = document.getElementById('products-container');
        const productRow = document.createElement('div');
        productRow.classList.add('product-row');
        productsContainer.appendChild(productRow);

        const productQuantity = document.createElement('input');
        const productPrice = document.createElement('input');

        const select = document.createElement('select'); 

        data.forEach(category => {
            
            const optgroup = document.createElement('optgroup');
            optgroup.label = category.name;

            category.products.forEach(product => {
                const option = document.createElement('option');
                option.value = product.id;
                option.textContent = product.name;
                optgroup.appendChild(option);
            });

            select.appendChild(optgroup);
        });

        productRow.appendChild(select);
        productRow.appendChild(productQuantity);
        productRow.appendChild(productPrice);

    })
    .catch(error => console.error('Erro ao carregar categorias e produtos:', error));
};
