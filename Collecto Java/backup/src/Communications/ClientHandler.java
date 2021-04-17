package Communications;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.Socket;

import Communications.exceptions.AlreadyLoggedIn;
import Communications.exceptions.InvalidMove;
import Game.Collecto;

public class ClientHandler implements Runnable{
	/** The socket and In- and OutputStreams. */
	private BufferedReader in;
	private BufferedWriter out;
	private Socket sock;
	private Server srv;
	/** Name of this ClientHandler. */
	private String name;
	private String username = "NotDefined";
	private boolean loggedin;

	
	/**
	 * Constructs a new HotelClientHandler. Opens the In- and OutputStreams.
	 * 
	 * @param sock The client socket
	 * @param srv  The connected server
	 * @param name The name of this ClientHandler
	 */
	public ClientHandler(Socket sock, Server srv) {
		try {
			in = new BufferedReader(
					new InputStreamReader(sock.getInputStream()));
			out = new BufferedWriter(
					new OutputStreamWriter(sock.getOutputStream()));
			this.sock = sock;
			this.srv = srv;
		} catch (IOException e) {
			shutdown();
		}
	}
	/**
	 * Continuously listens to client input and forwards the input to the
	 * {@link #handleCommand(String)} method.
	 */
	public void run() {
		String msg;
		try {
			msg = in.readLine();
			while (msg != null) {
				System.out.println("> [" + username + "] Incoming: " + msg);
				handleCommand(msg);
				out.newLine();
				out.flush();
				msg = in.readLine();
				
			}
			
			shutdown();
		} catch (IOException e) {
			System.out.println("Shutdown!!!");
			shutdown();
		}
	}
	/**
	 * Handles commands received from the client by calling the according 
	 * methods at the HotelServer. For example, when the message "i Name" 
	 * is received, the method doIn() of HotelServer should be called 
	 * and the output must be sent to the client.
	 * 
	 * If the received input is not valid, send an "Unknown Command" 
	 * message to the server.
	 * 
	 * @param msg command from client
	 * @throws IOException if an IO errors occur.
	 */
	
	void handleCommand(String msg) throws IOException {
		
		String[] msgArray = msg.split(ProtocolMessages.DELIMITER);
		String action = msgArray[0];
		switch (action) {
			case ProtocolMessages.HELLO:
				String message = "Server by " + srv.getServerName();
				out.write(ProtocolMessages.HELLO + ProtocolMessages.DELIMITER + message);
				break;
			case ProtocolMessages.LOGIN:
				try {
					// add the list of clients on server.
					srv.doLogin(this, msgArray[1]);
					out.write(ProtocolMessages.LOGIN);
				
					loggedin = true;
				} catch (AlreadyLoggedIn o) {
					out.write(ProtocolMessages.ALREADYLOGGEDIN);
				}
				break;
			case ProtocolMessages.LIST:
				if (loggedin) {
					String messageList = ProtocolMessages.LIST;
					messageList += srv.doList();
					out.write(messageList);
				} else {
					out.write(ProtocolMessages.ERROR + ProtocolMessages.DELIMITER 
							+ " You need to LogIn first");
				}
			  	break;
			case ProtocolMessages.QUEUE:
				if (loggedin) {
					srv.doQueue(this);
				} else {
					out.write(ProtocolMessages.ERROR + ProtocolMessages.DELIMITER 
							+ " You need to LogIn first");
				}
				break;
			case ProtocolMessages.MOVE:
				if (loggedin) {
					int i = 0;
					int j = 0;
					if (msgArray.length == 2) {
						try {
							i = Integer.parseInt(msgArray[1]);
							try {
								srv.doMove(this, i);
								String txt= ProtocolMessages.MOVE + ProtocolMessages.DELIMITER + i;
								out.write(txt);
								messageToPartner(txt);
							} catch (InvalidMove e) {
								out.write(ProtocolMessages.ERROR + e.getMessage() );
							}
							
						} catch (NumberFormatException e) {
							out.write(ProtocolMessages.ERROR + ProtocolMessages.DELIMITER 
									+ " mve must be integer.");
						}
					} else if (msgArray.length == 3) {
						try {
							i = Integer.parseInt(msgArray[1]);
							j = Integer.parseInt(msgArray[2]);
							try {
								srv.doMove(this, i, j);
								String output = ProtocolMessages.MOVE + ProtocolMessages.DELIMITER 
										+ i + ProtocolMessages.DELIMITER + j;
								out.write(output);
								messageToPartner(output);
							} catch (InvalidMove e) {
								out.write(ProtocolMessages.ERROR + e.getMessage());
							}
						} catch (NumberFormatException e) {
							out.write(ProtocolMessages.ERROR + ProtocolMessages.DELIMITER 
									+ " mve must be integer.");
						}
					}
					// after each move check if game is over.
					// TODO check how to make game over. ---------------
					// add DISCONNECT, VICTORY or DRAW.
					boolean gameOver = false;
					if (gameOver) {
						String msgGameover = ProtocolMessages.GAMEOVER + ProtocolMessages.DELIMITER;
						 msgGameover += ""; //---------------------------
						out.write(msgGameover);
						messageToPartner(msgGameover);
						// TODO maybe shutdown here
					}
				} else {
					out.write(ProtocolMessages.ERROR + ProtocolMessages.DELIMITER 
							+ " You need to LogIn first.");
				}
				break;
			case ProtocolMessages.NEWGAME:
				String msgNewgame = ProtocolMessages.NEWGAME + ProtocolMessages.DELIMITER;
				msgNewgame += srv.doNewgame(this);
				msgNewgame += ProtocolMessages.DELIMITER + getUserName() 
					+ ProtocolMessages.DELIMITER + srv.getPartner(this).getUserName();  
				out.write(msgNewgame);
				out.newLine();
				out.flush();
				break;
			case ProtocolMessages.ERROR:
				out.write(ProtocolMessages.ERROR);
				break;
			default:
				System.out.println("Unkown command: " + action);
		}

	}
	/**
	 * Shut down the connection to this client by closing the socket and 
	 * the In- and OutputStreams.
	 */
	private void shutdown() {
		System.out.println("> [" + name + "] Shutting down.");
		try {
			loggedin = false;
			in.close();
			out.close();
			sock.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
		srv.removeClient(this);
	}
	public String getUserName() {
		return username;
	}
	public void setUserName(String username) {
		this.username = username;
	}
	public boolean getLoggedIn() {
		return loggedin;
	}
	/**
	 * Given a message it sends the message to the other client.
	 */
	public void messageToPartner(String msg) {
		ClientHandler other = srv.getPartner(this);
		BufferedWriter out = other.getBufferWrite();
		try {
			out.write(msg);
			out.newLine();
			out.flush();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	public BufferedWriter getBufferWrite() {
		return this.out;
	}
	
}
