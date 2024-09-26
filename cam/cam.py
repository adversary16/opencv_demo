from cv2 import typing, VideoCapture, imshow, imwrite, waitKey, CAP_PROP_FPS, destroyAllWindows
from utils import queuefy
from typing import Callable, Any
from time import sleep

def noop(*args):
    return

class Cam:
    port: int = -1
    is_running: bool = False

    def __init__(self):
        self.port = Cam.get_cam_port()
        self.cam = Cam.get_cam_instance(self.port)
    
    @staticmethod
    def get_cam_port() -> int :
        max_tries: int = 16
        found_port: int = -1
        for i in range(max_tries):
            try:
                cam = VideoCapture(i)
                if cam.isOpened():
                    found_port = i
                    cam.release()
                    break
            except:
                print(('camera not found', i))
        if found_port == -1:
            raise(Exception('no cam found'))
        return found_port
    
    @staticmethod
    def get_cam_instance(port: int):
        cam = VideoCapture(port)
        return cam
    
    @staticmethod
    def set_cam_fps(cam: VideoCapture, fps: float):
        cam.set(CAP_PROP_FPS, fps)
        real_fps = cam.get(CAP_PROP_FPS)
        return fps == real_fps

    @staticmethod
    def capture(cam: VideoCapture, fps: float):
        capture_pause_msec = -1
        if not Cam.set_cam_fps(cam, fps):
            capture_pause_msec = 1 / fps
        while cam.isOpened():
            result, image = cam.read()
            if not result:
                raise(Exception('failed to capture'))
            if (capture_pause_msec >= 0):
                sleep(capture_pause_msec)
            return image

    def start(self, fps: float, processor_fn: Callable[[ typing.MatLike], Any]):
        q = queuefy.queuefy(self.capture, self.cam.isOpened, args=[self.cam, fps])
        while self.cam.isOpened():
            f = q.get()
            processor_fn(f)
            q.task_done()


    def stop(self):
        self.is_running = False