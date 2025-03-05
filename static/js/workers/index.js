const shiftEndStr = document.getElementById("remaining-time").innerHTML;  
startCountdown(shiftEndStr);

function startCountdown(endTimeStr) {
  const [hours, minutes, seconds] = endTimeStr.split(":").map(Number);
  const now = new Date();
  const endTime = new Date(now.getFullYear(), now.getMonth(), now.getDate(), hours, minutes, seconds);

  const statusIndicator = document.getElementById('status-indicator')
  statusIndicator.classList.add('functional')
  document.getElementById('status-indicator-text').innerHTML = `EM SERVIÇO`

  function updateCountdown() {
    const now = new Date();
    let remainingTime = endTime - now;

    if (remainingTime > 0) {
      const hoursLeft = Math.floor(remainingTime / (1000 * 60 * 60));
      const minutesLeft = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
      const secondsLeft = Math.floor((remainingTime % (1000 * 60)) / 1000);

      document.getElementById('remaining-time').innerHTML = (`${hoursLeft}h ${minutesLeft}m ${secondsLeft}s`);
    } else {
      document.getElementById('status-indicator-text').innerHTML = `DESCANSO`
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
