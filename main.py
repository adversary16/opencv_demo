from cam import cam, process_video
from time import sleep

# cam_port = cam.get_cam_port()
# cam.get_image(cam_port)

camera = cam.Cam()
def l(*args):
    print('gello', flush=True)
camera.start(30, process_video.contour)
print(camera.port)
