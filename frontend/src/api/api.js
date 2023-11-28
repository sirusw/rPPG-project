import cookie from 'react-cookies';
async function sendApiRequest(param, value) {
    const url = 'http://localhost:8000/api/config'; // Correctly specify the API endpoint URL
    const cookieValue = cookie.load('csrftoken');
    console.log("cookieValue", cookieValue);
    const payload = {
      param: param,
      value: value
    };
  
    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          let cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      console.log("cookieValue", cookieValue);
      return cookieValue;
    }
  
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Include the CSRF token in the request header
          'X-CSRFToken': cookieValue
        },
        body: JSON.stringify(payload),
        credentials: 'include'
      });
  
      if (!response.ok) {
        throw new Error('Request failed');
      }
  
      const data = await response.json();
      return data;
    } catch (error) {
      throw new Error(error);
    }
  }

  export function setCsrfToken() {
    return fetch('http://localhost:8000/api/set-csrf-token/', {credentials: 'include'})
      .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
      })
      .catch(error => console.error('Error:', error));
  }
  
  export default sendApiRequest;
