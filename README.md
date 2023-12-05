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
this will create a virtual env and install the dependencies
```bash
cd python
python3 -m venv venv
source venv/bin/activate
make install
```

## Usage
### Unity
Open the project with **Unity `2022.3.13f1`** or later. You can find the project in the folder `UnityProject/`.

### Python
#### Execute scripts
Open a terminal and run these commands :
This will run the script `scripts/main.py` with the --help option to show you the available options
```bash
cd python
source venv/bin/activate
python scripts/main.py --help
```

##### Examples
Use your webcam
```bash
python scripts/main.py --source 0
```

Show the webcam output
```bash
python scripts/main.py --source 0 --show
```

Use video file
```bash
python scripts/main.py --source path/to/video.mp4
```

**You can find more examples in the `scripts/` folder**

#### Execute the tests
Open a terminal and run these commands :
```bash
cd python
source venv/bin/activate
pywui-test
```

## Collaborate
If you want to collaborate on this open source repo, you're free to do so.
- Fork the repo
- Create your own branch
- Develop your feature
- And with a PR describe the purpose of your feature


