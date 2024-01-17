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

    // Start is called before the first frame update
    void Start()
    {
        socket = GameObject.Find("Socket");
        peopleCount = socket.GetComponent<UdpSocket>().peopleCount;

        for (int i = 0; i < peopleCount; i++)
        {
            if (socket.GetComponent<UdpSocket>().DetectedObjects[i]["is_valid"])
            {
                SpawnAvatar(i);
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


    void SpawnAvatar(int i)
    {
        // spawn avatar with i parameter
        Vector3 SpawnPos = Random.insideUnitSphere * SpawnRadius;
        SpawnPos = new Vector3(transform.position.x, 0, transform.position.z) + new Vector3(SpawnPos.x, 0, SpawnPos.z);
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
                        SpawnAvatar(i);
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
