from torch import device
from ultralytics import YOLO
import json
from pywui.utils import *
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt


class Yolo:
    def __init__(self, path, conf=0.5, gpu=False, plot=False):
        self.model = YOLO(path)
        self.cap = None
        self.peoples = list()
        self.confidence = conf  # Confidence threshold
        self.device = device("cuda:0" if gpu else "cpu")
        self.last_values = dict()
        self.last_filtered_values = dict()

        self.plot = plot
        self.fig = None  # Initialize a figure attribute
        self.axes = None  # Initialize axes

    def run_detection(self, frame, mode: str = "predict", tracker: str = "./trackers/botsort.yaml"):
        """
        Run detection on a frame
        """
        # Prédire les poses
        if mode == "predict":
            results = self.model(
                frame, conf=self.confidence, device=self.device)
        elif mode == "track":
            results = self.model.track(
                frame, tracker=tracker, persist=True, conf=self.confidence, device=self.device)
        else:
            raise Exception("Mode must be 'predict' or 'track'")

        f = results[0].plot()

        return results, f

    def parse_results(self, results):
        """
        Parse predictions into a list of dictionaries
        """
        # print(results[0].boxes)
        boxes = results[0].boxes.xyxy.tolist()
        ids = results[0].boxes.id.tolist(
        ) if results[0].boxes.id is not None else []
        keypoints = results[0].keypoints.xy.tolist()
        keypoints_normalized = results[0].keypoints.xyn.tolist()

        self.peoples = list()

        for person in keypoints:
            if len(person) == 0:
                continue

            index = keypoints.index(person)
            id = "id_" + str(int(ids[index] if len(ids) > 0 else index))

            if self.last_values.get(id) is None:
                self.last_values[id] = list()
                self.last_filtered_values[id] = list()

            positions = {
                "nose": person[0],
                "left_eye": person[1],
                "right_eye": person[2],
                "left_ear": person[3],
                "right_ear": person[4],
                "left_shoulder": person[5],
                "right_shoulder": person[6],
                "left_elbow": person[7],
                "right_elbow": person[8],
                "left_wrist": person[9],
                "right_wrist": person[10],
                "left_hip": person[11],
                "right_hip": person[12],
                "left_knee": person[13],
                "right_knee": person[14],
                "left_ankle": person[15],
                "right_ankle": person[16]
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

            if positions["left_wrist"] != [0, 0] or positions["right_wrist"] != [0, 0] and positions["nose"] != [0, 0]:
                valid = True
            else:
                valid = False

            data = {
                "left_wrist": positions["left_wrist"],
                "right_wrist": positions["right_wrist"],
                "hands_distance": distance(positions["left_wrist"], positions["right_wrist"]),
                "left_elbow_angle": angle(positions["left_wrist"], positions["left_elbow"], positions["left_shoulder"]),
                "right_elbow_angle": angle(positions["right_wrist"], positions["right_elbow"], positions["right_shoulder"]),
                "is_valid": valid,
                "id": id
            }

            # Fill last_fives
            ORDER = 5
            self.last_values[id].append(data)

            # Filter
            _fd = self.filter_signal(id, ORDER)

            if _fd is not None:
                print("raw",  self.last_values[id][-5])

                print("filtered", _fd["left_elbow_angle"])
                self.last_filtered_values[id].append(_fd)

            self.peoples.append(data)

        # TODO: REPRENDRE LA FONCTION PLOT_FILTERED_DATA
        if (self.plot):
            self.plot_filtered_data()

        return self.peoples

    @staticmethod
    def get_json_data(data):
        return json.dumps(data)

    def filter_signal(self, id, order=5):
        """
        Apply average filter on last values
        """
        print("Filtering data with order : ", order, " and id : ", id)
        if id is None:
            print("No id")
            return None

        samples = [s for s in self.last_values[id]]
        samples = samples[-order:]

        if len(samples) < order:
            print("Not enough data")
            return None
        elif len(samples) > order:
            raise Exception("Too much data in last_fives")

        filtered_data = dict()
        data = dict()

        for sample in samples:
            for key, value in sample.items():
                if key not in ["id", "is_valid"]:
                    try:
                        if data.get(key) is None:
                            if isinstance(value, list):
                                data[key] = dict()
                                filtered_data[key] = dict()
                                if len(value) == 2:
                                    data[key]["x"] = list()
                                    data[key]["y"] = list()
                                    data[key]["x"].append(value[0])
                                    data[key]["y"].append(value[1])
                            else:
                                data[key] = list()
                                filtered_data[key] = list()
                                data[key].append(value)
                        else:
                            if isinstance(value, list):
                                if len(value) == 2:
                                    data[key]["x"].append(value[0])
                                    data[key]["y"].append(value[1])

                                else:
                                    data[key].append(value)

                    except Exception as e:
                        print(e)
                        continue

        for key, value in data.items():
            if isinstance(value, dict):
                r = list()
                for k, v in value.items():
                    if len(v) == 0:
                        continue

                    r.append(sum(v) / len(v))

                filtered_data[key] = r
            else:
                if len(value) == 0:
                    continue
                filtered_data[key] = sum(value) / len(value)

        return filtered_data

    def get_peoples(self):
        return self.peoples

    def plot_filtered_data(self):
        """
        Plot comparison graphs for each key in self.last_filtered_values/last_values
        to compare filtered values with raw values
        """
        # Collecting unique keys for dynamic subplot creation
        unique_keys = set()
        for values in self.last_values.values():
            for data in values:
                unique_keys.update(data.keys())
        for values in self.last_filtered_values.values():
            for data in values:
                # Assuming the first item in each list is the data dictionary
                unique_keys.update(data.keys())

        unique_keys -= {'id', 'is_valid'}  # Remove non-plotable keys

        # Check if there are any keys to plot
        if not unique_keys:
            print("No data to plot.")
            return

        # Initialize or update the figure and axes with a smaller figsize
        num_plots = len(unique_keys)
        fig_width = 10  # Adjust the width as needed
        fig_height = 2 * num_plots  # Adjust the height per subplot as needed
        if self.fig is None or self.axes is None or len(self.axes) != num_plots:
            plt.ion()
            self.fig, self.axes = plt.subplots(
                num_plots, 1, figsize=(fig_width, fig_height))
            if num_plots == 1:
                self.axes = [self.axes]  # Ensure axes is always a list

        for ax in self.axes:
            ax.clear()  # Clear each subplot

        for i, key in enumerate(unique_keys):
            # Extracting raw and filtered values for each key
            raw_values = []
            for id, values in self.last_values.items():
                for data in values:
                    if key in data:
                        if isinstance(data[key], dict) and ('x' in data[key] and 'y' in data[key]):
                            # Extracting 'x' value
                            raw_values.append(data[key]['x'])
                            raw_values.append(data[key]['y'])
                        else:
                            raw_values.append(data[key])

            filtered_values = []
            for id, values in self.last_filtered_values.items():
                for data in values:
                    if key in data:
                        if isinstance(data[key], dict) and ('x' in data[key] or 'y' in data[key]):
                            filtered_values.append(data[key]['x'])
                            filtered_values.append(data[key]['y'])

                        else:
                            filtered_values.append(data[key])

            # Plotting
            self.axes[i].plot(raw_values, label='Raw Data', color='blue')
            self.axes[i].plot(
                filtered_values, label='Filtered Data', color='orange')

            self.axes[i].set_title(f'{key.capitalize()} Over Time')
            self.axes[i].set_xlabel('Sample')
            self.axes[i].set_ylabel(key)
            self.axes[i].legend()

        self.fig.tight_layout()
        plt.draw()
        plt.pause(0.001)
