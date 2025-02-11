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

        /* According with the button's name, call a function, pass the button to use it's ID */
            switch (button.name) {

                /* If the function is */
                case 'add' || 'edit':
                submit(button);
                break;

                case 'remove':
                remove(button);
                break;

            }

        });

        /* When the user click's out of the modal, it closes */
        window.onclick = function (event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        };

    }

    /* Function to prevents multiple submitions */
    function submit(button) {
    
        /* Get the form from the modal */
        let form = document.getElementById(`restock_${button.name}_form`);

        
        switch (button.name) {

            case 'add':

                form.removeEventListener("submit", submitAddForm);
                form.addEventListener("submit", submitAddForm);
                
                break;

            case 'edit':
                
                form.removeEventListener("submit", submitEditForm);
                form.addEventListener("submit", submitEditForm);

                break;
        
        }

        

    }

  /* ADD MODAL */ 



    /* Function that subimits the form to the Django URL */
    function submitAddForm(event) {

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
          alert(data.message);
          window.location.reload();
      })
      .catch(error => console.error("Erro:", error));

    }

  /* EDIT MODAL */

    /* Function that is called when the confirm of the EDIT modal is clicked */
    function edit(event) {

        event.preventDefault(); 
  
        let formData = new FormData(this);
  
        fetch(`restock/edit/${button.id}/`, {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
            }
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            window.location.reload();
        })
        .catch(error => console.error("Erro:", error));
  
      }



  /* REMOVE MODAL */
    
    /* Function called after the confirm button from the REMOVE modal is clicked */
    function remove(button) {

        /* Gets the token fron the form and uses to make a requisition */
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        /* Uses the fetch function to do a requisition to the URL of Django that does the logic */
        fetch(`restock/delete/${button.id}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            window.location.reload();
        })
        .catch(error => {
            console.error('Erro:', error);
        });
        
    }

      