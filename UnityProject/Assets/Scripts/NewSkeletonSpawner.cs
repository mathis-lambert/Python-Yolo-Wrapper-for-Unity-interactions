using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NewSkeletonSpawner : MonoBehaviour
{
    private GameObject socket;
    // avatar prefab
    public GameObject avatarSkeletonPrefab;
    public float SpawnRadius = 10f;
    private int peopleCount;
    private int lastPeopleCount = 0;
    public GameObject SpaceDimensions;
    private SpaceDimensionController spaceDimensionController;
    public int assignedPerson;
    private float StartX;
    private float EndX;
    private float RangeX;

    // Start is called before the first frame update
    void Start()
    {
        socket = GameObject.Find("Socket");
        peopleCount = socket.GetComponent<UdpSocket>().peopleCount;
        spaceDimensionController = SpaceDimensions.GetComponent<SpaceDimensionController>();

        for (int i = 0; i < peopleCount; i++)
        {
            if (socket.GetComponent<UdpSocket>().DetectedObjects[i]["is_valid"])
            {
                float offsetLeft = socket.GetComponent<UdpSocket>().DetectedObjects[i]["offset"][0];
                float offsetBottom = socket.GetComponent<UdpSocket>().DetectedObjects[i]["offset"][1];
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


    void SpawnAvatar(int i, float offsetLeft, float offsetBottom = 0)
    {
        string name = "NewSkeleton " + i;
        // spawn avatar with i parameter
        if (!GameObject.Find(name))
        {
            float leftPos = offsetLeft * RangeX;
            float height = offsetBottom * 10;
            Vector3 SpawnPos = new(leftPos, height, transform.position.z);
            Quaternion SpawnRot = Quaternion.Euler(0, 180, 0);
            GameObject avatar = Instantiate(avatarSkeletonPrefab, SpawnPos, SpawnRot);
            avatar.name = name;
            avatar.GetComponent<NewAvatarController>().assignedPerson = i;
        }
    }

    void Update()
    {
        peopleCount = CountValidPeople();
        StartX = spaceDimensionController.StartXYValue[0];
        EndX = spaceDimensionController.EndXValue;
        RangeX = spaceDimensionController.RangeX;
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
