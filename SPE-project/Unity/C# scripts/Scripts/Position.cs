using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class Position : MonoBehaviour
{
    private Grid grid;
    GameObject Cubemover;
    GameObject Ghostmover;

    private void Awake()
    {
        grid = FindObjectOfType<Grid>();
    }

    //code that initiates the movement of an object after it already has been selected
    public void PosClick()
    {
        //find point that has been clicked and use this point in the MoveCubeNear function
        Ray toMouse = Camera.main.ScreenPointToRay(Input.mousePosition);
        RaycastHit rhInfo;
        if (Physics.Raycast(toMouse, out rhInfo, 2000.0f))
        {
            
            MoveCubeNear(rhInfo.point);

        }

    }

    
    //funciton that moves the selected object (which is tagged with the "selectedcube" tag) to the clicked point.
    private void MoveCubeNear(Vector3 clickPoint)
    {
        var gridPosition = grid.GetNearestPointOnGrid(clickPoint);
        Cubemover = GameObject.FindWithTag("SelectedCube");
        Cubemover.transform.position = new Vector3(gridPosition.x, 12, gridPosition.z);


    }

    //code that initiates the ghost moving function:
    public void PosGhost()
    {
        //find point and use this point in the MoveGhostNear function
        Ray toMouse = Camera.main.ScreenPointToRay(Input.mousePosition);
        RaycastHit rhInfo;
        if (Physics.Raycast(toMouse, out rhInfo, 2000.0f))
        {

            MoveGhostNear(rhInfo.point);

        }

    }
    //funciton that moves the ghost object
    private void MoveGhostNear(Vector3 clickPoint)
    {
        var gridPosition = grid.GetNearestPointOnGrid(clickPoint);
        Ghostmover = GameObject.FindWithTag("Ghost");
       // Ghostmover.transform.position = gridPosition;
        Ghostmover.transform.position = new Vector3(gridPosition.x, 11, gridPosition.z);
    }

    public void GhostAway()
    {

        //move ghost object out of screen if no object is selected
        Ghostmover = GameObject.FindWithTag("Ghost");
        Ghostmover.transform.position = new Vector3(-200, 1, -100);

    }

}
