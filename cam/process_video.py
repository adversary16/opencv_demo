"video processing functions"
import cv2 as cv

def show(frame: cv.typing.MatLike):
    cv.imshow('video', frame)
    k = cv.waitKey(1)
    if k == 27:
        cv.destroyAllWindows()

def contour(frame: cv.typing.MatLike):
    grayscale = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(grayscale, 127, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contoured_frame = cv.drawContours(frame, contours, -1, (0,255,0), 3 )
    show(contoured_frame)
