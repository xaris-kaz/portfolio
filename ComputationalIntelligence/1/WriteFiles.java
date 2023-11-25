import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.PrintWriter;
import java.util.ArrayList;

public class WriteFiles {

	private static void writeToFile(String name, ArrayList<Point> allPoints, int start, int stop) {
		try {
			PrintWriter writer = new PrintWriter(new FileOutputStream(name));
			for(int i = start; i < stop; i++) {
				writer.println(allPoints.get(i));
			}
			writer.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		RandomPoints randomPoints = new RandomPoints();
		randomPoints.createRandomPoints(8000, -1, 1, -1, 1);
		ArrayList<Point> allPoints = randomPoints.getAllPoints();
		writeToFile("train.txt", allPoints, 0, 4000);
		writeToFile("test.txt", allPoints, 4000, 8000);
		
		randomPoints = new RandomPoints();
		
		randomPoints.createRandomPoints(150, 0.8f, 1.2f, 0.8f, 1.2f);
		randomPoints.createRandomPoints(150, 0.0f, 0.5f, 0.0f, 0.5f);
		randomPoints.createRandomPoints(150, 0.0f, 0.5f, 1.5f, 2.0f);
		randomPoints.createRandomPoints(150, 1.5f, 2.0f, 0.0f, 0.5f);
		randomPoints.createRandomPoints(150, 1.5f, 2.0f, 1.5f, 2.0f);
		randomPoints.createRandomPoints(75, 0.8f, 1.2f, 0.0f, 0.4f);
		randomPoints.createRandomPoints(75, 0.8f, 1.2f, 1.6f, 2.0f);
		randomPoints.createRandomPoints(75, 0.3f, 0.7f, 0.8f, 1.2f);
		randomPoints.createRandomPoints(75, 1.3f, 1.7f, 0.8f, 1.2f);
		randomPoints.createRandomPoints(150, 0.0f, 2.0f, 0.0f, 2.0f);

		allPoints = randomPoints.getAllPoints();
		writeToFile("points.txt", allPoints, 0, allPoints.size());
		
		
	}

}
