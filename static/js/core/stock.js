/* ##### ACCORDION ##### */

  /* VARIABLES */

    var acc = document.getElementsByClassName("accordion-row");
    var i;

  /* EXPAND ACCORDION */

    for (i = 0; i < acc.length; i++) {
      acc[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var panel = this.nextElementSibling;
        if (panel.style.maxHeight) {
          panel.style.maxHeight = null;
        } else {
          panel.style.maxHeight = panel.scrollHeight + "px";
        }
      });
    }

/* ##### MODAL ##### */

  /* OPEN */ 

    function openModal(button){

      const modal = document.getElementById(button.name+'-modal');
      modal.style.display = 'block';

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

      const closeButton = document.getElementById('close-' + button.name + '-modal');
      closeButton.onclick = function() {
        modal.style.display = 'none';
      };

      window.onclick = function(event) {
        if (event.target == modal) {
          modal.style.display = "none";
        }
      }

    }

  /* ADD MODAL */ 

    function add() {
      console.log('Função Add chamada');
    }
  
  /* EDIT MODAL */

    function edit(button) {

      const accordionRow = button.closest('.accordion')

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

      console.log(supplier)

    }

  /* REMOVE MODAL */
    
    function remove(button) {
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
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
          } else {
            console.error('Panel relacionado não encontrado.');
          }
        })
        .catch(error => {
          console.error('Erro:', error);
        });
    }
    
    