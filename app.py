from flask import Flask, render_template, request
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    quality = request.form.get('quality')
    format_choice = request.form.get('format')

    # تحديد مسار FFmpeg
    ffmpeg_location = "C:/ffmpeg/bin"  # تأكد من أن هذا هو المسار الصحيح لـ FFmpeg

    # إعدادات yt-dlp
    ydl_opts = {
        'format': 'bestaudio+bestaudio',  # تحديد الجودة الأعلى للصوت والفيديو
        'extractaudio': False,  # لا نحتاج لاستخراج الصوت فقط
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # تحديد المسار لحفظ الملفات
        'ffmpeg_location': ffmpeg_location,  # تمرير مسار FFmpeg
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': format_choice
        }]
    }

    try:
        # تنزيل الفيديو باستخدام yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
        return f"تم تحميل الفيديو بنجاح: {info_dict['title']} بصيغة {format_choice}!"
    except Exception as e:
        return f"حدث خطأ أثناء تحميل الفيديو: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
