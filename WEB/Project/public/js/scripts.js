"use strict"

document.addEventListener('DOMContentLoaded', async () => {
  const searchQuery = new URLSearchParams(window.location.search).get('q');

  const container = document.getElementById('animeContainer');
  const statusDiv = document.getElementById('searchStatus');

  if (!searchQuery) {
    if (container) container.innerHTML = '<p class="placeholder">Не указан поисковый запрос.</p>';
    return;
  }

  if (statusDiv) statusDiv.innerHTML = `<p>Ищем аниме по запросу: <b>${searchQuery}</b>...</p>`;
  if (container) container.innerHTML = '<div class="loader"></div><p class="placeholder">Загрузка...</p>';





  try {
    const response = await fetch(`/api/search?q=${encodeURIComponent(searchQuery)}`);
    
    if (!response.ok) {
      throw new Error(`Ошибка сервера: ${response.status}`);
    }
    const animeList = await response.json();


    if (animeList && animeList.length > 0) {
      if (statusDiv) statusDiv.innerHTML = `<p style="margin-top: 10px">Найдено аниме: ${animeList.length}</p>`;
      renderAnime(animeList);
    } else {
      if (container) container.innerHTML = '<p class="placeholder">Аниме по вашему запросу не найдено.</p>';
    }
  } catch (error) {
      console.error('Ошибка при запросе:', error);
      if (container) container.innerHTML = `<p class="placeholder">Ошибка при загрузке данных: ${error.message}</p>`;
      if (statusDiv) statusDiv.innerHTML = '<p class="error">Не удалось выполнить поиск.</p>';
  }
});



function renderAnime(animeList) {
  const container = document.getElementById('animeContainer');
  if (!container) return;
  
  container.innerHTML = '';
  animeList.forEach((anime) => {
    const card = document.createElement('div');
    card.className = 'anime-card';
    

    let imageUrl = 'https://placehold.co/225x319?text=No+Image'; // Заглушка
    if (anime.image && anime.image.original) {
      imageUrl = `https://shikimori.io${anime.image.original}`;
    }
    card.innerHTML = `
      <img class="anime-cover" src="${imageUrl}" alt="Постер ${anime.russian}">
      <div class="anime-score">⭐ ${anime.score}</div>
      <div class="info">
        <div class="title">${anime.russian || anime.name}</div>
        <p class="subTitle">${anime.name}</p>
        <div class="anime-info">
          <div class="anime-type">${anime.kind}</div>
          <div class="episode">${anime.episodes} эп.</div>
        </div>
        
      </div>
    `;
    container.appendChild(card);
  });
}
