let sourceType = 'paper';
const API_BASE = 'https://recosearch.co.kr';

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

  fetch(API_BASE + url)
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


function setSourceType(type) {
  window.setSourceType = setSourceType;
  sourceType = type;
  const title = document.querySelector('h1');
  if (title) title.textContent = sourceType === 'patent' ? '🔍 특허 추천 시스템' : '📚 DBpia 인기 논문 추천 시스템';
  document.getElementById('result').innerHTML = '';
}


// 특허 결과 렌더링
function renderPatents(items) {
  const container = document.getElementById('result');
  container.innerHTML = '';
  if (!items.length) {
    container.textContent = '조회된 특허가 없습니다.';
    return;
  }
  const html = items.map(item => {
    const link = item.link || '#';
    return `
      <div class="paper">
        <strong>${item.title}</strong>
        <em>출원인: ${item.applicant}</em>
        <p>출원일: ${item.application_date}</p>
        <a href="${link}" target="_blank">상세 보기</a>
      </div>
    `;
  }).join('');
  container.innerHTML = html;
}


// 버튼 클릭 시 소스 타입 전환
document.getElementById('btn-paper').addEventListener('click', () => setSourceType('paper'));
document.getElementById('btn-patent').addEventListener('click', () => setSourceType('patent'));
