const form = document.getElementById('search-form');
const input = document.getElementById('keyword');
const resultsEl = document.getElementById('results');
const recsEl = document.getElementById('recs');
const loadingEl = document.getElementById('loading');

form.addEventListener('submit', async e => {
  e.preventDefault();
  const keyword = input.value.trim();
  if (!keyword) return;

  resultsEl.innerHTML = '';
  recsEl.innerHTML = '';
  loadingEl.hidden = false;

  try {
    const res = await fetch('/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ keyword })
    });
    const data = await res.json();

    data.results.forEach(doc => {
      const li = document.createElement('li');
      li.innerHTML = `<a href="${doc.link}" target="_blank">${doc.title}</a>`;
      resultsEl.appendChild(li);
    });

    data.recommendations.forEach(r => {
      const li = document.createElement('li');
      li.textContent = r;
      recsEl.appendChild(li);
    });
  } catch (err) {
    alert('검색 중 오류가 발생했습니다.');
    console.error(err);
  } finally {
    loadingEl.hidden = true;
  }
});