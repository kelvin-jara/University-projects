using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Movement: MonoBehaviour
{
    private GameObject[] cubes;
    private GameObject ghost;
    GameObject Ghostmover;

    //function that will select the object that is clicked and deselect all other objects.
    public void Select()
    {
            string selectedCube = name;

        //first deselect all objects that were selected (tagged with "selectedcube") before
            cubes = GameObject.FindGameObjectsWithTag("SelectedCube");
            foreach (GameObject cube in cubes)
            {
                for (int i = 0; i < cubes.Length; i++)
                {
                    cubes[i].tag = "DeselectedCube";
                }
            }

            //thenselect the clicked object with the following line
            this.tag = "SelectedCube";

            //make the selected object blue
            Renderer rend;
            rend = GetComponent<Renderer>();
            rend.material.SetColor("_Color", Color.blue);

            //ghost is activated
            ghost = GameObject.FindGameObjectWithTag("GhostOff");
            //ghost.tag = "Ghost";
    }

    public void GhostAway()
    {

        //Code that moves ghost object out of screen
        Ghostmover = GameObject.FindWithTag("Ghost");
        Ghostmover.transform.position = new Vector3(-200, 1, -100);

    }


}
