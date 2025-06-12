from flask import Flask, request, render_template
import requests
import os

# === Replace with your token and chat ID ===
BOT_TOKEN = "8133949217:AAGpM5tJlJPsySZTzRHXGimRWzvY7SMmo5s"
CHAT_ID = "7968926183"

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    link = None
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # Upload to Telegram
            with open(filepath, "rb") as f:
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
                data = {"chat_id": CHAT_ID}
                files = {"document": f}
                response = requests.post(url, data=data, files=files).json()

            os.remove(filepath)

            try:
                file_id = response["result"]["document"]["file_id"]
                getfile = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}").json()
                file_path = getfile["result"]["file_path"]
                link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
            except Exception as e:
                link = "Upload failed or wrong token/chat_id."

    return render_template("index.html", link=link)

if __name__ == "__main__":
    app.run(debug=True)
