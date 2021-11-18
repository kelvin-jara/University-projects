using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System;

public class PythonConector : MonoBehaviour
{
    
    string address = "127.0.0.1";
    int port = 12345;
    Socket server; //server socket
    Socket client; //user socket
    IPAddress ip;
    byte[] bytes = null;
    public GameObject[] Cubes;
    void Start()
    {
        StartSocket();
       //SocketLoop();
    }
    /*
    public void SocketLoop()
    {
        while (true)
        {
            for (int i = 0; i < Cubes.Length; i++)
            {

                String msg = "";
                float x = Cubes[i].transform.position.x;
                float z = Cubes[i].transform.position.z;
                msg = x.ToString("R") + " : " + z.ToString("R");
                Debug.Log(msg);
            }
        }
    }
    */
    public void StartSocket()
    {
        //address = GetHostIP(); //= "127.0.0.1";
        server = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        ip = IPAddress.Parse(address);
        //server.Bind(new IPEndPoint(ip, port));
        IPEndPoint remoteEP = new IPEndPoint(ip, 12345);
        server.Connect(remoteEP);
        bytes = new byte[1024];
        int bytesRec = server.Receive(bytes);
        Debug.Log("Echoed test = {0}" +
            Encoding.UTF8.GetString(bytes, 0, bytesRec));
        


    }
    public static string GetHostIP()
    {
        string ret = "";
        IPAddress[] ips = Dns.GetHostEntry(Dns.GetHostName()).AddressList;
        foreach (IPAddress ip in ips)
        {
            if (ip.AddressFamily == AddressFamily.InterNetwork)
            {
                ret = ip.MapToIPv4().ToString();
            }
        }
        if (ret == "")
        {
            return null;
        }
        return ret;
    }

    // Update is called once per frame
    
    void Update()
    {
        for (int i = 0; i < Cubes.Length; i++)
        {
            
            String msg = "";
            //Here you have to include the length of both links
            float x = (float)(Cubes[i].transform.position.x* (45.5 / 350.0)) ;
            float z = (float)(  Cubes[i].transform.position.z* ( 45.5 / 350.0));
            msg = Cubes[i].name + " : " + x.ToString("R") + " : " + z.ToString("R")+" ? ";
            Debug.Log(msg);
            byte[] byData = Encoding.UTF8.GetBytes(msg);
            server.Send(byData);
            
        }
        


    }
}
