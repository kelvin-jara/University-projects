package Communications.exceptions;

public class AlreadyLoggedIn extends Exception{

	/**
	 * When client tries to log in and "username" is already in use
	 */
	private static final long serialVersionUID = 7803783912231019052L;
	public AlreadyLoggedIn(String msg) {
		super(msg);
	}

}
