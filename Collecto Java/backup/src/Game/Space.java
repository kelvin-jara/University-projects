package Game;

public class Space {
	int color;
	int location;
	
	public Space(int location) {
		color = 0;
		this.location = location;
	}
	
	public int getColor() {
		return color;
	}
	
	public int getLocation() {
		return location;
	}
}
