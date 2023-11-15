import cv2
import pytest
from src.yolo import Yolo


@pytest.fixture
def yolo():
    return Yolo("./models/yolov8n-pose.pt")


def test_run_detection(yolo):
    frame = cv2.imread("./images/test.jpeg")
    results, f = yolo.runDetection(frame)
    assert len(results) > 0
    assert f is not None


def test_parse_results(yolo):
    results = yolo.model(cv2.imread("./images/test.jpeg"))
    peoples = yolo.parseResults(results)
    assert isinstance(peoples, list)
    assert len(peoples) > 0
    assert isinstance(peoples[0], dict)


def test_get_json_data(yolo):
    data = {"test": "data"}
    json_data = yolo.getJsonData(data)
    assert isinstance(json_data, str)
    assert json_data == '{"test": "data"}'


def test_get_peoples(yolo):
    results = yolo.model(cv2.imread("./images/test.jpeg"))
    yolo.parseResults(results)
    peoples = yolo.getPeoples()
    assert isinstance(peoples, list)
    assert len(peoples) > 0

# to run tests
# python -m pytest -v
