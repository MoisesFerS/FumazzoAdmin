fetch(`get-shift/`)
.then(response => response.json())
.then(data => {
    startCountdown(data)
})
.catch(error => console.error('Erro ao carregar informações do turno:', error));

function startCountdown(data) {

  const now = new Date();
  var [hours, minutes, seconds] = data.start.split(":").map(Number);
  const startTime = new Date(now.getFullYear(), now.getMonth(), now.getDate(), hours, minutes, seconds);
  var [hours, minutes, seconds] = data.end.split(":").map(Number);
  const endTime = new Date(now.getFullYear(), now.getMonth(), now.getDate(), hours, minutes, seconds);

  document.getElementById('shift-name').innerHTML = data.name

  const statusIndicator = document.getElementById('status-indicator')
  statusIndicator.classList.add('functional')
  document.getElementById('status-indicator-text').innerHTML = `EM SERVIÇO`

  function updateCountdown() {
    const now = new Date();
    if(now < endTime && now > startTime){
      
      var remainingTime = endTime - now;
      const hoursLeft = Math.floor(remainingTime / (1000 * 60 * 60));
      const minutesLeft = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
      const secondsLeft = Math.floor((remainingTime % (1000 * 60)) / 1000);

      document.getElementById('remaining-time').innerHTML = (`${hoursLeft}h ${minutesLeft}m ${secondsLeft}s`);

    } else {
      document.getElementById('status-indicator-text').innerHTML = `DESCANSO`
      document.getElementById('remaining-time').innerHTML = (`00h 00m 00s`);
      statusIndicator.classList.remove('functional')
      statusIndicator.classList.add('not-functional')
      clearInterval(interval);
    }
    
  }

  const interval = setInterval(updateCountdown, 1000);
  updateCountdown();
}

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

  await fetch(`manage/tickets/add/`, {
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
