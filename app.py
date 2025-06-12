from flask import Flask, request, render_template, jsonify
import requests
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
BOT_TOKEN = '8133949217:AAGpM5tJlJPsySZTzRHXGimRWzvY7SMmo5s'
CHAT_ID = '7968926183'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    with open(filepath, 'rb') as f:
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendDocument'
        response = requests.post(url, data={'chat_id': CHAT_ID}, files={'document': f})

    os.remove(filepath)

    if response.ok:
        file_info = response.json()
        file_id = file_info['result']['document']['file_id']
        file_path_resp = requests.get(
            f'https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}'
        )
        file_path = file_path_resp.json()['result']['file_path']
        direct_link = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}'
        return jsonify({'download_link': direct_link})
    else:
        return jsonify({'error': 'Telegram upload failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)
