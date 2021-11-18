using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ClickTerrain : MonoBehaviour
{

    public GameObject[] Cubes;
    public GameObject Ghost;

    // Start is called before the first frame update
    void Start()
    {
        //make sure the objects on the table have the right color
        Cubes[0].GetComponent<Renderer>().material.color = Color.white;
        Cubes[1].GetComponent<Renderer>().material.color = Color.white;
        Cubes[2].GetComponent<Renderer>().material.color = Color.white;
        Cubes[3].GetComponent<Renderer>().material.color = Color.white;
        Cubes[4].GetComponent<Renderer>().material.color = Color.white;
        Ghost.GetComponent<Renderer>().material.color = Color.red;
    }
    // Update is called once per frame
    void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            Ray toMouse = Camera.main.ScreenPointToRay(Input.mousePosition);
            RaycastHit rhInfo;
            bool didHit = Physics.Raycast (toMouse, out rhInfo, 2000.0f);
            if (didHit)
            {
                //If clicked on something, this code will check which kind of object is clicked, looking at the attached code.
                //The corresponding script will be called to perform further actions.
                
                Movement selectScript = rhInfo.collider.GetComponent<Movement>();
                Position posScript = rhInfo.collider.GetComponent<Position>();
                //ReturnToZero ZeroScript = rhInfo.collider.GetComponent<ReturnToZero>();
                
                
                if (selectScript)
                {
                    Cubes[0].GetComponent<Renderer>().material.color = Color.white;
                    Cubes[1].GetComponent<Renderer>().material.color = Color.white;
                    Cubes[2].GetComponent<Renderer>().material.color = Color.white;
                    Cubes[3].GetComponent<Renderer>().material.color = Color.white;
                    Cubes[4].GetComponent<Renderer>().material.color = Color.white;

                    //call the function "Select" from the Movement script
                    selectScript.Select();

                }
                if (posScript)
                {
                    //call the function "PosClick" from the Position script
                    posScript.PosClick();
                }
               
            }
            else
            //if did-not-hit-anything
            {
                //Debug.Log("clicked on empty space");
                //reset (de-select) all objects
                Cubes[0].tag = "DeselectedCube";
                Cubes[1].tag = "DeselectedCube";
                Cubes[2].tag = "DeselectedCube";
                Cubes[3].tag = "DeselectedCube";
                Cubes[4].tag = "DeselectedCube";

                Cubes[0].GetComponent<Renderer>().material.color = Color.white;
                Cubes[1].GetComponent<Renderer>().material.color = Color.white;
                Cubes[2].GetComponent<Renderer>().material.color = Color.white;
                Cubes[3].GetComponent<Renderer>().material.color = Color.white;
                Cubes[4].GetComponent<Renderer>().material.color = Color.white;


            }

        }
    }
}
