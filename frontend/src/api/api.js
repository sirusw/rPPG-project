import cookie from 'react-cookies';
export async function sendApiRequest(param, value) {
    const url = 'http://localhost:8000/api/config'; // Correctly specify the API endpoint URL
    const cookieValue = cookie.load('csrftoken');
    console.log("hello");
    const payload = {
      param: param,
      value: Number(value)
    };
  
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

  export async function sendSyncRequest() {
    const url = 'http://localhost:8000/api/sync'; // Correctly specify the API endpoint URL
    const cookieValue = cookie.load('csrftoken');
    const payload = {
      param: "sync",
      value: 0
    };
  
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
  
  // export default sendApiRequest;
