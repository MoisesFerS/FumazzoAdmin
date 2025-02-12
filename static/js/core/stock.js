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

/* Function to open a modal based on ID */
function openModal(button) {

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
    document.getElementById('confirm-' + button.name).addEventListener('click', function () {
        submit(button);
    });

    /* When the user click's out of the modal, it closes */
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };

}

function submit(button) {

    let form = document.getElementById(`restock_${button.name}_form`);

    let options = {
        
        method: "POST",
        headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
        }

    };

    let path;

    switch (button.name) {

        case 'add':
            path = `restock/add/`;
            options.body = new FormData(form);
            break;

        case 'edit':
            path = `restock/edit/${button.id}/`;
            options.body = new FormData(form);
            break;

        case 'remove':
            path = `restock/remove/${button.id}/`;
            break;

    }

    console.log("Enviando requisição para:", path);

    fetch(path, options)
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        location.reload();
    })
    .catch(error => console.error("Erro:", error));

}

document.getElementById('add-item').addEventListener('click', function () {
    // Criação de uma nova div para o item
    const itemDiv = document.createElement('div');
    itemDiv.classList.add('edit-item');
    
    // Campos para o novo item (por exemplo, nome do item e quantidade)
    const itemNameInput = document.createElement('input');
    itemNameInput.type = 'text';
    itemNameInput.name = 'item_name[]';
    itemNameInput.placeholder = 'Nome do Item';
    
    const itemQuantityInput = document.createElement('input');
    itemQuantityInput.type = 'number';
    itemQuantityInput.name = 'item_quantity[]';
    itemQuantityInput.placeholder = 'Quantidade';
    
    // Botão para remover o item
    const removeButton = document.createElement('button');
    removeButton.textContent = 'Remover Item';
    removeButton.type = 'button';
    removeButton.classList.add('remove-item');
    
    // Adicionando os campos e o botão à nova div
    itemDiv.appendChild(itemNameInput);
    itemDiv.appendChild(itemQuantityInput);
    itemDiv.appendChild(removeButton);
    
    // Adicionando a nova div dentro de edit-items
    document.querySelector('.edit-items').appendChild(itemDiv);
    
    // Lógica para remover o item
    removeButton.addEventListener('click', function() {
        itemDiv.remove();
    });
});
