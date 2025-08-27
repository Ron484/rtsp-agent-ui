from flask import Flask, render_template_string, request
import subprocess

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RTSP to MediaMTX Agent</title>
    <style>
         body {
            font-family: Arial, sans-serif;
            background-color: #f8f9fa;
            margin: 0;
            padding: 0;
        }
        header {
            background-color: #C4C4C4;
            color: white;
            padding: 15px;
            text-align: center;
        }
        .container {
            max-width: 600px;
            margin: 40px auto;
            background: #fff;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h2 {
            margin-top: 0;
        }
        label {
            font-weight: bold;
        }
        input[type="text"] {
            width: 100%;
            padding: 8px;
            margin-top: 5px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        input[type="submit"] {
            background-color: #C4C4C4;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
        .message {
            margin-top: 20px;
            padding: 10px;
            border-radius: 4px;
            background-color: #e9f7ef;
            color: #2e7d32;
        }
    </style>
</head>
<body>
    <header>
        <h1>RTSP to MediaMTX Agent</h1>
    </header>
    <div class="container">
        <h2>Start Streaming</h2>
       <form method="post">
            <label for="rtsp_url">RTSP URL:</label>
            <input type="text" id="rtsp_url" name="rtsp_url" placeholder="rtsp://..." required>
            <input type="submit" value="Send">
        </form>
        {% if message %}
            <div class="message">{{ message }}</div>
        {% endif %}
    </div>
</body>
</html>
"""


SERVER_IP = "16.24.201.25"  # MediaMTX server
DEFAULT_STREAM_NAME = "camera1" #use deffrent one for defferent camera

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        rtsp_url = request.form["rtsp_url"]
        rtmp_url = f"rtmp://{SERVER_IP}/live/{DEFAULT_STREAM_NAME}"
        
        cmd = [
            "ffmpeg",
            "-rtsp_transport", "tcp",
            "-i", rtsp_url,
            "-c:v", "copy",
            "-c:a", "aac",
            "-f", "flv",
            rtmp_url
        ]
        subprocess.Popen(cmd)
        message = f"Streaming started to {rtmp_url}"
    return render_template_string(HTML, message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
