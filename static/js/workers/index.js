document.getElementById('ticket-form').addEventListener('submit', async function(event){
  event.preventDefault();

  var formData = this.querySelectorAll('#form-data');
  
  var data = {
    reason : formData[0].value,
    priority : formData[1].value,
    sector : formData[2].value,
    category : formData[3].value,
    description : formData[4].value,
  }

  let csrfToken = getToken();

  await fetch(`manage/ticket/add/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
      },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
    if(data.status == 'success'){
      location.reload(); 
    } else {          
      message.style.display = 'block';        
      message.querySelector('#message-text').innerHTML = data.message; 
      message.querySelector('#message-error').innerHTML = data.error;
      setTimeout(() => {
        message.style.display = 'none'; 
      }, 3000);
    }
  }); 
  
});