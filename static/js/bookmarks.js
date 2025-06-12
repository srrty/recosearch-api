// bookmarks.js

// ==============================
// 🔹 즐겨찾기 목록 불러오기
// ==============================
// bookmarks.js

async function loadBookmarks() {
  const token = localStorage.getItem("token");
  if (!token) return;
  const ul = document.getElementById("bm-list");
  ul.innerHTML = '<li>불러오는 중...</li>';
  try {
    const list = await apiGet("/bookmarks/");
    ul.innerHTML = list.length
      ? list.map(bm => {
          // 1) 서버가 내려주는 paper_link 또는 link 필드 우선 사용
          let href = bm.paper_link || bm.link;

          // 2) 위가 없으면, 키 이름에 'link'가 포함된 문자열 프로퍼티 찾기
          if (!href) {
            for (const key of Object.keys(bm)) {
              if (/link/i.test(key) && typeof bm[key] === 'string') {
                href = bm[key];
                break;
              }
            }
          }

          // 3) 여전히 없으면 api_link에서 NODE#### 추출
          if (!href && bm.api_link) {
            const m = bm.api_link.match(/id=(NODE\d+)/);
            if (m) {
              href = `https://www.dbpia.co.kr/journal/articleDetail?nodeId=${m[1]}`;
            }
          }

          // 4) 최후의 수단: paper_id fallback (이 경우 앞자리 0이 손실될 수 있음)
          if (!href) {
            href = `https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE${bm.paper_id}`;
          }

          return `<li>
  <span class="bm-title">${bm.title}</span>
  <span class="bm-info">ID: ${bm.id} <a href="${href}" target="_blank" rel="noopener">상세 보기</a></span>
  <button class="bm-remove" data-bmid="${bm.id}">✖</button>
</li>`;
        }).join("")
      : '<li>즐겨찾기한 논문이 없습니다.</li>';
  } catch (err) {
    console.error("📌 [bookmarks.js] 즐겨찾기 불러오기 실패:", err);
    ul.innerHTML = '<li>불러오기 오류</li>';
  }
}

// 즐겨찾기 해제 로직 (변경 없음)
document.getElementById('bm-list')?.addEventListener('click', async function (e) {
  if (!e.target.classList.contains('bm-remove')) return;
  const bmid = e.target.dataset.bmid;
  try {
    await fetch(API_BASE + `/bookmarks/${bmid}`, {
      method: "DELETE",
      headers: {
        "Authorization": "Bearer " + localStorage.getItem("token")
      }
    });
    e.target.closest('li').remove();
  } catch (err) {
    console.error("즐겨찾기 삭제 오류:", err);
    alert('삭제 중 오류가 발생했습니다.');
  }
});

// ==============================
// 🔹 즐겨찾기 모달 내 해제
// ==============================
document.getElementById('bm-list')?.addEventListener('click', async function (e) {
  if (!e.target.classList.contains('bm-remove')) return;
  const bmid = e.target.dataset.bmid;
  try {
    await fetch(API_BASE + `/bookmarks/${bmid}`, {
      method: "DELETE",
      headers: {
        "Authorization": "Bearer " + localStorage.getItem("token")
      }
    });
    e.target.closest('li').remove();
  } catch (err) {
    alert('삭제 중 오류가 발생했습니다.');
  }
});
