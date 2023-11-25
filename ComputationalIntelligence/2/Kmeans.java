import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;

public class Kmeans {

	private static int N = 1200;
	private static int M = 12;
	
	private static MyRandom myRandom = new MyRandom();
	
	private static ArrayList<Point> allPoints = new ArrayList<Point>();
	private static ArrayList<Point> centers = new ArrayList<Point>();
	private static int group[] = new int[M];
	
	private static void readFromFile() {
		Scanner scanner;
		try {
			scanner = new Scanner(new FileInputStream("points.txt"));
			while(scanner.hasNextLine()) {
				String line = scanner.nextLine();
				allPoints.add(new Point(line));
			}
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	private static void initCenter(){
	   int i, j;
	   centers.clear();
	   
	   for(i = 0; i < M; i++){
	        do{
	            j = myRandom.myRand(N);
	            
	            Point p;
				do {
					p = allPoints.get(j);
				}while(p.isIn(centers));
				centers.add(new Point(p));
	        }
	        while(j < i);
	    }
	}

	private static double distance(Point p1, Point p2){
	    return Math.sqrt(Math.pow(p1.x1-p2.x1, 2) + Math.pow(p1.x2-p2.x2,2));
	}

	private static int newGroup(){
	    int i = 0, j;
	    int count = 0, pos;
	    double dist, min = 0;
	    
	    for(i = 0; i < N; i++){
	        pos = -1;
	        Point p = allPoints.get(i);
	        for(j = 0; j < M; j++){
	            dist = distance(p, centers.get(j));
	            if(j == 0 || dist < min){
	                min = dist;
	                pos = j;
	            }
	        }
	        if(pos != group[i]){
	            count++;
	        }
	        group[i] = pos;
	    }
	    return count;
	}
	
	private static void newCenter(){
	    int i;
	    int counters[] = new int[M];
	    
	    for(i = 0; i < M; i++){
	        centers.get(i).setZero();
	    }
	    for(i = 0; i < N; i++){
	        centers.get(group[i]).add(allPoints.get(i));
	        
	        counters[group[i]]++;
	    }
	    
	    for(i = 0; i < M; i++){
	    	centers.get(i).div(counters[i]);
	    }
	}

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		int i;
	    
		readFromFile();
		
	    group = new int[N];

	    double sum;
	    int count;
	    
	   			
		for(int k = 0; k < 15; k++){
	        initCenter();
	        count = 1;
	        while(count > 0){
	            count = newGroup();
	            newCenter();
	        }
	        
	        sum = 0;
	        for(i = 0; i < N; i++){
	            sum += distance(centers.get(group[i]), allPoints.get(i));
	        }
	        
	        System.out.println("sum = " + sum);
	        
	        
	        for(i = 0; i < M; i++){
	        	System.out.println(centers.get(i));
	        }
	        System.out.println();
	    }
			
	}

}
