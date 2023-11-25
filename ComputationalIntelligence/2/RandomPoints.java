import java.util.ArrayList;

public class RandomPoints {
	private ArrayList<Point> allPoints = new ArrayList<Point>();
	
	public void createRandomPoints(int N, float min, float max, float min2, float max2){
		ArrayList<Point> points = new ArrayList<Point>();
		
		for(int i = 0; i < N; i++) {
			Point p;
			do {
				p = new Point(min, max, min2, max2);
			}while(p.isIn(allPoints));
			points.add(p);
			allPoints.add(p);
		}
		
	}
	
	public ArrayList<Point> getAllPoints(){
		return allPoints;
	}
}
