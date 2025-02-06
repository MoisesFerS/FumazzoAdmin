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

  /* OPEN */ 

    function openModal(button){
      console.log(button)

      const modal = document.getElementById(button.name+'-modal');
      modal.style.display = 'block';

      document.getElementById('confirm-'+button.name).addEventListener('click', function(){

        switch (button.name) {
          case 'add':
            add();
            break;

          case 'edit':
            edit(button);
            break;

          case 'remove':
            remove(button);
            break;
        }

      });

      window.onclick = function(event) {
        if (event.target == modal) {
          modal.style.display = "none";
        }
      }

    }

  /* ADD MODAL */ 

  function add() {
    let form = document.getElementById("restock_add_form");

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        let formData = new FormData(this);

        fetch("restock/add/", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
            }
        })
        .then(response => response.json())
        .then(data => {
            let msgDiv = document.getElementById("mensagem");

            if (data.status === "success") {
                msgDiv.innerHTML = `<p style="color: green;">${data.message}</p>`;
            
                let newRestock = data.restock; 

                let newAccordionRow = document.createElement("div");
                newAccordionRow.classList.add("accordion-row");

                newAccordionRow.innerHTML = `
                    <div class="accordion-row-labels">
                        <p class="row-date-label">DATA: </p>
                        <p class="row-supplier-label">FORNECEDOR: </p>
                        <p class="row-receiver-label">RECEPTOR: </p>
                        <p class="row-price-label">PREÇO TOTAL: </p>
                    </div>
                    <div class="accordion-row-data">
                        <p class="row-date">${newRestock.date}</p>
                        <p class="row-supplier">${newRestock.supplier}</p>
                        <p class="row-receiver">${newRestock.receiver}</p>
                        <p class="row-price">${newRestock.total_price}</p>
                    </div>
                    <div class="accordion-row-buttons">
                        <button class="button-edit" id="${newRestock.id}" name="edit" onclick="openModal(this)">
                            <img src="{% static 'icons/edit.ico' %}" class="accordion-icon" alt="">
                        </button>
                        <button class="button-remove" id="${newRestock.id}" name="remove" onclick="openModal(this)">
                            <img src="{% static 'icons/trash-can.ico' %}" class="accordion-icon" alt="">
                        </button>
                    </div>
                `;

                document.querySelector(".accordion-container").prepend(newAccordionRow);

                form.reset(); 
                document.getElementById("add-modal").style.display = "none";

            } else {
                msgDiv.innerHTML = `<p style="color: red;">${data.message}</p>`;
            }
        })
        .catch(error => console.error("Erro:", error));
    });
}




  /* REMOVE MODAL */
    
    function remove(button) {
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      console.log(button)
    
      fetch(`restock/delete/${button.id}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
        },
      })
      .then(response => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error('Erro ao deletar o restock');
        }
      })
      .then(data => {
        console.log(data.message);
  
        const accordionRow = button.closest('.accordion-row');
        if (accordionRow) {
          accordionRow.remove();
          console.log('Accordion-row removido com sucesso.');
        }
  
        const panel = document.getElementById(`panel-${button.id}`);
        if (panel) {
          panel.remove();
          console.log('Panel removido com sucesso.');
        }

        const accordionDivision = document.getElementById(`accordion-division-${button.id}`);
        if (accordionDivision) {
          accordionDivision.remove();
          console.log('Accordion-division removido com sucesso.');
        }

      })
      .catch(error => {
        console.error('Erro:', error);
      });
    }
    

      /* EDIT MODAL */

      function edit(button) {

        const accordionRow = button.closest('.accordion-row')
  
        const supplier = accordionRow.querySelector(".row-supplier").textContent;
        const receiver = accordionRow.querySelector(".row-receiver").textContent;
        const price = accordionRow.querySelector(".row-price").textContent.replace(',', '.');
  
        const rawDate = accordionRow.querySelector(".row-date").textContent;
        const [day, month, year] = rawDate.split('/');
        const date = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
  
        document.getElementById('edit-supplier').value = supplier;
        document.getElementById('edit-receiver').value = receiver;
        document.getElementById('edit-date').value = date;
        document.getElementById('edit-price').value = price;
  
  
  
      }
    