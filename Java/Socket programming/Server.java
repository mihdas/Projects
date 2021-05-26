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

import java.net.*; 
import java.io.*; 
import java.util.*;
import java.awt.*;
import java.awt.geom.AffineTransform;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.nio.ByteBuffer;
import javax.imageio.ImageIO;
import javax.swing.*;

class Draw_Graph1 extends JPanel {
    int width;
    int height;
    Node[] nodes=new Node[5];
    ArrayList<edge> edges;
    public Draw_Graph1() { //Constructor
        
	edges = new ArrayList<>();
	width = 30;
	height = 30;
    }
    class Node {
	int x, y;
	String name;
	
	public Node(String myName, int myX, int myY) {
	    x = myX;
	    y = myY;
	    name = myName;
	}
    }    
    class edge {
	int i,j;
	
	public edge(int start_node, int dest_node) {
	    i = start_node;
	    j = dest_node;	    
	}
    }    
    public void addNodes() { 
	//add a node at pixel (x,y)
	nodes[0]=(new Node("A",175,50));
        nodes[1]=(new Node("B",50,100));
        nodes[2]=(new Node("C",300,100));
        nodes[3]=(new Node("D",50,200));
        nodes[4]=(new Node("E",300,200));
	this.repaint();
    }
    public void addEdge(int i, int j) {
	//add an edge between nodes i and j
	edges.add(new edge(i,j));
	this.repaint();
    }
    private static final Polygon ARROW_HEAD = new Polygon();
    static {
        ARROW_HEAD.addPoint(0, 0);
        ARROW_HEAD.addPoint(-5, -30);
        ARROW_HEAD.addPoint(5, -30);
    }
    @Override
    protected void paintComponent(Graphics g) { // draw the nodes and edges
	FontMetrics f = g.getFontMetrics();
	int nodeHeight = Math.max(height, f.getHeight());

	g.setColor(Color.black);
	for (edge e : edges) {
            

            Graphics2D g2 = (Graphics2D) g;
            g2.setStroke(new BasicStroke(2));
            double angle = Math.atan2(nodes[e.j].y - nodes[e.i].y, nodes[e.j].x - nodes[e.i].x);
            g2.drawLine(nodes[e.i].x, nodes[e.i].y, (int) (nodes[e.j].x - 10 * Math.cos(angle)), (int) (nodes[e.j].y - 10 * Math.sin(angle)));
            AffineTransform tx1 = g2.getTransform();
            AffineTransform tx2 = (AffineTransform) tx1.clone();
            tx2.translate(nodes[e.j].x, nodes[e.j].y);
            tx2.rotate(angle - Math.PI / 2);
            g2.setTransform(tx2);
            g2.fill(ARROW_HEAD);
            g2.setTransform(tx1);
            
           
	}

	for (Node n : nodes) {
	    int nodeWidth = Math.max(width, f.stringWidth(n.name)+width/2);
	    g.setColor(Color.white);
	    g.fillOval(n.x-nodeWidth/2, n.y-nodeHeight/2, 
		       nodeWidth, nodeHeight);
	    g.setColor(Color.black);
	    g.drawOval(n.x-nodeWidth/2, n.y-nodeHeight/2, 
		       nodeWidth, nodeHeight);
	    
	    g.drawString(n.name, n.x-f.stringWidth(n.name)/2,
			 n.y+f.getHeight()/2);
	}
    }
    
    }

  
public class Server 
{ 
    //initialize socket and input stream 
    private Socket          socket   = null; 
    private ServerSocket    server   = null; 
    private DataInputStream in       =  null;
    private DataOutputStream outputStream=null;
    static int[][] arr=new int[5][5];
    static int[][][] r1=new int[5][5][5];
    boolean exist;
    int n,nod1,nod2;
    
    public int str2int(String s){
        if (s.charAt(0)=='A'){
        return 0;}
        else if (s.charAt(0)=='B'){
        return 1;}
        else if (s.charAt(0)=='C'){
        return 2;}
        else if (s.charAt(0)=='D'){
        return 3;}
        else
            return 4;
    }
    
    public boolean pathfind(int n, int node1, int node2){
        for (int h=0;h<n;h++){
            for (int i=0;i<5;i++){               
                for (int j=0;j<5;j++){
                    r1[h][i][j]=0;
                    
                    for (int k=0;k<5;k++){
                        if(h==0){
                            r1[h][i][j]+=arr[i][k]*arr[k][j];
                            
                        }
                        else{
                        r1[h][i][j]+=arr[i][k]*r1[h-1][k][j]; }
                    }
                }
            }
        }
        
        if(r1[n-1][node1][node2]!=0){
            return true;
        }
        else{
        return false;
        }

    }
  
    // constructor with port 
    public Server(int port) 
    { 
        // starts server and waits for a connection 
        try
        { 
            server = new ServerSocket(port); 
            System.out.println("Server started"); 
  
            System.out.println("Waiting for a client ..."); 
  
           // while(true){
                socket = server.accept();
                System.out.println("Connected to client");
                in= new DataInputStream(socket.getInputStream());
                outputStream=new DataOutputStream(socket.getOutputStream());
                for(int i=0;i<5;i++) {
                    for(int j=0;j<5;j++) {
                    arr[i][j] = in.readInt();
                    //System.out.print(String.valueOf(arr[i][j]));
                }
                    //System.out.println("");
                }
                n=in.readInt();
                nod1=str2int(in.readUTF());
                nod2=str2int(in.readUTF());
//                System.out.println(n);
//                System.out.println(nod1);
//                System.out.println(nod2);
                exist =pathfind(n,nod1,nod2);
                if(exist){
                    //System.out.println("YESS");
                outputStream.writeChar('Y');
                }
                else{
                    //System.out.println("NOOO");
                    outputStream.writeChar('N');
                }
                //BufferedImage image = ImageIO.read(("Graph.jpg"));
                

        
                
                
                
            JFrame f = new JFrame();
        f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        f.setSize(400, 300);
	Draw_Graph1 panel = new Draw_Graph1();
	panel.setSize(350,250);
	panel.setVisible(true);
	panel.addNodes();
	for(int i=0;i<5;i++){
            for(int j=0;j<5;j++){
                if (arr[i][j]>0){
                    panel.addEdge(i, j);
                }
            }
        }
        f.add(panel);     
        
        f.setVisible(true);
        
        try
        {
            BufferedImage image = new BufferedImage(400,300, BufferedImage.TYPE_INT_RGB);
            Graphics2D graphics2D = image.createGraphics();
            f.paint(graphics2D);
            ImageIO.write(image,"jpeg", new File("Graph.jpeg"));
            
            
                    BufferedImage image1 = ImageIO.read(new File("Graph.jpeg"));

        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        ImageIO.write(image1, "jpeg", byteArrayOutputStream);

        byte[] size = ByteBuffer.allocate(4).putInt(byteArrayOutputStream.size()).array();
        outputStream.write(size);
        outputStream.write(byteArrayOutputStream.toByteArray());
        outputStream.flush();
        System.out.println("Response Sent   Current time in milliseconds: " + System.currentTimeMillis());

        Thread.sleep(5000);
        //System.out.println("Closing: " + System.currentTimeMillis());
        socket.close();
        }
        catch(Exception exception)
        {
            //code
            exception.printStackTrace();
        }
    
            //}
     
  
            // close connection 
            
        } 
        catch(IOException i) 
        { 
            System.out.println(i); 
        } 
    } 
  
    public static void main(String args[]) 
    { 
        Server server = new Server(5000);
        
    } 
} 