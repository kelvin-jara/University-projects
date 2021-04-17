package Game;

public class Board {
	int boardSize;
	Ball[] board;
	
	public Board() {
		boardSize = 7;
		board = new Ball[boardSize*boardSize];
		populateBoard();
	}
	
	public void populateBoard() {
		
	}
	
	public Board getBoard() {
		return this;
	}
	
	public String toString() {
		String s = "";
		
		return s;
	}
	
	public void doMove(int move) {
		
	}
}
