let globalData = [];
let isProcessed = false;

async function loadData() {
    const loading = document.getElementById('loading');
    const dataList = document.getElementById('dataList');
    const processBtn = document.getElementById('processBtn');
    
    loading.style.display = 'block';
    dataList.innerHTML = '';
    
    try {
        const response = await fetch('/api/load-data', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            globalData = result.data.map(item => ({
                data_id: item.id,
                success: false,
                result: {
                    text: item.text,
                    photos: item.photos
                }
            }));
            renderDataList();
            processBtn.disabled = false;
        } else {
            alert('加载失败：' + result.error);
        }
    } catch (error) {
        alert('请求失败：' + error.message);
    } finally {
        loading.style.display = 'none';
    }
}

async function processData() {
    const processBtn = document.getElementById('processBtn');
    const loading = document.getElementById('loading');
    
    if (isProcessed) {
        alert('已经处理过了，如需重新处理请刷新页面');
        return;
    }
    
    loading.style.display = 'block';
    processBtn.disabled = true;
    processBtn.textContent = '处理中...';
    
    try {
        const response = await fetch('/api/concurrent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const result = await response.json();
        
        if (result.success) {
            globalData = result.results;
            isProcessed = true;
            renderDataList();
            processBtn.textContent = '处理完成';
        } else {
            alert('处理失败：' + result.error);
            processBtn.disabled = false;
            processBtn.textContent = '开始处理';
        }
    } catch (error) {
        alert('请求失败：' + error.message);
        processBtn.disabled = false;
        processBtn.textContent = '开始处理';
    } finally {
        loading.style.display = 'none';
    }
}

function renderDataList() {
    const dataList = document.getElementById('dataList');
    dataList.innerHTML = '';
    
    globalData.forEach((item, index) => {
        const dataItem = document.createElement('div');
        dataItem.className = 'data-item';
        
        let statusClass = 'status-pending';
        let statusText = '待处理';
        
        if (isProcessed) {
            statusClass = item.success ? 'status-success' : 'status-error';
            statusText = item.success ? '成功' : '失败';
        }
        
        let photosHtml = '';
        if (item.result && item.result.photos) {
            photosHtml = '<div class="photos-container">';
            item.result.photos.forEach(photo => {
                photosHtml += `
                    <div class="photo-item">
                        <img src="${photo.url}" alt="Photo ${photo.id}" onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22><text y=%2250%%22 x=%2250%%22 text-anchor=%22middle%22>图片加载失败</text></svg>'">
                    </div>
                `;
            });
            photosHtml += '</div>';
        }
        
        let originalText = '';
        let resultText = '';
        
        if (item.result && item.result.text) {
            originalText = item.result.text;
        }
        
        if (isProcessed && item.success && item.result && item.result.generated_text) {
            resultText = `
                <div class="text-block result-text">
                    <div class="text-label">请求返回的文案</div>
                    <div class="text-content">${item.result.generated_text}</div>
                </div>
            `;
        } else if (isProcessed && !item.success) {
            resultText = `
                <div class="text-block error-text">
                    <div class="text-label">错误信息</div>
                    <div class="text-content">${item.error || '未知错误'}</div>
                </div>
            `;
        }
        
        dataItem.innerHTML = `
            <div class="data-item-header">
                <span class="data-item-id">数据项 #${item.data_id || index + 1}</span>
                <span class="data-item-status ${statusClass}">${statusText}</span>
            </div>
            ${photosHtml}
            <div class="text-section">
                <div class="text-block original-text">
                    <div class="text-label">原始文案</div>
                    <div class="text-content">${originalText || '无'}</div>
                </div>
                ${resultText}
            </div>
        `;
        
        dataList.appendChild(dataItem);
    });
}

window.onload = function() {
    loadData();
};
