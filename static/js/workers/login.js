document.getElementById('login-form').addEventListener('submit', function(event){
  event.preventDefault();

  var id = this.querySelector('#id').value;
  var password = this.querySelector('#password').value;

  var data = {
    id : id,
    password : password,
  }

  let csrfToken = getToken();
  const message = document.getElementById('message');

  fetch('authentication/', { 
    method: 'POST',
    headers: { 'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
      if (data.status == 'success'){
        window.location.href = '/'
      } else {          
        message.style.display = 'block';        
        message.querySelector('#message-text').innerHTML = data.message; 
        message.querySelector('#message-error').innerHTML = data.error;
        setTimeout(() => {
          message.style.display = 'none'; 
        }, 3000);
      }
  })
  .catch(error => console.error('Erro:', error));

});