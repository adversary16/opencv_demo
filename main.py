import signal
from cam import cam, process_video
from time import sleep

def make_graceful_shutdown(cam: cam.Cam):
    def killer(*args):
        cam.stop()
        exit(0)
    return killer
camera = cam.Cam()
kill_fn = make_graceful_shutdown(camera)

signal.signal(signal.SIGINT, kill_fn)
signal.signal(signal.SIGTERM, kill_fn)

camera.start(30, process_video.contour)

print(camera.port)
