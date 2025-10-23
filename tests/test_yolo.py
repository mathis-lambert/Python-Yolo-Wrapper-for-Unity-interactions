import cv2
import pytest
from pywui.yolo import Yolo
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
TEST_IMAGE = ROOT_DIR / "docs" / "assets" / "images" / "test.jpeg"
MODEL_WEIGHTS = ROOT_DIR / "models" / "yolov8n-pose.pt"

pytestmark = pytest.mark.skipif(
    not MODEL_WEIGHTS.exists(),
    reason="YOLO model weights are not available in ./models/yolov8n-pose.pt",
)


@pytest.fixture
def yolo():
    return Yolo(str(MODEL_WEIGHTS))


def test_run_detection(yolo):
    frame = cv2.imread(str(TEST_IMAGE))
    results, f = yolo.run_detection(frame)
    assert len(results) > 0
    assert f is not None


def test_parse_results(yolo):
    results = yolo.model(cv2.imread(str(TEST_IMAGE)))
    peoples = yolo.parse_results(results)
    assert isinstance(peoples, list)
    assert len(peoples) > 0
    assert isinstance(peoples[0], dict)


def test_get_json_data(yolo):
    data = {"test": "data"}
    json_data = yolo.get_json_data(data)
    assert isinstance(json_data, str)
    assert json_data == '{"test": "data"}'


def test_get_peoples(yolo):
    results = yolo.model(cv2.imread(str(TEST_IMAGE)))
    yolo.parse_results(results)
    peoples = yolo.get_peoples()
    assert isinstance(peoples, list)
    assert len(peoples) > 0


def test_filter_signal(yolo):
    signal = [
        {
            "a": 0,
            "b": 1,
        },
        {
            "a": 2,
            "b": 3,
        },
        {
            "a": 4,
            "b": 5,
        },
        {
            "a": 6,
            "b": 7,
        },
        {
            "a": 8,
            "b": 9,
        }
    ]
    yolo.last_values["id_1"] = signal
    filtered_signal = yolo.filter_signal("id_1")
    assert isinstance(filtered_signal, dict)
    assert len(filtered_signal) == 2
    assert filtered_signal["a"] == 4
    assert filtered_signal["b"] == 5


# to run tests
# python -m pytest -v
