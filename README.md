# Python-Yolo-Wrapper-for-Unity-interactions

## Introduction
This source code has been developped to allow python and these libraries communicate with Unity Engine. This use case is using Ultralytics's YoloV8 and is able to send position information to unity in order to create interactions and animations with it.

## Installation
Clone this public repo with 
```bash
git clone https://github.com/mathis-lambert/python-yolo-wrapper-for-unity-interactions
```
*It's not a docker project for now, but it should be later...*

Open a terminal and init the project with these commands :
```bash
cd python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
### Unity
Open the project with Unity 2022.3.13f1 or later. You can find the project in the folder `UnityProject/`.

### Python
Open a terminal and init the project with these commands :
```bash
cd python
source venv/bin/activate
python ./src/main.py --source 0 # To use your webcam
python ./src/main.py --source path/to/video # To use a video
python ./src/main.py --source 0 --show # To show the video
python ./src/main.py --help # To see all the options
```

## Collaborate
If you want to collaborate on this open source repo, you're free to do so.
- Fork the repo
- Create your own branch
- Develop your feature
- And with a PR describe the purpose of your feature


