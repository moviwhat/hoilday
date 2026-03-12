from flask import Flask, render_template, request, jsonify, send_file, abort
import os
from services.api_service import APIService

app = Flask(__name__)
api_service = APIService()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/photo/<path:filename>')
def get_photo(filename):
    try:
        if os.path.exists(filename):
            return send_file(filename)
        else:
            return abort(404)
    except Exception:
        return abort(404)

@app.route('/api/load-data', methods=['GET'])
def load_local_data():
    try:
        config_data = api_service.concurrent_service.load_data_config()
        return jsonify({
            'success': True,
            'data': config_data.get('data', []),
            'styles': config_data.get('style', ['文艺']),
            'default_style': config_data.get('default_style', '文艺'),
            'system_prompt': config_data.get('system_prompt', '')
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/concurrent', methods=['POST'])
def send_concurrent_requests():
    try:
        data = request.get_json() or {}
        user_prompt = data.get('userPrompt', '')
        style = data.get('style', '文艺')
        system_prompt = data.get('systemPrompt', '')
        results = api_service.send_concurrent_requests(
            user_prompt=user_prompt,
            style=style,
            system_prompt=system_prompt
        )
        return jsonify({
            'success': True,
            'total': len(results),
            'results': results
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
