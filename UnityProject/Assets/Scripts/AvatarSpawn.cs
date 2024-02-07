using System.Collections;
using System.Collections.Generic;
using SimpleJSON;
using UnityEngine;

public class AvatarSpawn : MonoBehaviour
{
    private GameObject socket;
    // avatar prefab
    public GameObject avatarPrefab;
    public float SpawnRadius = 10f;
    private int peopleCount;
    private int lastPeopleCount = 0;
    public int startX = -2;
    public int endX = 2;
    public int rangeX;

    // Start is called before the first frame update
    void Start()
    {
        socket = GameObject.Find("Socket");
        peopleCount = socket.GetComponent<UdpSocket>().peopleCount;
        rangeX = endX - startX;

        for (int i = 0; i < peopleCount; i++)
        {
            if (socket.GetComponent<UdpSocket>().DetectedObjects[i]["is_valid"])
            {
                float offsetLeft = socket.GetComponent<UdpSocket>().DetectedObjects[i]["left_offset"];
                SpawnAvatar(i, offsetLeft);
            }
        }
    }

    int CountValidPeople()
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


    void SpawnAvatar(int i, float offsetLeft)
    {
        // spawn avatar with i parameter
        float leftPos = offsetLeft * rangeX;
        Vector3 SpawnPos = new(leftPos, 0, 0);
        Quaternion SpawnRot = Quaternion.Euler(0, 180, 0);
        GameObject avatar = Instantiate(avatarPrefab, SpawnPos, SpawnRot);
        avatar.name = "Avatar " + i;
        avatar.GetComponent<AvatarScript>().assignedPerson = i;
    }

    void Update()
    {
        peopleCount = CountValidPeople();
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
                    if (socket.GetComponent<UdpSocket>().DetectedObjects[i]["is_valid"])
                    {
                        float offsetLeft = socket.GetComponent<UdpSocket>().DetectedObjects[i]["left_offset"];
                        SpawnAvatar(i, offsetLeft);
                    }
                }
            }
            else
            {
                for (int i = peopleCount; i < lastPeopleCount; i++)
                {
                    Destroy(GameObject.Find("Avatar " + i));
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
