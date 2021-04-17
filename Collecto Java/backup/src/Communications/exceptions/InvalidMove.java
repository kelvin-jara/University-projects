package Communications.exceptions;

public class InvalidMove extends Exception {

	/**
	 * Exception is throw when a move is invalid.
	 */
	private static final long serialVersionUID = -4994792320381471790L;
	public InvalidMove(String msg) {
		super(msg);
	}
	
}
