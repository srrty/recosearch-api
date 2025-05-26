// 검색 버튼 이벤트 핸들러
document.getElementById('searchBtn').addEventListener('click', () => {
  const year     = document.getElementById('yearInput').value;
  const month    = document.getElementById('monthInput').value;
  const category = document.getElementById('categorySelect').value;
  const query    = document.getElementById('searchQuery').value;

  let url = `/recommend?category=${category}`;
  if (year && month) {
    url += `&pyear=${year}&pmonth=${month}`;
  }
  if (query) {
    url += `&query=${encodeURIComponent(query)}`;
  }

  fetch(url)
    .then(res => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    })
    .then(data => renderResults(data.recommendations))
    .catch(err => console.error('검색 오류:', err));
});

// 결과 렌더링 함수
function renderResults(items) {
  const container = document.getElementById('results');
  container.innerHTML = '';
  if (!items.length) {
    container.textContent = '논문이 없습니다.';
    return;
  }
  items.forEach(doc => {
    const card = document.createElement('div');
    card.className = 'paper-card';
    card.innerHTML = `
      <h3>${doc.title}</h3>
      <p>Authors: ${doc.authors.map(a => a.name).join(', ')}</p>
      <p>Journal: ${doc.publication.name}</p>
      <a href="${doc.link_url}" target="_blank">원문 보기</a>
    `;
    container.appendChild(card);
  });
}