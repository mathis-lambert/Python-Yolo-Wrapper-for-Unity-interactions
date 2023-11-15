# Python-Yolo-Wrapper-for-Unity-interactions

## Introduction
This source code has been developped to allow python and these libraries communicate with Unity Engine. This use case is using Ultralytics's YoloV8 and is able to send position information to unity in order to create interactions and animations with it.

## Installation
Clone this public repo with wherever you want
```bash
git clone https://github.com/mathis-lambert/python-yolo-wrapper-for-unity-interactions yolo_with_unity
cd yolo_with_unity
```
*It's not a docker project for now, but it should be later...*

init the project with these commands :
```bash
cd python
python3 -m venv venv # create the virtual env (only the first time, it will handle the dependencies)
source venv/bin/activate # activate the virtual env
pip install -r requirements.txt # install the dependencies
```

## Usage
### Unity
Open the project with `Unity **2022.3.13f1**` or later. You can find the project in the folder `UnityProject/`.

### Python
#### Execute the project
Open a terminal and init the project with these commands :
```bash
cd python
source venv/bin/activate
python -m src.main --source 0 # To use your webcam
python -m src.main --source path/to/video # To use a video
python -m src.main --source 0 --show # To show the video
python -m src.main --help # To see all the options
```
#### Execute the tests
Open a terminal and init the project with these commands :
```bash
cd python
source venv/bin/activate
python -m pytest -v
```

## Collaborate
If you want to collaborate on this open source repo, you're free to do so.
- Fork the repo
- Create your own branch
- Develop your feature
- And with a PR describe the purpose of your feature


