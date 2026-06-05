
import express from 'express';
import path from 'path';
import fs from 'fs';
import axios from 'axios';

const app = express();

app.use(express.json());
app.use(express.static(path.join(import.meta.dirname,'public')));

app.get('/', (req,res)=>{
  res.sendFile(path.join(import.meta.dirname,'html','index.html'))
})
app.get('/catalog', (req,res)=>{
  res.sendFile(path.join(import.meta.dirname,'html','catalog.html'))
})
app.get('/about', (req,res)=>{
  res.sendFile(path.join(import.meta.dirname,'html','about.html'))
})

app.get('/top', (req, res) => {
    const template = fs.readFileSync(path.join(import.meta.dirname,'html','top.html'), 'utf8');
    const items = JSON.parse(fs.readFileSync(path.join(import.meta.dirname,'public','data.json'), 'utf8'));

    const top10 = items.sort((a, b) => (b.score || 0) - (a.score || 0)).slice(0, 10);

    let itemsHtml = '';
    top10.forEach((anime, idx) => {
        itemsHtml += `
        <div class="anime-card">
            <img class="anime-cover" src="${anime.image}" alt="Постер ${anime.russian}">
            <div class="anime-score">⭐ ${anime.score}</div>
            <div class="info">
              <div class="title">${anime.russian || anime.title}</div>
              <p class="subTitle">${anime.title}</p>
              <div class="anime-info">
                <div class="anime-type">${anime.kind}</div>
                <div class="episode">${anime.episodes} эп.</div>
              </div>
              
            </div>
          </div>
        `;
    });



    const finalHtml = template.replace('%items%', itemsHtml);
    res.send(finalHtml);
});









app.get('/api/search', async (req, res) => {
  const userQuery = req.query.q;
  try {
    const apiUrl = `https://shikimori.io/api/animes/search?q=${encodeURIComponent(userQuery)}`;
    console.log(`запрос к Shikimori: ${apiUrl}`);

    const response = await axios.get(apiUrl, {timeout: 10000});

    // console.log(`# получено ${response.data.length} результатов.`);
    res.json(response.data);

  } catch (error) {
    console.error('# Ошибка при запросе к Shikimori:');
    
    console.error(`   ${error.message}`);
    res.status(500).json({ error: 'Не удалось получить данные от Shikimori.' });
  }
});




app.post('/api/form',async (req, res) => {
  const { name, email, message } = req.body;

  if (!email.includes('@')) {
    return res.status(400).json({ success: false, error: 'Введите корректный email' });
  }


   const feedbackEntry = {name,email,message, date: new Date().toString()};

   const filePath = path.join(path.join(import.meta.dirname, '/public/log'), 'form.json');


    try{
      
      let feedbacks = [];
    
      try {
        const fileContent = await fs.promises.readFile(filePath, 'utf8');
          feedbacks = JSON.parse(fileContent);
      } catch (err) {
          feedbacks = [];
        }
        
        feedbacks.push(feedbackEntry);

      
        await fs.promises.writeFile(filePath, JSON.stringify(feedbacks, null, 2));
        return res.json({ success: true, message: 'Сообщение получено.' });
            
    } catch (err) {
        return res.status(500).json({ success: false, error: 'Не удалось' });
    }
    
    

});












app.listen(3000, () => {
  console.log(`🚀 Сервер запущен: http://localhost:3000`);
});