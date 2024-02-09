using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SceneController : MonoBehaviour
{

    private GameObject[] avatars;
    // Start is called before the first frame update
    void Start()
    {
        // get all gameobjects with the tag "Avatar"
        avatars = GameObject.FindGameObjectsWithTag("Avatar");



    }

    // Update is called once per frame
    void Update()
    {
        foreach (GameObject avatar in avatars)
        {
            if (avatar.GetComponent<NewAvatarController>().isArmsUp)
            {
                Debug.Log("Arms Up");
            }
        }

    }
}
