from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

BOT_TOKEN = '8133949217:AAGpM5tJlJPsySZTzRHXGimRWzvY7SMmo5s'
CHAT_ID = '7968926183'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        file.save(file.filename)
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        with open(file.filename, 'rb') as f:
            r = requests.post(url, data={'chat_id': CHAT_ID}, files={'document': f})
        os.remove(file.filename)
        result = r.json()
        try:
            file_id = result['result']['document']['file_id']
            get_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
            file_path = requests.get(get_url).json()['result']['file_path']
            download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
            return f"✅ Uploaded! <a href='{download_url}' target='_blank'>Download Link</a>"
        except:
            return "❌ Error: file link not found"
    return "No file uploaded"
