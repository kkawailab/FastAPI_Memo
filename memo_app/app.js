// APIのベースURL
const API_URL = 'http://localhost:8000';

// ページ読み込み時にメモ一覧を取得
document.addEventListener('DOMContentLoaded', () => {
    loadMemos();
});

// メモ一覧を読み込む
async function loadMemos() {
    try {
        const response = await fetch(`${API_URL}/memos/`);
        const memos = await response.json();
        displayMemos(memos);
    } catch (error) {
        console.error('メモの読み込みに失敗しました:', error);
        alert('メモの読み込みに失敗しました');
    }
}

// メモを表示する
function displayMemos(memos) {
    const container = document.getElementById('memoContainer');
    container.innerHTML = '';
    
    if (memos.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #888;">メモがありません</p>';
        return;
    }
    
    memos.forEach(memo => {
        const memoCard = createMemoCard(memo);
        container.appendChild(memoCard);
    });
}

// メモカードを作成する
function createMemoCard(memo) {
    const card = document.createElement('div');
    card.className = 'memo-card';
    
    const createdAt = new Date(memo.created_at).toLocaleString('ja-JP');
    const updatedAt = new Date(memo.updated_at).toLocaleString('ja-JP');
    
    card.innerHTML = `
        <h3>${escapeHtml(memo.title)}</h3>
        <p>${escapeHtml(memo.content)}</p>
        <div class="memo-meta">
            作成: ${createdAt} | 更新: ${updatedAt}
        </div>
        <div class="memo-actions">
            <button class="edit-btn" onclick="openEditModal(${memo.id})">編集</button>
            <button class="delete-btn" onclick="deleteMemo(${memo.id})">削除</button>
        </div>
    `;
    
    return card;
}

// HTMLエスケープ
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 新しいメモを作成
async function createMemo() {
    const title = document.getElementById('memoTitle').value.trim();
    const content = document.getElementById('memoContent').value.trim();
    
    if (!title || !content) {
        alert('タイトルと内容を入力してください');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/memos/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title, content })
        });
        
        if (response.ok) {
            document.getElementById('memoTitle').value = '';
            document.getElementById('memoContent').value = '';
            loadMemos();
            alert('メモを作成しました');
        } else {
            alert('メモの作成に失敗しました');
        }
    } catch (error) {
        console.error('メモの作成に失敗しました:', error);
        alert('メモの作成に失敗しました');
    }
}

// メモを削除
async function deleteMemo(id) {
    if (!confirm('このメモを削除しますか？')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/memos/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadMemos();
            alert('メモを削除しました');
        } else {
            alert('メモの削除に失敗しました');
        }
    } catch (error) {
        console.error('メモの削除に失敗しました:', error);
        alert('メモの削除に失敗しました');
    }
}

// 編集モーダルを開く
async function openEditModal(id) {
    try {
        const response = await fetch(`${API_URL}/memos/${id}`);
        const memo = await response.json();
        
        document.getElementById('editMemoId').value = memo.id;
        document.getElementById('editMemoTitle').value = memo.title;
        document.getElementById('editMemoContent').value = memo.content;
        document.getElementById('editModal').style.display = 'block';
    } catch (error) {
        console.error('メモの取得に失敗しました:', error);
        alert('メモの取得に失敗しました');
    }
}

// 編集モーダルを閉じる
function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}

// メモを更新
async function updateMemo() {
    const id = document.getElementById('editMemoId').value;
    const title = document.getElementById('editMemoTitle').value.trim();
    const content = document.getElementById('editMemoContent').value.trim();
    
    if (!title || !content) {
        alert('タイトルと内容を入力してください');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/memos/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title, content })
        });
        
        if (response.ok) {
            closeEditModal();
            loadMemos();
            alert('メモを更新しました');
        } else {
            alert('メモの更新に失敗しました');
        }
    } catch (error) {
        console.error('メモの更新に失敗しました:', error);
        alert('メモの更新に失敗しました');
    }
}

// メモを検索
async function searchMemos() {
    const query = document.getElementById('searchInput').value.trim();
    
    if (!query) {
        loadMemos();
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/memos/search/?q=${encodeURIComponent(query)}`);
        const memos = await response.json();
        displayMemos(memos);
    } catch (error) {
        console.error('メモの検索に失敗しました:', error);
        alert('メモの検索に失敗しました');
    }
}

// Enterキーで検索実行
document.getElementById('searchInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        searchMemos();
    }
});

// モーダルの外側をクリックしたら閉じる
window.onclick = function(event) {
    const modal = document.getElementById('editModal');
    if (event.target == modal) {
        closeEditModal();
    }
}