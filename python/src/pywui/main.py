############################
# @Author: Mathis LAMBERT
# @Date: Janvier 2024
############################

from pywui.udpsocket import updsocket as s
import cv2
from pywui.yolo import Yolo
import argparse
import platform

# Parse arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument("--show", action="store_true", help="show video")
parser.add_argument(
    "--source",
    type=str,
    default="0",
    help="Your capture source, 0 for camera or /path/to/file for a video",
)
parser.add_argument(
    "--model",
    type=str,
    default="./models/yolov8n-pose.pt",
    help="model path, default is yolov8n-pose.pt",
)
parser.add_argument(
    "--detect-method",
    type=str,
    default="predict",
    choices=["predict", "track"],
    help="detection method, predict or track",
)
parser.add_argument(
    "--tracker",
    type=str,
    default="./trackers/botsort.yaml",
    help="tracker path if detect method is track",
)
parser.add_argument(
    "--confidence", type=float, default=0.5, help="confidence threshold, default is 0.5"
)
parser.add_argument("--gpu", action="store_true", help="use gpu for detection")
parser.add_argument(
    "--plot",
    action="store_true",
    help="Display plot to compare filtered and raw values",
)
parser.add_argument(
    "--plot-show",
    action="store_true",
    help="Display plot to compare filtered and raw values",
)
parser.add_argument(
    "--plot-save",
    action="store_true",
    help="Display plot to compare filtered and raw values",
)
parser.add_argument(
    "--debug", action="store_true", help="debug mode with print statements"
)
parser.add_argument("--log", action="store_true", help="log data to txt file")
parser.add_argument(
    "--log-path", type=str, default="./logs/", help="path to save log files"
)
parser.add_argument("--filter", action="store_true", help="filter data")
parser.add_argument("--filter-order", type=int, default=3, help="filter order")
args = parser.parse_args()

SHOW_VIDEO = args.show


class main:
    def __init__(self) -> None:
        """
        Constructor of the main class that handles the UDP socket and the video capture
        call start() to start detection, sending and receiving data
        """
        # Create UDP socket to use for sending (and receiving)
        self.sock = s(
            udpIP="127.0.0.1",
            portTX=8000,
            portRX=8001,
            enableRX=True,
            suppressWarnings=not args.debug,
        )

        # Create video capture object
        try:
            args.source = int(args.source)
        except:
            if args.debug:
                print("Source is not an int, setting source to path")
            pass
        # Détecte le système d'exploitation
        if platform.system() == 'Windows':
            # Sur Windows, utilise le backend MSMF
            self.cap = cv2.VideoCapture(args.source, cv2.CAP_MSMF)
        else:
            # Sur les autres systèmes d'exploitation, utilise le backend par défaut
            self.cap = cv2.VideoCapture(args.source)

        self.yolo = Yolo(
            path=args.model,
            conf=args.confidence,
            gpu=args.gpu,
            plot=args.plot,
            plot_show=args.plot_show,
            plot_save=args.plot_save,
            debug=args.debug,
            log=args.log,
            log_path=args.log_path,
            filter=args.filter,
            filter_order=args.filter_order,
        )

    def start(self):
        """
        Start sending and receiving data with yolo detections and poses
        """
        print("pywui is running ;) - Mathis LAMBERT 2024")
        print("Press ctrl+c to stop the program")

        while True:
            # Read frame from video capture object
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

            # Run detection and parse results
            r, f = self.yolo.run_detection(
                frame, mode=args.detect_method, tracker=args.tracker
            )
            # Get data from results
            d = self.yolo.parse_results(r)

            self.sock.SendData(self.yolo.get_json_data(d))  # send data

            if SHOW_VIDEO:
                cv2.imshow("frame", f)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            data = self.sock.ReadReceivedData()  # read data

            if args.debug:
                if data is not None:  # if NEW data has been received since last ReadReceivedData function call
                    print(data)  # print new received data


if __name__ == "__main__":
    main().start()
