package Communications;

import java.io.IOException;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import Communications.exceptions.*;
import Game.Collecto;


public class Server implements Runnable {
	/** The ServerSocket of this HotelServer.*/
	private ServerSocket ssock;
	/** List of ClientHandlers, one for each connected client. */
	private List<ClientHandler> clients;
	/**List of clients in queue. */
	private List<ClientHandler> queue;
	/**List of games. */
	private Map<ClientHandler, Collecto> games;
	/** Next client number, increasing for every new connection .*/
	private int nextClientNo;
	/** The view of this HotelServer. */
	private ServerTUI view;
	/** Server name. */
	private String serverName;
	 
	public Server() {
		clients = new ArrayList<>();
		queue = new ArrayList<>();
		view = new ServerTUI(this);
		nextClientNo = 1;
		games = new HashMap<>();
		
	}
	/**
	 * @return the name of the server.
	 */
	public String getServerName() {
		return serverName;
	}
	/**
	 * Opens a new socket by calling {@link #setup()} and starts a new
	 * ClientHandler for every connecting client.
	 * If {@link #setup()} throws a ExitProgram exception, stop the program. 
	 * In case of any other errors, ask the user whether the setup should be 
	 * ran again to open a new socket.
	 */
	public void run() {
		try {
			setup();
		} catch (Communications.exceptions.ExitProgram e2) {
			// TODO Auto-generated catch block
			e2.printStackTrace();
		}
		boolean openNewSocket = true;
		Thread t1 = new Thread(new Runnable() {
			/**
			 * Creates new games when there are 
			 */
		    @Override
		    public void run() {
		    	boolean serverRunning = true;
				while (serverRunning) {
					if (queue.size() > 2) {
						Collecto newGame = new Collecto(clients.get(0), clients.get(1));
						games.put(queue.get(0), newGame); games.put(queue.get(1), newGame);
						// send response NEWGAME to both clients.
						try {
							queue.get(0).handleCommand(ProtocolMessages.NEWGAME);
							queue.get(1).handleCommand(ProtocolMessages.NEWGAME);
						} catch (IOException e) {
							// TODO maybe add something
						}
						// remove the the two first clients form the list.
						queue.remove(0); queue.remove(0);
					}
					
				}
		    }
		});  
		t1.start();
		while (openNewSocket) {
			try {
				while (true) {
					Socket sock = ssock.accept();
					view.showMessage("New client  connected! Number of clients: " + nextClientNo);
					ClientHandler handler = new ClientHandler(sock, this);
					new Thread(handler).start();
				}
			} catch (IOException e) {
				System.out.println("A server IO error occurred: " + e.getMessage());
				if (!view.getBoolean("Do you want to open a new socket?")) {
					openNewSocket = false;
				}
			}
		}
		view.showMessage("See you later!");
	}
	/**
	 * @throws ExitProgram if a connection can not be created on the given 
	 *                     port and the user decides to exit the program.
	 * @ensures a serverSocket is opened.
	 */
	public void setup() throws ExitProgram {
		ssock = null;
		while (ssock == null) {
			serverName = view.getString("Please enter a name for the server:");
			int port = view.getInt("Please enter the server port.");
			// try to open a new ServerSocket
			try {
				view.showMessage("Attempting to open a socket at 127.0.0.1 "
						+ "on port " + port + "...");
				ssock = new ServerSocket(port, 0, 
						InetAddress.getByName("127.0.0.1"));
				view.showMessage("Server started at port " + port);
			} catch (IOException e) {
				view.showMessage("ERROR: could not create a socket on "
						+ "127.0.0.1" + " and port " + port + ".");
				if (!view.getBoolean("Do you want to try again?")) {
					throw new ExitProgram("User indicated to exit the "
							+ "program.");
				}
			}
		}
	
	}
	// ------------------ Server Methods --------------------------

	/**
	 * @requires this.clients.contains(handler)
	 */
	public void doLogin(ClientHandler handler, String username) throws AlreadyLoggedIn {
		if (clients.size() < 1) {
			handler.setUserName(username);
			clients.add(handler);
		} else {
			for (ClientHandler client: clients) {
				if (!username.equals(client.getUserName())) {
					
					handler.setUserName(username);
					clients.add(handler);
				} else {
					throw new AlreadyLoggedIn("The username is already in use.");
				}
				
			}
		}
	}
	/**
	 * Upon request a list containing the names is sent to the client.
	 * The messages to be sent is: ProtocolMessages.LIST 
	 * + ProtocolMessages.DELIMETER + [user-in-queue]
	 */
	public String doList() {
		String result = "";
		for (int i = 0; i < getQueue().size(); i++) {
			result+= ProtocolMessages.DELIMITER+ getQueue().get(i).getUserName();
		}
		return result;
	}
	/**
	 * Makes a move on the board.
	 * 1. Given a move, it checks if the move is valid
	 * 		if move is valid: move is made to the game.
	 * 			2. Server sends to clients: ProtocolMesages.MOVE  + ProtocolMessages.DELIMETER 
	 * + [move]
	 * 		if move is not valid 
	 * 			2. Server sends to clients: ProtocolMesages.ERROR + [message]
	 * 
	 */
	public void doMove(ClientHandler client, int move) throws InvalidMove {
		// TODO must also send this command to the other client handler
		boolean isvalid = false;
		if (!isvalid) {
			throw new InvalidMove("Move is not valid.");
		} else {
			// Make single move
			//upateBoards(ClientHandler client, Collecto game)
		}
		
	}
	public void doMove(ClientHandler client, int move, int move2) throws InvalidMove {
		// TODO must also send this command to the other client handler
		//------------------------------------------------
		boolean isvalid = false;
		if (!isvalid) {
			throw new InvalidMove("Move is not valid.");
		} else {
			// Make double move
			//upateBoards(ClientHandler client, Collecto game)
		}
		
	}
	/**
	 * Notifies the player that the game has ended.
	 * Sends to players: ProtocolMessages.GameOver.GAMEOVER + ProtocolMessages.DELIMETER + 
	 * [reason] + ProtocolMessages.DELIMETER + [winner - name]
	 */
	public void doGameOver() {
		//remove
		
	}
	/**
	 * 
	 * @param client
	 * @param game
	 */
	public void upateBoards(ClientHandler client, Collecto game) {
	    for (ClientHandler clientHandler : games.keySet()) {
			if (games.get(clientHandler) == games.get(client)) {
				games.replace(client, game);
				games.replace(clientHandler, game);
			}
	    }
	}
	public List<ClientHandler> getClients() {
		return clients;
	}
	public List<ClientHandler> getQueue() {
		return queue;
	}
   
	public void doQueue(ClientHandler client) {
		if (queue.contains(client)) {
			queue.remove(client);
		} else {
			queue.add(client);
			
		}
	}
	public void removeClient(ClientHandler handler) {
		clients.remove(handler);
	}
	
	public ClientHandler getPartner(ClientHandler client) {
		for (ClientHandler clientHandler : games.keySet()) {
			if (clientHandler == client) {
				return clientHandler;
			}
	    }
		return null;
	}
	
	
	public String doNewgame(ClientHandler client) {
		String results = "";
		Collecto game = getGame(client);
		// TODO game.board; ---------------------------------------
		int[] board = new int[4];  
		for (int k = 0; k < board.length; k++) {
			results += ProtocolMessages.DELIMITER+ board[k]  ;
		}
		return results;
	}
	
	public Collecto getGame(ClientHandler client) {
		return games.get(client);
	}

		// ------------------ Main --------------------------

	/** Start a new HotelServer. */
	public static void main(String[] args) {
		Server server = new Server();
		System.out.println("Welcome to the Games Server! Starting...");
		new Thread(server).start();
	}
	
	
}
