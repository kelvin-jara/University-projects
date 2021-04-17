package Communications;

import java.io.PrintWriter;
import java.io.Writer;
import java.util.Scanner;

public class ServerTUI {
	/** The PrintWriter to write messages to */
	private Writer console;
	private Scanner scanner ;
	private Server server;
	
	public ServerTUI(Server server) {
		this.server = server;
		console = new PrintWriter(System.out, true);
		scanner = new Scanner(System.in);
	}
	public void showMessage(String message) {
		((PrintWriter) console).println(message);
		
	}
	public String getString(String question) {
	showMessage(question);
	return scanner.nextLine();
	}
	public boolean getBoolean(String question)  {
		showMessage(question + ". Y/N");
		String input = scanner.nextLine();
		if (input.equals("Y")) { 
			return  true;
		}
		return false;
	}
	/**
	 * 
	 * @param question
	 * @return
	 * @requires Integer.parseInt(scanner.nextLine()) == Integer
	 */
	public int getInt(String question) {
		int result = 8888;
		boolean correctInput = true;
		while (correctInput) {
			String input  =getString(question);
			try {
				result = Integer.parseInt(input);
				correctInput = false;
			} catch (NumberFormatException e) {
				continue;
			}

		}
		return result;
	}

}
