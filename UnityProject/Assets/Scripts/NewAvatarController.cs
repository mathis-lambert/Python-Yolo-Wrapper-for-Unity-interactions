using System.Collections;
using System.Collections.Generic;
using System.Threading.Tasks;
using SimpleJSON;
using UnityEngine;

public class NewAvatarController : MonoBehaviour
{
    private GameObject socket;
    public GameObject leftWrist;
    // public GameObject leftElbowHint;
    public GameObject rightWrist;
    public GameObject leftAnkle;
    public GameObject rightAnkle;
    public GameObject leftKnee;
    public GameObject rightKnee;
    public GameObject leftShoulder;
    public GameObject rightShoulder;

    // public GameObject rightElbowHint;
    public bool isArmsUp = false;
    public bool isArmsDown = false;


    private GameObject SpaceDimensions;
    private SpaceDimensionController spaceDimensionController;
    public int assignedPerson = -1;
    private float[] StartXY;
    private float EndX;
    private float EndY;

    private float RangeX;
    private float RangeY;
    // Start is called before the first frame update
    void Start()
    {
        // find by tag is used to find the game object with the tag "SpaceDimensions"
        SpaceDimensions = GameObject.FindGameObjectWithTag("SpaceDimensions");
        spaceDimensionController = SpaceDimensions.GetComponent<SpaceDimensionController>();
        StartXY = new float[2];
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
        JSONNode DetectedObjects = socket.GetComponent<UdpSocket>().DetectedObjects;
        int peopleCount = socket.GetComponent<UdpSocket>().peopleCount;

        if (assignedPerson >= peopleCount || peopleCount == 0 || !DetectedObjects[assignedPerson]["is_valid"])
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
        var leftAnklePos = Obj["left_ankle"];
        var rightAnklePos = Obj["right_ankle"];
        var leftKneePos = Obj["left_knee"];
        var rightKneePos = Obj["right_knee"];
        var offset = Obj["inter_leg_position"];

        // Set the position of the points
        leftWrist.transform.position = new Vector3(EndX - leftWristPos[0] * RangeX, EndY - leftWristPos[1] * RangeY, leftWrist.transform.position.z);
        rightWrist.transform.position = new Vector3(EndX - rightWristPos[0] * RangeX, EndY - rightWristPos[1] * RangeY, rightWrist.transform.position.z);
        // leftElbowHint.transform.position = new Vector3(EndX - leftElbowPos[0] * RangeX, EndY - leftElbowPos[1] * RangeY, leftElbowHint.transform.position.z);
        // rightElbowHint.transform.position = new Vector3(EndX - rightElbowPos[0] * RangeX, EndY - rightElbowPos[1] * RangeY, rightElbowHint.transform.position.z);
        leftAnkle.transform.position = new Vector3(EndX - leftAnklePos[0] * RangeX, EndY - leftAnklePos[1] * RangeY, leftAnkle.transform.position.z);
        rightAnkle.transform.position = new Vector3(EndX - rightAnklePos[0] * RangeX, EndY - rightAnklePos[1] * RangeY, rightAnkle.transform.position.z);
        leftKnee.transform.position = new Vector3(EndX - leftKneePos[0] * RangeX, EndY - leftKneePos[1] * RangeY, leftKnee.transform.position.z);
        rightKnee.transform.position = new Vector3(EndX - rightKneePos[0] * RangeX, EndY - rightKneePos[1] * RangeY, rightKnee.transform.position.z);
        transform.position = new Vector3(EndX - offset[0] * RangeX, EndY - offset[1] * RangeY, transform.position.z);

        if (leftWrist.transform.position.y > leftShoulder.transform.position.y && rightWrist.transform.position.y > rightShoulder.transform.position.y)
        {
            Debug.Log("Arms Up");
            isArmsUp = true;
            isArmsDown = false;
        }
        else
        {
            Debug.Log("Arms Down");
            isArmsUp = false;
            isArmsDown = true;
        }
    }
}
