using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HoverGhostScript : MonoBehaviour
{
    private Grid grid;
    private Vector3 mousePosition;
    private GameObject Ghost2;
    GameObject Ghostmover;


    //code that will detect wether the mouse is ("hovering") over the table and if an object is selected. If both are true, a ghost object should follow the cursor by using a grid
    private void OnMouseEnter()
    {
        grid = FindObjectOfType<Grid>();
        
    }
    private void OnMouseOver()
    {
        Debug.Log("Mouse is over table");
        if (Input.GetMouseButton(0))
        {

        }
        else
        {
            if (GameObject.FindGameObjectsWithTag("SelectedCube").Length == 1)
            {
                Ray toMouse = Camera.main.ScreenPointToRay(Input.mousePosition);
                RaycastHit rhInfo;
                if (Physics.Raycast(toMouse, out rhInfo, 2000.0f))
                {

                    MoveGhost2Near(rhInfo.point);

                }
            }
        }
        
    }

    //code that moves ghost object out of screen
    private void OnMouseExit()
    {
        Ghostmover = GameObject.FindWithTag("Ghost");
        Ghostmover.transform.position = new Vector3(-200, 1, -100);

    }

    //code that moves ghost to a grid point close to the cursor.
    private void MoveGhost2Near(Vector3 clickPoint)
    {
        var gridPosition = grid.GetNearestPointOnGrid(clickPoint);
        Ghost2 = GameObject.FindWithTag("Ghost");
       // Ghost2.transform.position = gridPosition;
        Ghost2.transform.position = new Vector3(gridPosition.x, 11, gridPosition.z);
    }
    }
