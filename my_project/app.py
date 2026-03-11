from flask import Flask, render_template, request, jsonify
from services.api_service import APIService

app = Flask(__name__)
api_service = APIService()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/load-data', methods=['GET'])
def load_local_data():
    try:
        data_items = api_service.concurrent_service.load_data_config()
        return jsonify({
            'success': True,
            'data': data_items
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/concurrent', methods=['POST'])
def send_concurrent_requests():
    try:
        results = api_service.send_concurrent_requests()
        return jsonify({
            'success': True,
            'total': len(results),
            'results': results
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
