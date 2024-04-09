# Python-Yolo-Wrapper-for-Unity-interactions

## Introduction
This source code has been developped to allow python and these libraries communicate with Unity Engine. This use case is using Ultralytics's YoloV8 and is able to send position information to unity in order to create interactions and animations with it.

## Prerequisites
- Unity `2022.3.13f1` or later
- Python `3.8` or later
- Make sure you have a webcam or a video file to test the project
- This installation guide has been tested on Linux and MacOS, but it should work on Windows too with some modifications

## Installation
⚠️ if you have a windows PC with RTX GPU and Intel CPU check the follow installation guide ⚠️

- [Lien de la documentation](https://polite-comma-f85.notion.site/Installation-Windows-a91307b8e6554cc59f0c552f998a92ef?pvs=4)

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
source venv/bin/activate # On windows : venv\Scripts\activate
make install # make is not available on windows, run install.bat instead (not tested)
```

## Usage
### Unity
Open the project with **Unity `2022.3.13f1`** or later. You can find the project in the folder `UnityProject/`.
- Click on the ADD button in the Unity Hub and select the folder `UnityProject/`
- Select the project and click on the OPEN button

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
source venv/bin/activate # On windows : venv\Scripts\activate
pywui-test
```

## Unity use case
The use case is simple, the python script will send the position of the detected object to Unity. Then Unity will move the object to the position sent by python.

### Python
Run the command :
```bash
pywui --model ./models/yolov8s-pose.pt --detect-method track --source 0 --conf 0.7 --filter
```

### Unity
#### Main Scene
- Open the scene `Assets/Scenes/Main.unity`
- Click on the play button
- You should see as many articulation groups as people detected by the python script and the articulations should move to the position of the people detected
- <img width="675" alt="image" src="https://github.com/mathis-lambert/Python-Yolo-Wrapper-for-Unity-interactions/assets/93223257/961683fb-3a5c-4ae8-b1d1-efb04767c28b">


#### Articulation Scene
- Open the scene `Assets/Scenes/Articulation.unity`
- Click on the play button
- You should see as many articulation groups as people detected by the python script and the articulations should move to the position of the people detected
- <img width="669" alt="image" src="https://github.com/mathis-lambert/Python-Yolo-Wrapper-for-Unity-interactions/assets/93223257/4295744c-4853-4afc-8dc1-295cd1d97f3a">



## Current issues
- `python3` might not work, use `python` instead
- If you have an error with `pywui` command, try to run `source venv/bin/activate` again and then `pywui` should work
- If you have an error with `pywui-test` command, try to run `source venv/bin/activate` again and then `pywui-test` should work

## Collaborate
If you want to collaborate on this open source repo, you're free to do so.
- Fork the repo
- Create your own branch
- Develop your feature
- And with a PR describe the purpose of your feature


