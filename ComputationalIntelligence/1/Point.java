import java.util.ArrayList;

public class Point {
	float x1, x2;
	int category[] = new int[3];
	
	private MyRandom myRandom = new MyRandom();
	
	public Point(float min, float max, float min2, float max2) {
		x1 = myRandom.myRand(min, max);
		x2 = myRandom.myRand(min2, max2);
	}
	public Point(String line) {
		String[] toks = line.split(" ");
		this.x1 = Float.parseFloat(toks[0]);
		this.x2 = Float.parseFloat(toks[1]);
	}
	
	public Point(Point other) {
		// TODO Auto-generated constructor stub
		this.x1 = other.x1;
		this.x2 = other.x2;
		
	}
	
	public boolean isIn(ArrayList<Point> allPoints) {
		// TODO Auto-generated method stub
		for(int i = 0; i < allPoints.size(); i++) {
			if(this.equals(allPoints.get(i))) {
				return true;
			}
		}
		return false;
	}
	
	public boolean equals(Point other) {
		return (this.x1 == other.x1 && this.x2 == other.x2);
	}
	
	public String toString() {
		return x1 + " " + x2;
	}
	public void setZero() {
		// TODO Auto-generated method stub
		x1 = 0;
		x2 = 0;
	}
	public void add(Point other) {
		// TODO Auto-generated method stub
		x1 += other.x1;
		x2 += other.x2;	
	}
	public void div(float count) {
		// TODO Auto-generated method stub
		x1 /= count;
		x2 /= count;	
	}
	
	public void setCategory() {
		if(Math.pow(x1-0.5, 2) + Math.pow(x2-0.5, 2) < 0.2 && x2 > 0.5) {
			category[0] = 1;
		}
		else if(Math.pow(x1-0.5, 2) + Math.pow(x2-0.5, 2) < 0.2 && x2 < 0.5) {
			category[1] = 1;
		}
		
		else if(Math.pow(x1+0.5, 2) + Math.pow(x2+0.5, 2) < 0.2 && x2 > -0.5) {
			category[0] = 1;
		}
		else if(Math.pow(x1+0.5, 2) + Math.pow(x2+0.5, 2) < 0.2 && x2 < -0.5) {
			category[1] = 1;
		}
		

		else if(Math.pow(x1-0.5, 2) + Math.pow(x2+0.5, 2) < 0.2 && x2 > -0.5) {
			category[0] = 1;
		}
		else if(Math.pow(x1-0.5, 2) + Math.pow(x2+0.5, 2) < 0.2 && x2 < -0.5) {
			category[1] = 1;
		}
		
		else if(Math.pow(x1+0.5, 2) + Math.pow(x2-0.5, 2) < 0.2 && x2 > 0.5) {
			category[0] = 1;
		}
		else if(Math.pow(x1+0.5, 2) + Math.pow(x2-0.5, 2) < 0.2 && x2 < 0.5) {
			category[1] = 1;
		}
		else {
			category[2] = 1;
		}
	}
}
