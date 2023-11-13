using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BallScript : MonoBehaviour
{

    public GameObject udpController;
    // self game object
    public GameObject ball;

    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        int handsDistance = udpController.GetComponent<UdpSocket>().handsDistance;
        if (handsDistance > 0)
        {
            // Set the scale of the ball based on the distance between the hands
            ball.transform.localScale = new Vector3(1, 1, 1) * handsDistance / 100;
        }
    }
}
