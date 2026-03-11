async function callAPI() {
    const inputData = document.getElementById('inputData').value;
    const resultDiv = document.getElementById('result');
    const submitBtn = document.getElementById('submitBtn');
    
    if (!inputData.trim()) {
        alert('请输入数据');
        return;
    }
    
    submitBtn.disabled = true;
    submitBtn.textContent = '处理中...';
    resultDiv.innerHTML = '<p>正在调用服务...</p>';
    
    try {
        const response = await fetch('/api/call', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ data: inputData })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            resultDiv.innerHTML = '<pre>' + JSON.stringify(result, null, 2) + '</pre>';
        } else {
            resultDiv.innerHTML = '<p style="color: red;">错误: ' + result.error + '</p>';
        }
    } catch (error) {
        resultDiv.innerHTML = '<p style="color: red;">请求失败: ' + error.message + '</p>';
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = '提交';
    }
}
