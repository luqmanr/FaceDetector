from abc import ABCMeta, abstractmethod
import numpy as np

from FaceDetector.src.FaceDetector.ssd import FaceDetector as ssd

class IFaceDetector(metaclass=ABCMeta):
    """Interface for face detectors

    """
    @abstractmethod
    def detect_face_bounding_boxes_from(self, image):
        pass


class SSD(IFaceDetector):
    """Implementation of face detector using SSD architecture

    """
    def __init__(self):        
        self.ssd_detector = ssd.FaceDetector()

    def detect_face_bounding_boxes_from(self, image):
        """Returns a list of BoundingBox objects and amount of face detected

        """
        boxes, scores = self.ssd_detector.detect(image)
        face_boxes = boxes[np.argwhere(scores>0.2).reshape(-1)]
        face_scores = scores[np.argwhere(scores>0.2).reshape(-1)]

        detected_faces_amount = self._count_detected_faces(face_boxes)
        face_bounding_box_points = self._extract_face_bounding_box_points(face_boxes, detected_faces_amount)
        return face_bounding_box_points, detected_faces_amount, face_scores

    def _count_detected_faces(self, architecture_output):
        return len(architecture_output)

    def _extract_face_bounding_box_points(self, architecture_output, detected_faces_amount):
        bounding_boxes = []
        for i in range(detected_faces_amount):
            bounding_box = BoundingBox()
            bounding_box.top_left = (int(architecture_output[i][0]), int(architecture_output[i][1]))
            bounding_box.bottom_right = (int(architecture_output[i][2]), int(architecture_output[i][3]))

            bounding_boxes.append(bounding_box)
        return bounding_boxes

class BoundingBox:

    def __init__(self):
        # The corners tuple are ordered (row, col)
        # TODO consider making corners its own object
        self.top_left = (-1, -1)
        self.bottom_right = (-1, -1)
        self.width
        self.height

    @property
    def width(self):
        _, col_left = self.top_left
        _, col_right = self.bottom_right
        return col_right - col_left

    @property
    def height(self):
        # In opencv, (0,0) is at the top left
        row_top, _ = self.top_left
        row_bottom, _ = self.bottom_right
        return row_bottom - row_top

print("Loaded detector module")
