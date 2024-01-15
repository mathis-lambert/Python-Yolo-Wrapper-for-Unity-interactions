using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using SimpleJSON;

public class ArrowThrow : MonoBehaviour
{

    private GameObject socket;
    public int assignedPerson;

    private int selfWidth;
    private int selfHeight;

    // Start is called before the first frame update
    void Start()
    {
        socket = GameObject.Find("Socket");
        selfWidth =
        selfHeight = GetComponent<SpriteRenderer>().sprite.texture.height;

    }

    // Update is called once per frame
    void Update()
    {
        JSONNode DetectedObjects = socket.GetComponent<UdpSocket>().DetectedObjects;

        int handsDistance = DetectedObjects[assignedPerson]["hands_distance"];
        Debug.Log(handsDistance);
        if (DetectedObjects[assignedPerson]["is_valid"])
        {
            if (handsDistance < 100)
            {
                // accelerate
                GetComponent<Rigidbody>().velocity = new Vector3(10, 0, 0) * 2000;
            }
            else if (handsDistance > 200)
            {
                GetComponent<Rigidbody>().velocity = Vector3.zero;
            }
        }

    }

    void LateUpdate()
    {
        if (transform.position.x > 1920)
        {
            transform.position = new Vector3(-960 + selfWidth / 2, transform.position.y, transform.position.z);
        }
    }
}
