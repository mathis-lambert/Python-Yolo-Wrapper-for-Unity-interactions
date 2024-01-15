using System.Collections;
using System.Collections.Generic;
using SimpleJSON;
using UnityEngine;

public class BallScript : MonoBehaviour
{

    private GameObject socket;
    public int assignedPerson;

    // Start is called before the first frame update
    void Start()
    {
        socket = GameObject.Find("Socket");
    }

    // Update is called once per frame
    void Update()
    {
        JSONNode DetectedObjects = socket.GetComponent<UdpSocket>().DetectedObjects;
        int peopleCount = socket.GetComponent<UdpSocket>().peopleCount;

        if (assignedPerson < peopleCount)
        {
            int handsDistance = DetectedObjects[assignedPerson]["hands_distance"];

            if (handsDistance > 0)
            {
                transform.localScale = new Vector3(1, 1, 1) * handsDistance / 100;
            }
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
