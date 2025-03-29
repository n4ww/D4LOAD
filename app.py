import os
import subprocess
from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp

app = Flask(__name__)

# مجلد حفظ الملفات
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# مسار ملف الكوكيز
COOKIES_FILE = "cookies.txt"  # افترض أن ملف الكوكيز تم تصديره هنا

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_video_info', methods=['POST'])
def get_video_info():
    """ جلب معلومات الفيديو والجودات المتاحة """
    url = request.form.get('url')

    if not url:
        return jsonify({'error': '❌ يرجى إدخال رابط الفيديو'}), 400

    try:
        ydl_opts = {
            'quiet': True,
            'cookiefile': COOKIES_FILE  # إضافة ملف الكوكيز
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = []
            for fmt in info['formats']:
                if fmt.get('vcodec') == 'none':  # إذا كانت هذه جودة صوت فقط
                    formats.append({
                        'format_id': fmt['format_id'],
                        'ext': fmt['ext'],
                        'resolution': 'صوت فقط',
                        'filesize': fmt.get('filesize', 'غير معروف')
                    })
                else:
                    formats.append({
                        'format_id': fmt['format_id'],
                        'ext': fmt['ext'],
                        'resolution': fmt.get('resolution', 'غير معروف'),
                        'filesize': fmt.get('filesize', 'غير معروف')
                    })

        return jsonify({'title': info['title'], 'formats': formats})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download_video():
    """ تحميل الفيديو والصوت ودمجهما تلقائيًا """
    url = request.form.get('url')
    format_id = request.form.get('format_id')

    if not url or not format_id:
        return "❌ يرجى إدخال رابط الفيديو وتحديد الجودة", 400

    video_path = os.path.join(DOWNLOAD_FOLDER, "video.mp4")
    audio_path = os.path.join(DOWNLOAD_FOLDER, "audio.mp4")
    final_path = os.path.join(DOWNLOAD_FOLDER, "final_video.mp4")

    # إعداد تحميل الفيديو فقط
    ydl_opts_video = {
        'format': format_id,  # تحميل الفيديو فقط
        'outtmpl': video_path,
        'cookiefile': COOKIES_FILE  # إضافة ملف الكوكيز
    }

    # إعداد تحميل الصوت فقط
    ydl_opts_audio = {
        'format': 'bestaudio',  # تحميل أفضل جودة صوت متاحة
        'outtmpl': audio_path,
        'cookiefile': COOKIES_FILE  # إضافة ملف الكوكيز
    }

    try:
        # تحميل الفيديو
        with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
            ydl.download([url])

        # تحميل الصوت
        with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
            ydl.download([url])

        # دمج الفيديو والصوت باستخدام FFmpeg
        merge_command = [
            'ffmpeg', '-i', video_path, '-i', audio_path,
            '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental',
            '-y', final_path
        ]
        subprocess.run(merge_command, check=True)

        # إرسال الفيديو النهائي للمستخدم
        return send_file(final_path, as_attachment=True)

    except Exception as e:
        return f"❌ حدث خطأ أثناء تحميل الفيديو: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
