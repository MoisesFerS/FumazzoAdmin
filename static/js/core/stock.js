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

      window.onclick = function(event) {
        if (event.target == modal) {
          modal.style.display = "none";
        }
      }

    }

  /* ADD MODAL */ 

    function add() {

      const date = document.getElementById('restock-date').value;
      const supplier = document.getElementById('restock-price').value;
      const reveiver = document.getElementById('restock-supplier').value;
      const total_cost = document.getElementById('restock-receiver').value;

      console.log(date)
      console.log(supplier)
      console.log(reveiver)
      console.log(total_cost)

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
    
    