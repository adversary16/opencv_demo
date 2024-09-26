import numpy as np
import cv2 as cv
import typing

def noop(*args):
    return



class ChangeDetector:
    def __init__(self):
        self.prev_frame=np.zeros(shape=[480, 640], dtype=np.uint8)
        self.on_change:typing.Callable=noop


    def detect_change(self, frame: cv.typing.MatLike):
        _, prev_thresh = cv.threshold(self.prev_frame, 127, 255, 0)
        grayscale = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        _, curr_thresh = cv.threshold(grayscale, 127, 255, 0)
        diff = cv.absdiff(prev_thresh, curr_thresh)
        diff_percentage = np.count_nonzero(diff) / diff.size * 100
        if diff_percentage > 10:
            print("change found")
            if not self.on_change is None:
                self.on_change(frame)
        self.prev_frame = grayscale
        cv.imshow('im', frame)
        k = cv.waitKey(1)
        if k == 27:
            cv.destroyAllWindows()