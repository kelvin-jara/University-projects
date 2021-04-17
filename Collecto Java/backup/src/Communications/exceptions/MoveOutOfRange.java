package Communications.exceptions;

public class MoveOutOfRange extends Exception{
	/**
	 * This exception is throw when a move is intended outside the board.
	 */
	private static final long serialVersionUID = -6583976398554102673L;

	public MoveOutOfRange() {
		super("Move out of board");
	}
	
}
