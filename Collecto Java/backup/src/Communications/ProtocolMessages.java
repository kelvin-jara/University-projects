package Communications;

public class ProtocolMessages {
	/**
	 * Sent as last line in a multi-line response to indicate the end of the text.
	 */
	public static final String EOM = "\n";
	/**
	 * Delimiter used to separate arguments sent over the network.
	 */
	public static final String DELIMITER = "~";
	/** Used for the server-client handshake. */
	public static final String HELLO = "HELLO";

	/**
	 * The following chars are both used by the TUI to receive user input, and the
	 * server and client to distinguish messages.
	 */
	public static final String LOGIN = "LOGIN";
	public static final String LIST = "LIST";
	public static final String QUEUE = "QUEUE";
	public static final String MOVE = "MOVE";
	/**
	 * The following three commands are for the server only.
	 */
	public static final String NEWGAME = "NEWGAME";
	public static final String ALREADYLOGGEDIN = "ALREADYLOGGEDIN";
	public static final String GAMEOVER = "GAMEOVER";
	public static final String ERROR = "ERROR";
	/**
	 * Commands that are executed internally by the client only.
	 */
	public static final String HELP = "help";
	public static final String HINT = "hint";
	public static final String EXIT = "exit";
	/**
	 * Commands for Game Over.
	 */
	public static final String DISCONNECT = "DISCONNECT";
	public static final String VICTORY = "VICTORY";
	public static final String DRAW = "DRAW";

}
