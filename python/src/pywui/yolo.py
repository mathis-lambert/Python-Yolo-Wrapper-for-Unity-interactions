import os
import re
from torch import device
from ultralytics import YOLO
import json
from pywui.utils import *
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt
from collections import defaultdict
import time  # For time measurement


class Yolo:
    def __init__(self, path, conf=0.5, gpu=False, plot=False, plot_show=False, plot_save=False, debug=False, log=False, log_path="./logs/", filter=False, filter_order=3):
        self.model = YOLO(path)
        self.cap = None
        self.peoples = list()
        self.confidence = conf  # Confidence threshold
        self.device = device("cuda:0" if gpu else "cpu")
        self.last_values = dict()
        self.last_filtered_values = dict()

        self.plot = plot
        self.plot_show = plot_show
        self.plot_save = plot_save
        self.fig = None  # Initialize a figure attribute
        self.axes = None  # Initialize axes

        self.debug = debug  # Debug mode
        self.log = log  # Log data to txt file

        self.filter = filter
        self.filter_order = filter_order

    def run_detection(self, frame, mode: str = "predict", tracker: str = "./trackers/botsort.yaml") -> tuple:
        """
        Run detection on a frame and return results and a plot
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

            if positions["left_wrist"] != [0, 0] or positions["right_wrist"] != [0, 0] and positions["nose"] != [0, 0]:
                valid = True
            else:
                valid = False

            # Data is a dictionary of positions, if you want to add more data, add it here, it will be added to the list
            # and then filtered
            data = {
                "left_wrist": positions["left_wrist"],
                "right_wrist": positions["right_wrist"],
                "hands_distance": distance(positions["left_wrist"], positions["right_wrist"]),
                "left_elbow_angle": angle(positions["left_wrist"], positions["left_elbow"], positions["left_shoulder"]),
                "right_elbow_angle": angle(positions["right_wrist"], positions["right_elbow"], positions["right_shoulder"]),
                "left_arm_angle": round(angle(positions["left_shoulder"], positions["left_elbow"], positions["left_wrist"]), 2),
                "right_arm_angle": round(angle(positions["right_shoulder"], positions["right_elbow"], positions["right_wrist"]), 2),
                "left_shoulder_angle": round(angle(positions["left_hip"], positions["left_shoulder"], positions["left_elbow"]), 2),
                "right_shoulder_angle": round(angle(positions["right_hip"], positions["right_shoulder"], positions["right_elbow"]), 2),
                "is_valid": valid,
                "id": id
            }

            # Fill last_values
            self.last_values[id].append(data)

            if self.filter:
                ORDER = self.filter_order
                # Filter
                _fd = self.filter_signal(id, ORDER, verbose=True)
                # Fill last_filtered_values if available
                self.last_filtered_values[id].append(_fd) if _fd else None
                # Append filtered data if available, else raw data to peoples list
                self.peoples.append(_fd if _fd else data)
            else:
                self.peoples.append(data)

        if (self.plot):
            self.plot_filtered_data(save=True)

        return self.peoples

    @staticmethod
    def get_json_data(data):
        return json.dumps(data)

    def filter_signal(self, id, order=5, verbose=False):
        """
        Filter signal with a average filter
        """
        if verbose:
            start_time = time.perf_counter()

        print(f"Filtering data with order: {order} and id: {id}")
        if id is None:
            print("No id")
            return None

        samples = self.last_values[id][-order:]
        if len(samples) != order:
            print("Insufficient data")
            return None

        data = defaultdict(lambda: defaultdict(list))
        single_values = defaultdict(list)
        filtered_data = defaultdict(list)

        for sample in samples:
            for key, value in sample.items():
                if key not in ["id", "is_valid"]:
                    if isinstance(value, list) and len(value) == 2:
                        data[key]['x'].append(value[0])
                        data[key]['y'].append(value[1])
                    else:
                        single_values[key].append(value)

        for key, values in data.items():
            filtered_data[key] = [sum(v) / len(v)
                                  for v in values.values() if v]

        for key, values in single_values.items():
            filtered_data[key] = sum(values) / len(values) if values else None

        if verbose:
            end_time = time.perf_counter()
            duration = end_time - start_time
            print(f"Filtering completed in {duration:.6f} seconds")

        return dict(filtered_data)

    def get_peoples(self):
        return self.peoples

    def plot_filtered_data(self, real_time=False, save=False):
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

            if real_time:
                plt.ion()
            elif save:
                plt.ioff()

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

        if real_time and save:
            print("Choose either real_time or save")
            raise Exception("Choose either real_time or save")
        elif real_time:
            self.fig.tight_layout()
            plt.draw()
            plt.pause(0.00001)
        elif save:
            # check if plots directory exists
            if not os.path.exists("./plots/"):
                os.makedirs("./plots/")

            self.fig.tight_layout()
            plt.savefig(f"./plots/signal_filtering.png")
        else:
            print("Choose either real_time or save")
            raise Exception("Choose either real_time or save")
