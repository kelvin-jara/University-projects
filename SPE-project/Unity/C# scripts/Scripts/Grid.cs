using UnityEngine;

public class Grid : MonoBehaviour
{
    [SerializeField]
    private float size = 1f;

    public Vector3 GetNearestPointOnGrid(Vector3 position)
    {
         position -= transform.position;

         int xCount = Mathf.RoundToInt(position.x / size);
         int yCount = Mathf.RoundToInt(position.y / size);
         int zCount = Mathf.RoundToInt(position.z / size);

         Vector3 result = new Vector3(
             (float)xCount * size,
             (float)yCount * size,
             (float)zCount * size);

           /*  Vector3 result = new Vector3(
            (float)size /2,
            (float)size /2,
            (float)size /2);*/
         result += transform.position;

         return result;

       
    }

    //code that will show the grid in the Unity3d world editor
    private void OnDrawGizmos()
    {
        Gizmos.color = Color.yellow;
        for (float x = 0; x < 750; x += size)
        {
            for (float z = 0; z < 750; z += size)
            {
                var point = GetNearestPointOnGrid(new Vector3(x, 0f, z));
                Gizmos.DrawSphere(point, 1.0f);
            }

        }
    }
}