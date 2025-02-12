/* ##### ACCORDION ##### */

var acc = document.getElementsByClassName("accordion-row");
var i;

for (i = 0; i < acc.length; i++) {
    acc[i].onclick = function(){
        this.classList.toggle("active");
        var panel = this.nextElementSibling;
        if (panel.style.display === "block") {
            panel.style.display = "none";
        } else {
            panel.style.display = "block";
        }
    }
}

/* ##### MODAL ##### */

/* Define csrfToken como uma variável global */
let csrfToken = null;

/* Function to open a modal based on ID */
function openModal(button) {

    // Chama a função getToken e atribui o valor ao csrfToken
    csrfToken = getToken();  // Armazena o token globalmente
    console.log(csrfToken);

    /* Get the ID of the button clicked, the ID is used to open modals dynamically */
    const modal = document.getElementById(button.name + '-modal');

    /* Bring the modal to front of the page */
    modal.style.display = 'block';

    /* If the modal is Edit, get the information from the accordion row */
    if (button.name === 'edit') {

        /* Get the accordion row where the edit button is located */
        const accordionRow = button.closest('.accordion-row');

        /* Get each information from the row */
        const supplier = accordionRow.querySelector(".row-supplier").id;
        const receiver = accordionRow.querySelector(".row-receiver").id;
        const price = accordionRow.querySelector(".row-price").textContent.replace(',', '.');
        const rawDate = accordionRow.querySelector(".row-date").textContent;

        /* Format the date */
        const [day, month, year] = rawDate.split('/');
        const date = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;

        /* Set the inputs with the information from the accordion row */
        document.getElementById('edit-supplier').value = supplier;
        document.getElementById('edit-receiver').value = receiver;
        document.getElementById('edit-date').value = date;
        document.getElementById('edit-price').value = price;

    }

    /* Get the 'confirm' button from each modal to call the respective function */
    document.getElementById('confirm-' + button.name).onclick = function () {
        submit(button);
    };

    /* When the user click's out of the modal, it closes */
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };

}

function getToken() {
    let csrfToken = null;
    const cookies = document.cookie.split(';');
    cookies.forEach(cookie => {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            csrfToken = decodeURIComponent(value);
        }
    });
    return csrfToken; // Retorna o token
}

function submit(button) {
    const form = document.getElementById(`restock_${button.name}_form`);
    const path = `restock/${button.name}${button.id ? '/' + button.id : ''}/`;

    const options = {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken  // Usa o csrfToken que foi atribuído globalmente
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


/* teste */


document.getElementById('add-item').addEventListener('click', function () {

    const itemDiv = document.createElement('div');
    itemDiv.classList.add('edit-item');
    
    const itemNameInput = document.createElement('input');
    itemNameInput.type = 'text';
    itemNameInput.name = 'item_name[]';
    itemNameInput.placeholder = 'Nome do Item';
    
    const itemQuantityInput = document.createElement('input');
    itemQuantityInput.type = 'number';
    itemQuantityInput.name = 'item_quantity[]';
    itemQuantityInput.placeholder = 'Quantidade';
    
    const removeButton = document.createElement('button');
    removeButton.textContent = 'Remover Item';
    removeButton.type = 'button';
    removeButton.classList.add('remove-item');
    
    itemDiv.appendChild(itemNameInput);
    itemDiv.appendChild(itemQuantityInput);
    itemDiv.appendChild(removeButton);
    
    document.querySelector('.edit-items').appendChild(itemDiv);
    
    removeButton.addEventListener('click', function() {
        itemDiv.remove();
    });

});
