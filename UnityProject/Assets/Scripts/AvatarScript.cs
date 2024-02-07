using System.Collections;
using System.Collections.Generic;
using SimpleJSON;
using Unity.VisualScripting;
using UnityEngine;

public class AvatarScript : MonoBehaviour
{

    private GameObject socket;
    public int assignedPerson;
    public Transform leftShoulder;
    public Transform rightShoulder;
    public Transform leftElbow;
    public Transform rightElbow;
    public int startX = -2;
    public int endX = 2;
    public float rangeX;

    // Start is called before the first frame update
    void Start()
    {
        socket = GameObject.Find("Socket");
        rangeX = endX - startX;
        Debug.Log(rangeX);
        AssignShoulders();
    }

    void AssignShoulders()
    {
        // Parcourir tous les os et trouver les épaules
        foreach (Transform bone in GetComponentsInChildren<Transform>())
        {
            if (bone.name == "mixamorig:LeftArm")
            {
                leftShoulder = bone;
            }
            else if (bone.name == "mixamorig:RightArm")
            {
                rightShoulder = bone;
            }
            else if (bone.name == "mixamorig:LeftForeArm")
            {
                leftElbow = bone;
            }
            else if (bone.name == "mixamorig:RightForeArm")
            {
                rightElbow = bone;
            }
        }
    }

    void Rotate(JSONNode Obj)
    {
        // Appliquer une rotation aux épaules
        if (leftShoulder != null)
        {
            if (Obj["left_arm_angle"] > 0)
            {
                // Obj["left_shoulder_angle"] sur l'axe Left et 90° sur l'axe Up
                leftShoulder.localRotation = Quaternion.Euler(0, 80, 90 - Obj["left_shoulder_angle"]);
            }
            else
            {
                // Obj["left_shoulder_angle"] sur l'axe Left et 90° sur l'axe Up
                leftShoulder.localRotation = Quaternion.Euler(0, -80, Obj["left_shoulder_angle"] - 90);
            }
        }
        if (rightShoulder != null)
        {
            if (Obj["right_arm_angle"] > 0)
            {
                rightShoulder.localRotation = Quaternion.Euler(0, -80, Obj["right_shoulder_angle"] - 90);
            }
            else
            {
                rightShoulder.localRotation = Quaternion.Euler(0, 80, 90 - Obj["right_shoulder_angle"]);
            }
        }
        if (leftElbow != null)
        {
            RotateElbow(leftElbow, Obj["left_arm_angle"], Vector3.back);
        }
        if (rightElbow != null)
        {
            RotateElbow(rightElbow, Obj["right_arm_angle"], Vector3.forward);
        }
    }


    private void RotateElbow(Transform bodyPart, float rotationAngle, Vector3 rotationAxis)
    {
        rotationAngle = Mathf.Abs(rotationAngle);

        Quaternion rotation = Quaternion.AngleAxis(180 - rotationAngle, rotationAxis);
        bodyPart.transform.localRotation = rotation;
    }

    // Update is called once per frame
    void Update()
    {
        // Exemple de manipulation des épaules
        JSONNode DetectedObjects = socket.GetComponent<UdpSocket>().DetectedObjects;
        int peopleCount = socket.GetComponent<UdpSocket>().peopleCount;

        if (assignedPerson < peopleCount)
        {
            float offsetLeft = DetectedObjects[assignedPerson]["left_offset"];
            float xPos = startX + (float)(offsetLeft * rangeX);
            Debug.Log(xPos);
            transform.position = new Vector3(xPos, 0, 0);
            Rotate(DetectedObjects[assignedPerson]);
        }
        else
        {
            Destroy(gameObject);
        }

    }

    void LateUpdate()
    {
        if (transform.position.y < -10)
        {
            transform.position = new Vector3(transform.position.x, 2, transform.position.z);
        }
    }
}
