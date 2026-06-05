"use strict"

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('feedbackForm');
  const statusDiv = document.getElementById('formStatus');

  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const message = document.getElementById('message').value.trim();


    statusDiv.innerHTML = '<p class="loading">Отправка...</p>';

    try {
      const response = await fetch('/api/form', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, message })
      });

      if (!response.ok) {
        throw new Error(`Ошибка сервера: ${response.status}`);
      }

      const result = await response.json();
      if (result.success) {
        statusDiv.innerHTML = `<p class="success">${result.message}</p>`;
       
        form.reset(); 

        setTimeout(() => {
          if (statusDiv){
            statusDiv.innerHTML = '';
          }
        }, 3000);


        
      }else {
        statusDiv.innerHTML = `<p class="error" Ошибка: ${result.error}</p>`;
      }


    } catch (error) {
      console.error('Ошибка при отправке:', error);
      statusDiv.innerHTML = '<p class="error">Не удалось отправить сообщение.</p>';
    }
  });
});