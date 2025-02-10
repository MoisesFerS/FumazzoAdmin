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

  function openModal(button) {
    console.log(button);

    const modal = document.getElementById(button.name + '-modal');
    modal.style.display = 'block';

    if (button.name === 'edit') {
      setTimeout(() => edit(button), 100);
    }

    document.getElementById('confirm-' + button.name).addEventListener('click', function () {
        switch (button.name) {
            case 'add':
                add();
                break;

            case 'edit':
                submitEditForm();
                break;

            case 'remove':
                remove(button);
                break;
        }
    });

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };
}


  /* ADD MODAL */ 

    function add() {
      
      let form = document.getElementById("restock_add_form");

      form.removeEventListener("submit", submitAddForm);
      form.addEventListener("submit", submitAddForm);

    }

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
      .then(response => response.json())
      .then(data => {
          alert(data.message);
          window.location.reload();
      })
      .catch(error => {
          console.error('Erro:', error);
      });
      
    }

      