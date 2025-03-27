from flask import Flask, render_template, request, redirect, url_for
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form.get('url')

    if video_url:
        try:
            # إعداد خيارات yt-dlp
            ydl_opts = {
                'outtmpl': 'downloads/%(title)s.%(ext)s',  # تعيين مكان حفظ الفيديو
                'format': 'best',  # تنزيل أفضل جودة ممكنة
            }
            
            # تحميل الفيديو باستخدام yt-dlp
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            
            return f"تم تنزيل الفيديو بنجاح من الرابط: {video_url}"

        except Exception as e:
            return f"حدث خطأ أثناء تنزيل الفيديو: {str(e)}"
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
