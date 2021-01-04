from django.shortcuts import render
from django.http.response import StreamingHttpResponse

from camera.camera import Camera


def index(request):

    return render(request, 'camera/index.html', {})


def gen(camera):

    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video(request):

    return StreamingHttpResponse(gen(Camera()), content_type="multipart/x-mixed-replace; boundary=frame")
