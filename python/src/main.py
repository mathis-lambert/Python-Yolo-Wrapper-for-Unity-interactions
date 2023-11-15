from src.udpsocket import updsocket as s
import cv2
from src.yolo import Yolo
import argparse

# Parse arguments from command line
parser = argparse.ArgumentParser()
parser.add_argument("--show", action="store_true", help="show video")
parser.add_argument("--source", type=str, default="0",
                    help="Your capture source, 0 for camera or /path/to/file for a video")
parser.add_argument("--model", type=str, default="./models/yolov8n-pose.pt",
                    help="model path, default is yolov8n-pose.pt")
parser.add_argument("--detect-method", type=str, default="predict", choices=[
                    "predict", "track"], help="detection method, predict or track")
parser.add_argument("--tracker", type=str, default="./trackers/botsort.yaml",
                    help="tracker path if detect method is track")
parser.add_argument("--confidence", type=float, default=0.5,
                    help="confidence threshold, default is 0.5")
parser.add_argument("--gpu", action="store_true",
                    help="use gpu for detection")
args = parser.parse_args()

SHOW_VIDEO = args.show


class main():
    def __init__(self) -> None:
        """
        Constructor of the main class that handles the UDP socket and the video capture
        call start() to start detection, sending and receiving data
        """
        # Create UDP socket to use for sending (and receiving)
        self.sock = s(udpIP="127.0.0.1", portTX=8000, portRX=8001,
                      enableRX=True, suppressWarnings=True)

        # Create video capture object
        try:
            args.source = int(args.source)
        except:
            pass
        self.cap = cv2.VideoCapture(args.source)

        self.yolo = Yolo(args.model, conf=args.confidence, gpu=args.gpu)

    def start(self):
        """
        Start sending and receiving data with yolo detections and poses
        """
        while True:
            # Read frame from video capture object
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

            # Run detection and parse results
            r, f = self.yolo.runDetection(
                frame, mode=args.detect_method, tracker=args.tracker)
            # Get data from results
            d = self.yolo.parseResults(r)

            self.sock.SendData(self.yolo.getJsonData(d))  # send data
            print("Data sent")

            if SHOW_VIDEO:
                cv2.imshow("frame", f)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            data = self.sock.ReadReceivedData()  # read data

            if data != None:  # if NEW data has been received since last ReadReceivedData function call
                print(data)  # print new received data


if __name__ == "__main__":
    main().start()
