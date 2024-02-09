using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SpaceDimensionController : MonoBehaviour
{
    public GameObject StartXY;
    public GameObject EndX;
    public GameObject EndY;
    public float RangeX = 0.0f;
    public float RangeY = 0.0f;
    public float[] StartXYValue = new float[2];
    public float EndXValue = 0.0f;
    public float EndYValue = 0.0f;
    // Start is called before the first frame update
    void Start()
    {
        StartXYValue = new float[2];

        // Origin
        StartXYValue[0] = StartXY.transform.position.x;
        StartXYValue[1] = StartXY.transform.position.y;

        // End X and Y values
        EndXValue = EndX.transform.position.x;
        EndYValue = EndY.transform.position.y;

        // Range X and Y values
        RangeX = EndXValue - StartXYValue[0];
        RangeY = EndYValue - StartXYValue[1];
    }
}
