using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class WristScript : MonoBehaviour
{

    public GameObject leftWrist;
    public GameObject rightWrist;

    public GameObject socket;
    public object positions;
    // Start is called before the first frame update
    private float localScale;
    private float height;
    private float width;


    void Start()
    {
        localScale = transform.localScale.x;
        height = GetComponent<CanvasScaler>().referenceResolution.y;
        width = GetComponent<CanvasScaler>().referenceResolution.x;

    }

    // Update is called once per frame
    void Update()
    {
        // Get the position of the left and right wrist
        var leftWristPos = socket.GetComponent<UdpSocket>().leftWristPosition;
        var rightWristPos = socket.GetComponent<UdpSocket>().rightWristPosition;

        // Set the position of the left and right wrist
        leftWrist.transform.position = new Vector3(width - leftWristPos.x, leftWristPos.y + height, leftWristPos.z) * localScale;
        rightWrist.transform.position = new Vector3(width - rightWristPos.x, rightWristPos.y + height, rightWristPos.z) * localScale;
    }
}
