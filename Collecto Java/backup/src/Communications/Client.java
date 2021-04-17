package Communications;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.ConnectException;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Scanner;
import Communications.exceptions.*;
import Game.Collecto;
import Players.Player;
/**
 * Client for player to connect to server.
 * @ author Kelvin Jaramillo.
 */
public class Client {
	
	private Socket serverSocket;
	private BufferedReader in;
	private BufferedWriter out;
	private Player player;
	private ClientTUI view;
	private String name;
	private boolean loggedIn = false;
	private boolean inQueue = false;
	private boolean onGame = false;
	private String line ;
	public Thread t1;
	
	/**
	 * Constructs a new clients.
	 */
	public Client() {
		view  = new ClientTUI(this);
	}
	/**
	 * Starts a new connection  with the server, and then  the HELLO message is sent to the server.
	 */
	private void star() {
		boolean connectToNewServer = true;
		while (connectToNewServer) {
			createConnection();
			try {
					// Do the HELLO handshake; show welcome to the user
				try {
					handleHello();
				} catch (ProtocolException e) {
					view.showMessage(e.getMessage());
					view.showMessage("The protocol was not respected. "
							+ "Try connecting to a new server.");
					clearConnection();
					continue; // Continue with the next while loop;
				}
				// Show the available commands
				view.printHelpMenu();
				view.start();
			} catch (ServerUnavailableException e) {
				view.showMessage("Something went wrong. "
						+ e.getMessage());
				clearConnection();
			}
			connectToNewServer = view.getBoolean("Do you want to " + "connect to a new server?");
		}
		view.showMessage("See you later!");
	}
	/**
	 * Ask the user for input : < IP-address  port-number use-name>. 
	 * Then  it tries to connect to the server.
	 * @throws IOException 
	 */
	public void createConnection()  {
		clearConnection();
		while (serverSocket == null) {
			String input = view.getString("Input: " + " <IP-address>  <port-number> <use-name>");
			String[] inputSplit = input.split(" ");
			if (inputSplit.length == 1 || inputSplit.length > 3) {
				view.showMessage("Incorrect input, try again.");
				continue;
			}
			String host = inputSplit[0];
			System.out.println(host);
			int port; 
			try {
				port = Integer.parseInt(inputSplit[1]);
			} catch (NumberFormatException e) {
				view.showMessage("Port number is not valid, enter integers only");
				continue;
			}
			name = inputSplit[2];   // the gets set here for the client
			InetAddress ip;
			try {
				if (host.equals("127.0.0.1")) {
					ip = InetAddress.getByName(host);
				} else {
					ip = InetAddress.getByName(host); 
				}
			} catch (UnknownHostException e) {
				view.showMessage("IP-address is not valid, enter valid IP");
				continue;
			}
			view.showMessage("Attempt to connect to " + ip + ":" + port + "...");
			try {
				serverSocket = new Socket(ip, port);
				in = new BufferedReader(new InputStreamReader(
						serverSocket.getInputStream()));
				out = new BufferedWriter(new OutputStreamWriter(
						serverSocket.getOutputStream()));
			} catch (IOException r) {
				view.showMessage("ERROR: could not create a socket on " 
						+ host + " and port " + port + "." + " Please try again.");
				continue;
			}
		}
	}
	/**
	 * Clears the socket and the stream inputs and outputs.
	 */
	private void clearConnection() {
		serverSocket = null;
		in = null;
		out = null;
	}
	
	/**
	 * Sends a message to the connected server, followed by a new line. 
	 * The stream is then flushed.
	 * 
	 * @param msg the message to write to the OutputStream.
	 * @throws ServerUnavailableException if IO errors occur.
	 */
	public synchronized void sendMessage(String msg) 
			throws ServerUnavailableException {
		if (out != null) {
			try {
				out.write(msg);
				view.showMessage(">[ YOU ] Sending: " + msg);
				out.newLine();
				out.flush();
			} catch (IOException e) {
				view.showMessage(e.getMessage());
				throw new ServerUnavailableException("Could not write "
						+ "to server.");
			}
		} else {
			throw new ServerUnavailableException("Could not write "
					+ "to server.");
		}
	}
	/**
	 * Reads and returns one line from the server.
	 * 
	 * @return the line sent by the server.
	 * @throws ServerUnavailableException if IO errors occur.
	 */
	public String readLineFromServer() 
			throws ServerUnavailableException {
		if (in != null) {
			try {
				// Read and return answer from Server
				String answer = in.readLine();
				view.showMessage(">[Server] Incomnig: " + answer);
				if (answer == null) {
					throw new ServerUnavailableException("Could not read "
							+ "from server.");
				}
				return answer;
			} catch (IOException e) {
				throw new ServerUnavailableException("Could not read "
						+ "from server.");
			}
		} else {
			throw new ServerUnavailableException("Could not read "
					+ "from server.");
		}
	}
/**
 *Handles the initial connection between client and server.
 * 1. Sends a message to the server: 
 *   ProtocolMessages.HELLO + (message + (user's-name))
 *   2. Server returns on line containing:
 *   ProtocolMessages.HELLO + ProtocolMessages.DELIMITER + (message).
 * @throws ServerUnavailableException
 * @throws ProtocolException
 */
	public void handleHello() 
			throws ServerUnavailableException, ProtocolException {
		sendMessage(ProtocolMessages.HELLO + ProtocolMessages.DELIMITER + " Client by KJ");
		readLineFromServer();
	}
	/**
	 *Sends a login request to the server.
	 * 1. The request message is: ProtocolMessages.LOGIN + (user's-name)
	 * 2. Server responds
	 * if message equal to: ProtocolMessages.LOGIN, login is successful
	 * if message not equal to: ProtocolMessages.LOGIN, login is successful and the server returns:
	 * ProtocolMessages.ALREADYLOGIN, in which case the user has to try another name.
	 */
	public void doLogin() {
		try {
			sendMessage(ProtocolMessages.LOGIN + ProtocolMessages.DELIMITER +name);
		} catch (ServerUnavailableException e) {
			view.showMessage(e.getMessage());
		}
		String input;
		try {
			input = readLineFromServer();
			String[] inputSplit = input.split(ProtocolMessages.DELIMITER);
			if (inputSplit[0].equals(ProtocolMessages.ALREADYLOGGEDIN)) {
				view.showMessage("The user name" + name + " already exits on the server.");
			} else if (inputSplit[0].equals(ProtocolMessages.LOGIN)) {
				loggedIn = true;
				view.showMessage("Loggin successful, you can now get in queue.");
			}
		} catch (ServerUnavailableException e) {
			view.showMessage(e.getMessage());
		}
		
		
	}
	/**
	 * Sends a queue request to the server.
	 * 1. The request message is: ProtocolMessages.QUEUE + ProtocolMessages.DELIMETER + [user-name].
	 * 2. Check if client was put on list by sending a LIST request: ProtocolMessages.QUEUE.
	 * Then the server checks if there is other player available to create a game.
	 * If the server starts a new game.
	 * 2. The server then indicates that the user can start a game by message:
	 * ProtocolMessages.NEWGAME + ProtocolMessages.DELIMETER + <cell value>^49
	 * + ProtocolMessages.DELIMETER +  <player name>*
	 * If the method is called again then it means the user want to be taken out the queue.
	 * @assert !onGame
	 */
	public void doQueue() {
		if (loggedIn & !onGame) {
			try {
				sendMessage(ProtocolMessages.QUEUE);
				if (inQueue == false) {
					inQueue = true;
				} else {
					inQueue = false;
				}
				toPlay();
			} catch (ServerUnavailableException e) {
				view.showMessage(e.getMessage());
			}
		} else {
			view.showMessage("Please logging first");
			view.printHelpMenu();
		}
	}
	/**
	 * Checks if the move is valid
	 * 	Sends a do move request to the server.
	 * 1. ProtocolMessages.MOVE + ProtocolMessages.DELIMITER + (move).
	 * If valid move then server respond with: ProtocolMessages.MOVE + 
	 * ProtocolMessages.DELIMITER + (move)
	 * else if invalid move the server responds with: ERROR+[no valid messages].
	 * @param move 
	 * @assert 27 <= move >=0
	 * @throws MoveOutOfBounds 
	 */
	public void doMove(int[] move) throws MoveOutOfRange {
		for (int i = 0; i < move.length; i++) {
			if (move[i] < 0 || move[i] < 27 ) {
				throw new MoveOutOfRange();
			} else {
				continue;
			}
		}
		if (loggedIn & onGame) {
			String message = "";
			try {
				message = ProtocolMessages.MOVE + ProtocolMessages.DELIMITER ;
				for (int i = 0; i < move.length; i++) {
					message += move[i];
				}
				sendMessage(message);
			} catch (ServerUnavailableException e) {
				view.showMessage(e.getMessage());
			}
			
		}
	}
	/**
	 * Sends LIST request to the server to see the clients that are already connected to the server.
	 * 1. The message for request is: ProtocolMessages.List + ProtocolMessages.DELIMETER
	 * 2. The server responds with a list of clients connected to server as: ProtocolMessages.List 
	 * + ProtocolMessages.DELIMETER + [user-names]*
	 */
	
	public void doList() {
		
		if (loggedIn) {
			String message = "";
			try {
				message = ProtocolMessages.LIST ;
				sendMessage(message);
				if (!inQueue) {
					inQueue = true;
					String input = readLineFromServer();
					toPlay();
					
				}
			} catch (ServerUnavailableException e) {
				view.showMessage(e.getMessage());
			}
		} else {
			view.showMessage("You need LogIn first.");
		}
		
	}
	/**
	 * Shows the user possible moves that are legal.
	 */
	public void doHint() {
		//TODO define well how to get the possible moves that are legal. 
		// player.getBoard().getValidMoves
		// view.showMessage(valid moves)
	}
	public synchronized String getLine() {
		String result = "";
		return this.line;
	}
	public synchronized void setLine(String line) {
		this.line = line;
	}
	
	public void toPlay() {
		t1 = new Thread(new Runnable() {
		    @Override
		    public void run() {
				BufferedReader extraIn = null;
				try {
					extraIn = new BufferedReader(new InputStreamReader(
							serverSocket.getInputStream()));
				} catch (IOException e1) {
					e1.printStackTrace();
				} 
				String input;
				while (true) {
					try {
						input = extraIn.readLine();
						view.showMessage(">[Server] Incomnig: " + input);
						String[] inputSplit = input.split(ProtocolMessages.DELIMITER);
						if (inputSplit[0].equals(ProtocolMessages.NEWGAME)) {
							onGame = true;
						} else if(inputSplit[0].equals(ProtocolMessages.MOVE)){
							// TODO make move 
						} else if(inputSplit[0].equals(ProtocolMessages.ERROR)& onGame == true){
							view.showMessage("Error has occured");
						} else {
							view.showMessage("Setting line to:" + input);
							setLine(input);
							
						}
					} catch (IOException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
				}
		    	
		    }
		});  
		t1.start(); 
	}
	/**
	 * 
	 * @param args
	 */	
	public static void main(String[] args) {
		(new Client()).star();
	}
	
	
	
}
