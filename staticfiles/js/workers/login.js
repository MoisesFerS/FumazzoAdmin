document.getElementById('login-form').addEventListener('submit', function(event){
  event.preventDefault();

  var formData = new FormData();
  formData.append('id', document.querySelector('#worker-id').value);
  formData.append('password', document.querySelector('#worker-password').value);

  console.log(formData)

  let csrfToken = getToken();

  fetch('authentication/', { 
    method: 'POST',
    headers: { 'X-CSRFToken': csrfToken }, 
    body: formData
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