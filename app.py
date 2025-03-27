from flask import Flask, render_template, request, send_file
import yt_dlp  # type: ignore
import os

def download_video(url):
    # إنشاء المجلد إذا لم يكن موجودًا
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return os.path.abspath(filename)  # استخدام المسار المطلق

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    try:
        filepath = download_video(url)
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return f"Error: {e}" 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
    
import logging

logging.basicConfig(level=logging.DEBUG)
