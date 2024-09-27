import numpy as np
import cv2 as cv
import typing

def noop(*args):
    return



class ChangeDetector:
    def __init__(self):
        self.on_change:typing.Callable=noop
        self.prev_segs=[]

    
    def segment_frame(self, frame: cv.typing.MatLike, h_parts: int, w_parts: int):
        fh, fw, *_ = frame.shape
        chunk_size_h = fh // h_parts
        chunk_size_w = fw // w_parts
        out_segments = []
        current_h_part = 0
        while current_h_part < h_parts:
            current_w_part = 0
            while current_w_part < w_parts:
                h_chunk_start = current_h_part * chunk_size_h
                h_chunk_end = h_chunk_start + chunk_size_h
                w_chunk_start = current_w_part * chunk_size_w
                w_chunk_end = w_chunk_start + chunk_size_w
                out_segments.append(frame[h_chunk_start:h_chunk_end,:][:,w_chunk_start:w_chunk_end])
                current_w_part+=1
            current_h_part += 1
        return out_segments

    def detect_change(self,
                      frame: cv.typing.MatLike,
                      change_threshold: int,
                      hor_blocks: int = 1,
                      ver_blocks: int = 1):
        """
        Parameters
        ----------
        frame : cv.typing.Matlike
            OpenCV frame to parse
        change_threshold : int
            percentage of change in a single segment that will say the block is changed
        hor_blocks : int
            number of blocks to split frame into horizontally
        ver_blocks : int
            number of blocks to split frame into vertically
        """
        max_diff = 0
        grayscale = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        _, curr_thresh = cv.threshold(grayscale, 127,255, 0, cv.THRESH_TRUNC)
        segments = self.segment_frame(curr_thresh, ver_blocks, hor_blocks)
        changed_seg_indices=[]
        if len(self.prev_segs) > 0:
            for (ind, seg) in enumerate(segments):
                diff = cv.absdiff(seg, self.prev_segs[ind])
                diff_percentage = np.count_nonzero(diff) / diff.size * 100
                if diff_percentage >= change_threshold:
                    changed_seg_indices.append(ind)
                    max_diff = max(max_diff, diff_percentage)
        self.prev_segs = segments
        return max_diff >= change_threshold, changed_seg_indices
        

    def process(self, frame: cv.typing.MatLike):
        is_changed , *_ = self.detect_change(frame, 30, 12, 12)
        src_frame = frame.copy()
        self.detected_objects=getattr(self, 'detected_objects', [])
        if is_changed:
            if not self.on_change is None:
                out_boxes, out_w, out_c = self.on_change(frame)
                current_found = []
                for index, box in enumerate(out_boxes):
                    current_found.append([box, out_c[index]])
                if len(current_found) > 0:
                    self.detected_objects = current_found
        for det in self.detected_objects:
            [ box, label] = det
            b = np.array(box, dtype=int)
            fh, fw, _ = frame.shape
            [startx, starty]= b[:2]
            [endx, endy] = b[2:]
            src_frame=cv.rectangle(src_frame, (max(starty, 0), max(startx, 0)), (min(endy, fh), min(endx, fw)), (255, 0, 0), 2)
            src_frame=cv.putText(src_frame, label, ((starty + endy) // 2, (startx + endx) //2), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0) )
        cv.imshow('im', src_frame)
        k = cv.waitKey(1)
        if k == 27:
            cv.destroyAllWindows()