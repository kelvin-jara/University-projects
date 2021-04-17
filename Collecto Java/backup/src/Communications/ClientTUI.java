package Communications;

import java.io.PrintWriter;
import java.util.Scanner;

import Communications.exceptions.ExitProgram;
import Communications.exceptions.MoveOutOfRange;

public class ClientTUI {
	
	public ClientTUI(Client client) {
		this.client = client;
		console = new PrintWriter(System.out, true);
		scan = new Scanner(System.in);
	}
	private Client client;
	private PrintWriter console;
	private Scanner scan;
	/**
	 * Creates a loop for the use to input commands and handle them.
	 * When the users input "exit" the loops breaks.
	 */
	public void start() {
		
		String input;
		while (true) {
			input = scan.nextLine();
			try {
				handleUserInput(input);
			} catch (ExitProgram e) {
				showMessage(e.getMessage());
			}
		}
	}
	/**
	 * Handles the actions the user wants to perform.
	 * @param input
	 * @throws ExitProgram 
	 */
	private void handleUserInput(String input) throws ExitProgram {
		String[] splitted = input.split("\\s+"); // Split on space
		String commandString = splitted[0]; // Safe since input != empty
		String cmd1 = null;
		String cmd2 = null;
		if (splitted.length > 1) {
			cmd1 = splitted[1];
			if (splitted.length > 2) {
				cmd2 = splitted[2];
			}
		}
		switch (commandString) {
			case ProtocolMessages.LOGIN:
				client.doLogin();
				break;
			case ProtocolMessages.LIST:
				client.doList();
				break;
			case ProtocolMessages.QUEUE:
				client.doQueue();
				break;
			case ProtocolMessages.MOVE:
				int[] moves	=  null;
				if (splitted.length == 1) {
						moves = new int[1];
						moves[0] = Integer.parseInt(cmd1);
				}		
				else if  (splitted.length == 2) {
					moves[0] = Integer.parseInt(cmd1);
					moves[1] = Integer.parseInt(cmd2);
				}
				try {
					client.doMove(moves);
				} catch (MoveOutOfRange e) {
					showMessage(e.getMessage());
					break;
				}
				break;
			case ProtocolMessages.HELP:
				printHelpMenu();
				break;
			case ProtocolMessages.EXIT:
				throw new ExitProgram("User exited");
			default:
				System.out.println("Unkown command: " + commandString);
				printHelpMenu();
		}
		
	}
	/**
	 * Given and message, it is displayed to the user through the console.
	 * @param message
	 */
	public void showMessage(String message) {
		console.println(message);
	}
	/**
	 * 
	 * @param question
	 * @return
	 */
	public String getString(String question)  {
		showMessage(question);
		return scan.nextLine();
	}
	/**
	 * 
	 */
	public boolean getBoolean(String question)  {
		showMessage(question + ". Y/N");
		String input = scan.nextLine();
		if (input.equals("Y")) { 
			return  true;
		}
		return false;
	}
	/**
	 * 
	 */
	public void printHelpMenu() {
		// TODO the printMenu should print the commands available with each step.
		String result ="This commands are available.\n";
		result += "LOGIN username ........To claim a name on the server.\n" + 
				"QUEUE .......................To get in the list to play.\n" + 
				"LIST ............To see which players are waiting in the list.\n"+
				"MOVE number.....To make a single move.\n" +
				"MOVE number number....To make double move \n."
				+ "help .....To print this menu.\n"
				+ "exit ... To quit the program.\n"
				+ "hint....To see what moves are available\n";
		showMessage(result);
	}
}
