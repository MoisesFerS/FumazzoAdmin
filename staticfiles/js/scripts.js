/* Function that gets the csrf token from the cookies */
function getToken() {
  return document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1] || '';
}

document.getElementById('message').addEventListener('click', function(event){
  const message = document.getElementById('message');
  window.addEventListener('click', function(event) {
    if (event.target === message) {
      message.style.display = "none";
    }
  })
});

