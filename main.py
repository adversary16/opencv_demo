import signal
from cam import cam, process_video, change_detector as cd
from ml import ml

def make_graceful_shutdown(cam: cam.Cam):
    def killer(*args):
        cam.stop()
        exit(0)
    return killer


camera = cam.Cam()
kill_fn = make_graceful_shutdown(camera)

signal.signal(signal.SIGINT, kill_fn)
signal.signal(signal.SIGTERM, kill_fn)

change_detector = cd.ChangeDetector(30)
object_detector = ml.MlService()
change_detector.on_change = object_detector.process
camera.start(5, change_detector.process)

print(camera.port)
