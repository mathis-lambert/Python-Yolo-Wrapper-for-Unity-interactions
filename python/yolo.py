from ultralytics import YOLO
import json
from utils import *


class Yolo:
    def __init__(self, path):
        self.model = YOLO(path)
        self.cap = None
        self.peoples = list()
        self.confidence = 0.75

    def runDetection(self, frame, mode: str = "predict", tracker: str = "./trackers/botsort.yaml"):
        """
        Run detection on a frame
        """
        # Prédire les poses
        if mode == "predict":
            results = self.model(frame, conf=self.confidence)
        elif mode == "track":
            results = self.model.track(
                frame, tracker=tracker, persist=True, conf=self.confidence)
        else:
            raise Exception("Mode must be 'predict' or 'track'")

        f = results[0].plot()

        return results, f

    def parseResults(self, results):
        """
        Parse predictions into a list of dictionaries
        """
        keypoints = results[0].keypoints.xy.tolist()
        keypoints_normalized = results[0].keypoints.xyn.tolist()

        self.peoples = list()

        for person in keypoints:
            if len(person) == 0:
                continue

            positions = {
                "nose":              person[0],
                "left_eye":          person[1],
                "right_eye":         person[2],
                "left_ear":          person[3],
                "right_ear":         person[4],
                "left_shoulder":     person[5],
                "right_shoulder":    person[6],
                "left_elbow":        person[7],
                "right_elbow":       person[8],
                "left_wrist":        person[9],
                "right_wrist":       person[10],
                "left_hip":          person[11],
                "right_hip":         person[12],
                "left_knee":         person[13],
                "right_knee":        person[14],
                "left_ankle":        person[15],
                "right_ankle":       person[16]
            }

            # yolo_data = {
            #     "left_arm_angle": round(angle(positions["left_shoulder"], positions["left_elbow"], positions["left_wrist"]), 2),
            #     "right_arm_angle": round(angle(positions["right_shoulder"], positions["right_elbow"], positions["right_wrist"]), 2),
            #     "left_shoulder_angle": round(angle(positions["left_hip"], positions["left_shoulder"], positions["left_elbow"]), 2),
            #     "right_shoulder_angle": round(angle(positions["right_hip"], positions["right_shoulder"], positions["right_elbow"]), 2),
            #     "head_inclination": get_head_inclination(positions),
            #     "body_side": self.get_side(positions),
            #     "hands_distance": self.distance(positions["left_wrist"], positions["right_wrist"]),
            #     "positions": positions,
            #     "positions_normalized": keypoints_normalized
            # }

            data = {
                "left_wrist": positions["left_wrist"],
                "right_wrist": positions["right_wrist"],
                "hands_distance": distance(positions["left_wrist"], positions["right_wrist"]),
            }

            self.peoples.append(data)

        return self.peoples

    def getJsonData(self, data):
        return json.dumps(data)

    def getPeoples(self):
        return self.peoples
