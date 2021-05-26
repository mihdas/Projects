/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package cn;

/**
 *
 * @author Mihir
 */
import java.awt.image.BufferedImage;
import java.net.*; 
import java.io.*; 
import java.nio.ByteBuffer;
import javax.imageio.ImageIO;
  
public class Client 
{ 
    // initialize socket and input output streams 
    private Socket socket            = null; 
    private InputStream  inputStream   = null; 
    private DataInputStream in=null;
    private DataOutputStream out     = null;
    public int[][] arr={{0,0,0,0,1},{1,0,1,1,0},{1,1,0,0,0},{0,1,0,0,0},{1,0,0,1,0}};
    public int n=3;
    public String Node_1="C";
    public String Node_2="E";
    
  
    // constructor to put ip address and port 
    public Client(String address, int port) 
    { 
        // establish a connection 
        try
        { 
            socket = new Socket(address, port); 
            System.out.println("Client Running....");
            System.out.println("Connected"); 
  
            
            inputStream  = socket.getInputStream();
            in=new DataInputStream(socket.getInputStream());
  
             
            out    = new DataOutputStream(socket.getOutputStream()); 
        } 
        catch(UnknownHostException u) 
        { 
            System.out.println(u); 
        } 
        catch(IOException i) 
        { 
            System.out.println(i); 
        } 
        try{
            for(int i=0;i<5;i++){
                for(int j=0;j<5;j++){
                out.writeInt(arr[i][j]);//send adjacency matrix
                }
            }
            out.writeInt(n);//sending N
            out.writeUTF(Node_1);//send Node 1
            out.writeUTF(Node_2);//send node 2
            
            System.out.println("Receiving data from server    Current time in milliseconds:   " + System.currentTimeMillis());
            char output=in.readChar();
            System.out.println("OUTPUT:");
            System.out.println(output);
            

        byte[] sizeAr = new byte[4];
        inputStream.read(sizeAr);
        int size = ByteBuffer.wrap(sizeAr).asIntBuffer().get();

        byte[] imageAr = new byte[size];
        inputStream.read(imageAr);

        BufferedImage image = ImageIO.read(new ByteArrayInputStream(imageAr));

        System.out.println("Received Image " + image.getHeight() + "x" + image.getWidth() + "   Current time in milliseconds: " + System.currentTimeMillis());
        ImageIO.write(image, "jpeg", new File("Graph_copy.jpeg"));
        

            
            } 
        catch(IOException i) 
            { 
                System.out.println(i); 
            }
        try
        { 
//            input.close(); 
//            out.close(); 
//            socket.close(); 
        } 
        catch(Exception i) 
        { 
            System.out.println(i); 
        } 
} 
  
        // close the connection 
        

  
    public static void main(String args[]) 
    { 
        Client client = new Client("127.0.0.1", 5000); 
    } 
} 
