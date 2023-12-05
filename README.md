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
This will run the script `src/pywui/main.py` with the --help option to show you the available options
```bash
cd python
source venv/bin/activate
pywui --help
```

##### Examples
Use your webcam
```bash
pywui --source 0
```

Show the webcam output
```bash
pywui --source 0 --show
```

Use video file
```bash
pywui --source path/to/video.mp4
```

**NOTE: `pywui`only runs the script main.py, if you want to run a script from the `scripts/` folder, you have to use `python` instead of `pywui`**
```bash 
python scripts/the_script_you_want.py
```

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


