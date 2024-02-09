using System.Collections;
using System.Collections.Generic;
using SimpleJSON;
using UnityEngine;

public class AvatarController : MonoBehaviour
{
    private GameObject socket;
    public GameObject leftWrist;
    public GameObject leftElbow;
    public GameObject leftShoulder;
    public GameObject leftEar;
    public GameObject leftHip;
    public GameObject rightWrist;
    public GameObject rightElbow;
    public GameObject rightShoulder;
    public GameObject rightEar;
    public GameObject rightHip;
    public GameObject leftKnee;
    public GameObject rightKnee;
    public GameObject leftAnkle;
    public GameObject rightAnkle;

    public GameObject Nose;

    private GameObject SpaceDimensions;
    private SpaceDimensionController spaceDimensionController;
    public int assignedPerson = -1;
    public float[] StartXY = new float[2];
    public float EndX;
    public float EndY;

    public float RangeX;
    public float RangeY;
    public float ReductCoeff = 0.5f;
    // Start is called before the first frame update
    void Start()
    {
        // find by tag is used to find the game object with the tag "SpaceDimensions"
        SpaceDimensions = GameObject.FindGameObjectWithTag("SpaceDimensions");
        spaceDimensionController = SpaceDimensions.GetComponent<SpaceDimensionController>();
        StartXY[0] = spaceDimensionController.StartXYValue[0];
        StartXY[1] = spaceDimensionController.StartXYValue[1];
        EndX = spaceDimensionController.EndXValue;
        EndY = spaceDimensionController.EndYValue;
        RangeX = spaceDimensionController.RangeX;
        RangeY = spaceDimensionController.RangeY;

        // Get Socket game object
        socket = GameObject.Find("Socket");
    }

    // Update is called once per frame
    void Update()
    {
        int peopleCount = socket.GetComponent<UdpSocket>().peopleCount;

        if (assignedPerson >= peopleCount || peopleCount == 0)
        {
            Destroy(gameObject);
        }

    }



    // LateUpdate is called once per frame after Update
    void LateUpdate()
    {
        JSONNode DetectedObjects = socket.GetComponent<UdpSocket>().DetectedObjects;
        JSONNode Obj = DetectedObjects[assignedPerson];

        // Get the position of the left and right wrist
        var leftWristPos = Obj["left_wrist"];
        var rightWristPos = Obj["right_wrist"];
        var leftElbowPos = Obj["left_elbow"];
        var rightElbowPos = Obj["right_elbow"];
        var leftShoulderPos = Obj["left_shoulder"];
        var rightShoulderPos = Obj["right_shoulder"];
        var leftEarPos = Obj["left_ear"];
        var rightEarPos = Obj["right_ear"];
        var leftHipPos = Obj["left_hip"];
        var rightHipPos = Obj["right_hip"];
        var nosePos = Obj["nose"];
        var leftKneePos = Obj["left_knee"];
        var rightKneePos = Obj["right_knee"];
        var leftAnklePos = Obj["left_ankle"];
        var rightAnklePos = Obj["right_ankle"];



        // Set the position of the points
        leftWrist.transform.position = new Vector3(EndX - leftWristPos[0] * RangeX, EndY - leftWristPos[1] * RangeY, transform.position.z);
        rightWrist.transform.position = new Vector3(EndX - rightWristPos[0] * RangeX, EndY - rightWristPos[1] * RangeY, transform.position.z);
        leftElbow.transform.position = new Vector3(EndX - leftElbowPos[0] * RangeX, EndY - leftElbowPos[1] * RangeY, transform.position.z);
        rightElbow.transform.position = new Vector3(EndX - rightElbowPos[0] * RangeX, EndY - rightElbowPos[1] * RangeY, transform.position.z);
        leftShoulder.transform.position = new Vector3(EndX - leftShoulderPos[0] * RangeX, EndY - leftShoulderPos[1] * RangeY, transform.position.z);
        rightShoulder.transform.position = new Vector3(EndX - rightShoulderPos[0] * RangeX, EndY - rightShoulderPos[1] * RangeY, transform.position.z);
        leftEar.transform.position = new Vector3(EndX - leftEarPos[0] * RangeX, EndY - leftEarPos[1] * RangeY, transform.position.z);
        rightEar.transform.position = new Vector3(EndX - rightEarPos[0] * RangeX, EndY - rightEarPos[1] * RangeY, transform.position.z);
        leftHip.transform.position = new Vector3(EndX - leftHipPos[0] * RangeX, EndY - leftHipPos[1] * RangeY, transform.position.z);
        rightHip.transform.position = new Vector3(EndX - rightHipPos[0] * RangeX, EndY - rightHipPos[1] * RangeY, transform.position.z);
        Nose.transform.position = new Vector3(EndX - nosePos[0] * RangeX, EndY - nosePos[1] * RangeY, transform.position.z);
        leftKnee.transform.position = new Vector3(EndX - leftKneePos[0] * RangeX, EndY - leftKneePos[1] * RangeY, transform.position.z);
        rightKnee.transform.position = new Vector3(EndX - rightKneePos[0] * RangeX, EndY - rightKneePos[1] * RangeY, transform.position.z);
        leftAnkle.transform.position = new Vector3(EndX - leftAnklePos[0] * RangeX, EndY - leftAnklePos[1] * RangeY, transform.position.z);
        rightAnkle.transform.position = new Vector3(EndX - rightAnklePos[0] * RangeX, EndY - rightAnklePos[1] * RangeY, transform.position.z);
    }
}
