using System.Collections;
using System.Collections.Generic;
using SimpleJSON;
using UnityEngine;

public class BallSpawn : MonoBehaviour
{
    private GameObject socket;
    // ball prefab
    public GameObject ballPrefab;
    public float SpawnRadius = 10f;
    private int peopleCount;
    private int lastPeopleCount = 0;

    // Start is called before the first frame update
    void Start()
    {
        socket = GameObject.Find("Socket");
        peopleCount = socket.GetComponent<UdpSocket>().peopleCount;

        for (int i = 0; i < peopleCount; i++)
        {
            if (socket.GetComponent<UdpSocket>().DetectedObjects[i]["is_valid"])
            {
                SpawnBall(i);
            }
        }
    }

    int countValidPeople()
    {
        int count = 0;
        int objCount = socket.GetComponent<UdpSocket>().peopleCount;
        for (int i = 0; i < objCount; i++)
        {
            if (socket.GetComponent<UdpSocket>().DetectedObjects[i]["is_valid"])
            {
                count++;
            }
        }
        return count;
    }


    void SpawnBall(int i)
    {
        // spawn ball with i parameter
        Vector3 SpawnPos = Random.insideUnitSphere * SpawnRadius;
        SpawnPos = new Vector3(transform.position.x, 2, transform.position.z) + new Vector3(SpawnPos.x, 2, SpawnPos.z);
        GameObject ball = Instantiate(ballPrefab, SpawnPos, Quaternion.identity);
        ball.name = "Ball " + i;
        ball.GetComponent<BallScript>().assignedPerson = i;
    }

    void Update()
    {
        peopleCount = countValidPeople();
    }

    // Update is called once per frame
    void LateUpdate()
    {
        if (peopleCount != lastPeopleCount)
        {
            if (peopleCount > lastPeopleCount)
            {
                for (int i = lastPeopleCount; i < peopleCount; i++)
                {
                    Debug.Log(socket.GetComponent<UdpSocket>().DetectedObjects[i]);
                    if (socket.GetComponent<UdpSocket>().DetectedObjects[i]["is_valid"])
                    {
                        SpawnBall(i);
                    }
                }
            }
            else
            {
                for (int i = peopleCount; i < lastPeopleCount; i++)
                {
                    Destroy(GameObject.Find("Ball " + i));
                }
            }
        }
        else
        {
            Debug.Log("Count has not changed");
        }
        lastPeopleCount = peopleCount;
    }
}
