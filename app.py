from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('url')

    if not video_url:
        return "يرجى إدخال رابط الفيديو!", 400

    try:
        # تحديد مسار حفظ الملفات داخل /tmp/
        download_path = "/tmp/%(title)s.%(ext)s"

        ydl_opts = {
            'outtmpl': download_path,  # حفظ الفيديو في /tmp/
            'format': 'best'
        }

        # تحميل الفيديو باستخدام yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            file_title = info_dict.get('title', 'video')  # استخراج عنوان الفيديو
            file_ext = info_dict.get('ext', 'mp4')  # استخراج الامتداد
            file_path = f"/tmp/{file_title}.{file_ext}"

        # التحقق من وجود الملف وإرساله للمستخدم
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)

        return "حدث خطأ أثناء تنزيل الفيديو!", 500

    except Exception as e:
        return f"حدث خطأ: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
