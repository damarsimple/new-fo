from flask import Flask, render_template, Response
import cv2
from PIL import Image
import io

app = Flask(__name__)

camera = cv2.VideoCapture(1)

@app.route('/')
def index():
  """Video streaming home page."""
  return render_template('index.html')

def gen():
  """Video streaming generator function."""
  while True:
    rval, frame = camera.read()
    if rval:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # convert color space
        img = Image.fromarray(frame)
        file_object = io.BytesIO()
        img.save(file_object, 'JPEG')
        file_object.seek(0)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + file_object.read() + b'\r\n')

@app.route('/video_feed')
def video_feed():
  """Video streaming route. Put this in the src attribute of an img tag."""
  return Response(gen(),
                  mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, threaded=True)