let globalData = [];
let rawDataSource = [];  // 存储原始数据源，包含所有文风的文案
let isProcessed = false;
let globalSystemPrompt = '';
let currentStyle = '文艺';  // 当前选中的文风

function initStyleSelect() {
    const styleSelect = document.getElementById('styleSelect');
    const customStyle = document.getElementById('customStyle');
    
    styleSelect.addEventListener('change', function() {
        if (this.value === '自定义') {
            customStyle.style.display = 'inline-block';
        } else {
            customStyle.style.display = 'none';
            customStyle.value = '';
        }
        
        // 文风切换时更新原始文案显示
        if (!isProcessed) {
            currentStyle = this.value;
            updateTextByStyle();
        }
    });
}

function getSelectedStyle() {
    const styleSelect = document.getElementById('styleSelect');
    const customStyle = document.getElementById('customStyle');
    
    if (styleSelect.value === '自定义') {
        return customStyle.value || '文艺';
    }
    return styleSelect.value;
}

function getTextByStyle(item, style) {
    // 优先使用按文风区分的文案
    if (item.texts && item.texts[style]) {
        return item.texts[style];
    }
    // 兼容旧格式
    return item.text || '';
}

function updateTextByStyle() {
    // 根据当前文风更新 globalData 中的文案
    globalData.forEach((item, index) => {
        const rawItem = rawDataSource[index];
        if (rawItem) {
            item.result.text = getTextByStyle(rawItem, currentStyle);
        }
    });
    renderDataList();
}

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
            // 存储原始数据源
            rawDataSource = result.data;
            
            // 使用默认文风的文案初始化 globalData
            currentStyle = result.default_style || '文艺';
            
            globalData = result.data.map(item => ({
                data_id: item.id,
                success: false,
                result: {
                    text: getTextByStyle(item, currentStyle),
                    photos: item.photos
                }
            }));
            
            globalSystemPrompt = result.system_prompt || '';
            
            const styleSelect = document.getElementById('styleSelect');
            styleSelect.innerHTML = '';
            
            if (result.styles && Array.isArray(result.styles)) {
                result.styles.forEach(style => {
                    const option = document.createElement('option');
                    option.value = style;
                    option.text = style;
                    styleSelect.appendChild(option);
                });
                
                if (result.default_style) {
                    styleSelect.value = result.default_style;
                }
            }
            
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
    const exportBtn = document.getElementById('exportBtn');
    const loading = document.getElementById('loading');
    const userPrompt = document.getElementById('userPrompt').value;
    const selectedStyle = getSelectedStyle();
    
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
            },
            body: JSON.stringify({
                userPrompt: userPrompt,
                style: selectedStyle,
                systemPrompt: globalSystemPrompt
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            globalData = result.results;
            isProcessed = true;
            renderDataList();
            processBtn.textContent = '处理完成';
            exportBtn.disabled = false;
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
                const photoUrl = '/api/photo/' + encodeURIComponent(photo.url);
                photosHtml += `
                    <div class="photo-item" onclick="showImagePreview('${photoUrl}', '图片 ${photo.id}')">
                        <img src="${photoUrl}" alt="Photo ${photo.id}" onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22><text y=%2250%%22 x=%2250%%22 text-anchor=%22middle%22>图片加载失败</text></svg>'">
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
            <div class="data-item-content">
                <div class="data-item-left">
                    ${photosHtml}
                </div>
                <div class="data-item-center">
                    <div class="text-section">
                        <div class="text-block original-text">
                            <div class="text-label">原始文案</div>
                            <div class="text-content">${originalText || '无'}</div>
                        </div>
                    </div>
                </div>
                <div class="data-item-right">
                    <div class="text-section">
                        ${resultText || '<div class="text-block" style="border-left: 4px solid #999;"><div class="text-label">等待处理</div><div class="text-content" style="color: #999;">点击"开始处理"按钮生成文案</div></div>'}
                    </div>
                </div>
            </div>
        `;
        
        dataList.appendChild(dataItem);
    });
}

async function exportToExcel() {
    if (globalData.length === 0) {
        alert('没有数据可导出');
        return;
    }
    
    const exportBtn = document.getElementById('exportBtn');
    exportBtn.disabled = true;
    exportBtn.textContent = '导出中...';
    
    try {
        const response = await fetch('/api/export-excel', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                results: globalData
            })
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'copywriting_result_' + new Date().toISOString().slice(0, 10) + '.xlsx';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        } else {
            alert('导出失败');
        }
    } catch (error) {
        alert('导出失败：' + error.message);
    } finally {
        exportBtn.disabled = false;
        exportBtn.textContent = '导出 Excel';
    }
}

window.onload = function() {
    initStyleSelect();
    initImagePreviewModal();
    loadData();
};

// 图片预览模态框功能
let currentScale = 1;
let currentX = 0;
let currentY = 0;
let isDragging = false;
let startX, startY;
let lastTouchDistance = 0;
let modalImg, modalImageContainer;

function initImagePreviewModal() {
    const modal = document.getElementById('imagePreviewModal');
    modalImg = document.getElementById('previewImage');
    modalImageContainer = document.getElementById('modalImageContainer');
    const closeBtn = document.getElementsByClassName('modal-close')[0];
    
    // 点击关闭按钮关闭模态框
    closeBtn.onclick = function() {
        modal.style.display = "none";
        resetZoom();
    };
    
    // 点击模态框背景关闭
    modal.onclick = function(event) {
        if (event.target === modal || event.target === modalImageContainer) {
            modal.style.display = "none";
            resetZoom();
        }
    };
    
    // ESC 键关闭模态框
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && modal.style.display === 'block') {
            modal.style.display = "none";
            resetZoom();
        }
    });
    
    // 滚轮缩放
    modalImageContainer.addEventListener('wheel', function(e) {
        e.preventDefault();
        const delta = e.deltaY > 0 ? -0.15 : 0.15;
        applyZoom(delta);
    });
    
    // 鼠标拖拽
    modalImageContainer.addEventListener('mousedown', function(e) {
        if (e.button === 0) {
            isDragging = true;
            startX = e.clientX - currentX;
            startY = e.clientY - currentY;
            modalImageContainer.style.cursor = 'grabbing';
        }
    });
    
    document.addEventListener('mousemove', function(e) {
        if (isDragging) {
            e.preventDefault();
            currentX = e.clientX - startX;
            currentY = e.clientY - startY;
            applyTransform();
        }
    });
    
    document.addEventListener('mouseup', function() {
        isDragging = false;
        modalImageContainer.style.cursor = 'grab';
    });
    
    // 双击重置
    modalImageContainer.addEventListener('dblclick', function() {
        resetZoom();
    });
    
    // 触摸事件 - 双指缩放
    modalImageContainer.addEventListener('touchstart', function(e) {
        if (e.touches.length === 2) {
            lastTouchDistance = getTouchDistance(e.touches);
        } else if (e.touches.length === 1 && currentScale > 1) {
            isDragging = true;
            startX = e.touches[0].clientX - currentX;
            startY = e.touches[0].clientY - currentY;
        }
    });
    
    modalImageContainer.addEventListener('touchmove', function(e) {
        e.preventDefault();
        
        if (e.touches.length === 2) {
            const distance = getTouchDistance(e.touches);
            if (lastTouchDistance > 0) {
                const delta = (distance - lastTouchDistance) * 0.005;
                applyZoom(delta);
            }
            lastTouchDistance = distance;
        } else if (e.touches.length === 1 && isDragging) {
            currentX = e.touches[0].clientX - startX;
            currentY = e.touches[0].clientY - startY;
            applyTransform();
        }
    });
    
    modalImageContainer.addEventListener('touchend', function(e) {
        if (e.touches.length < 2) {
            lastTouchDistance = 0;
        }
        if (e.touches.length === 0) {
            isDragging = false;
        }
    });
}

function getTouchDistance(touches) {
    const dx = touches[0].clientX - touches[1].clientX;
    const dy = touches[0].clientY - touches[1].clientY;
    return Math.sqrt(dx * dx + dy * dy);
}

function applyZoom(delta) {
    currentScale = Math.max(0.5, Math.min(currentScale + delta, 5));
    applyTransform();
}

function applyTransform() {
    modalImg.style.transform = `scale(${currentScale}) translate(${currentX / currentScale}px, ${currentY / currentScale}px)`;
}

function zoomInPreview() {
    applyZoom(0.3);
}

function zoomOutPreview() {
    applyZoom(-0.3);
}

function resetZoom() {
    currentScale = 1;
    currentX = 0;
    currentY = 0;
    applyTransform();
}

function showImagePreview(imageSrc, caption = '') {
    const modal = document.getElementById('imagePreviewModal');
    const captionText = document.getElementById('caption');
    
    resetZoom();
    modal.style.display = "block";
    modalImg.src = imageSrc;
    captionText.innerHTML = caption || '图片预览';
}
