import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Random;
import java.util.Scanner;

public class MLP {
	private static int N = 4000;
	private static int K = 3;
	private static int d = 2;
	
	private static int H1 = 5;
	private static int H2 = 10;
	private static int H3 = 15;
	
	private static int type = 2;
	private static float n = (float) 0.0001;
	
	private static int B = N/10;	
	
	private static float[] y0 = new float[d]; 
	private static float[][] w1 = new float[H1][d];
	private static float[] b1 = new float[H1];
	private static float[] u1 = new float[H1];
	private static float[] y1 = new float[H1];
	private static float[] d1 = new float[H1];
	private static float[][] dEw1 = new float[H1][d];
	private static float[] dEb1 = new float[H1];
	private static float[][] w2 = new float[H2][H1];
	private static float[] b2 = new float[H2];
	private static float[] u2 = new float[H2];
	private static float[] y2 = new float[H2];
	private static float[] d2 = new float[H2];
	private static float[][] dEw2 = new float[H2][H1];
	private static float[] dEb2 = new float[H2];
	private static float[][] w3 = new float[H3][H2];
	private static float[] b3 = new float[H3]; 
	private static float[] u3 = new float[H3];
	private static float[] y3 = new float[H3];
	private static float[] d3 = new float[H3];
	private static float[][] dEw3 = new float[H3][H2]; 
	private static float[] dEb3 = new float[H3];
	private static float[][] w4 = new float[K][H3];
	private static float[] b4 = new float[K];
	private static float[] u4 = new float[K];
	private static float[] y4 = new float[K];
	private static float[] d4 = new float[K];
	private static float[][] dEw4 = new float[K][H3];
	private static float[] dEb4 = new float[K];

	private static MyRandom myRandom = new MyRandom();
	
	private static ArrayList<Point> trainPoints = new ArrayList<Point>();
	private static ArrayList<Point> testPoints = new ArrayList<Point>();
	
	private static void readFromFile(String filename, ArrayList<Point> points){
		try {
			Scanner scanner = new Scanner(new FileInputStream(filename));
			int i = 0;
			while(scanner.hasNextLine()) {
				String line = scanner.nextLine();
				Point p = new Point(line);
				points.add(p);
				p.setCategory();
			}
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	
	
	private static float g(float u) {
		if(type == 0){
        	return  (float) (1.0/(1.0+Math.exp(-1.0*u)));
        }
        else if(type == 1){
            return (float) Math.tanh(u);
        }
        else{
        	if(u > 0){
    	        return u;
    	    }
    	    return 0;
        }
	}
	private static float gPar(float u) {
		if(type == 0){
        	return  u*(1.0f - u);
        }
        else if(type == 1){
            return (float) (1.0f - Math.tanh(u)*Math.tanh(u));
        }
        else{
        	if(u > 0){
    	        return 1;
    	    }
    	    return 0;
        }
	}
	private static void forward_pass(Point p, float[] y){
	    int i,j;

	    y0[0] = p.x1;
	    y0[1] = p.x2;
	    
	    for(i = 0; i < H1; i++){
	        u1[i] = 0;
	        for(j = 0; j< d; j++){
	            u1[i] = u1[i] + w1[i][j]*y0[j];
	        }
	        u1[i] = u1[i] + b1[i];

	        y1[i] = g(u1[i]);
	    }

	    for(i = 0; i < H2; i++){
	        u2[i] = 0;
	        for(j = 0; j < H1; j++){
	            u2[i] = u2[i] + w2[i][j]*y1[j];
	        }
	        u2[i] = u2[i]+b2[i];
	        y2[i] = g(u2[i]);
	         
	    }	

	    for(i = 0; i < H3; i++){
	        u3[i]=0;
	        for(j = 0; j < H2; j++){
	            u3[i] = u3[i] + w3[i][j]*y2[j];
	        }
	        u3[i] = u3[i] + b3[i];
	        y3[i] = g(u3[i]);
	    }
	    
	    for(i = 0; i < K; i++){
	        u4[i]=0;
	        for(j = 0; j < H3; j++){
	            u4[i] = u4[i] + w4[i][j]*y3[j];
	        }
	        u4[i] = u4[i] + b4[i];
	        y4[i] = (float) (1.0/(1.0+Math.exp(-1.0*u4[i])));
	        y[i] = y4[i];
	    }
	}
	private static void calcError(Point p, float[] y) {
	    float sum = 0;
		for(int i = 0; i < K; i++){
	        d4[i] = (float) (y[i]*(1.0-y[i])*(y[i]-p.category[i]));
	    }
	    for(int i = 0; i < H3; i++){
	        sum = 0;
	        for(int j = 0;j < K; j++){
	            sum += w4[j][i]*d4[j];
	        }
	        if(type == 0){
	        	d3[i] = (float) (y3[i]*(1.0-y3[i])*sum);
	        }
	        else {
	        	d3[i]= gPar(u3[i])*sum;
	        }
	    }
	    for(int i = 0; i < H2; i++){
	        sum = 0;
	        for(int j = 0;j < H3; j++){
	            sum += w3[j][i]*d3[j];
	        }
	        if(type == 0){
	        	d2[i] = (float) (y2[i]*(1.0-y2[i])*sum);
	        }
	        else {
	        	d2[i]= gPar(u2[i])*sum;
	        }
	    }

	    for(int i = 0; i < H1; i++){
	        sum=0;
	        for(int j = 0; j < H2; j++){
	            sum += w2[j][i]*d2[j];
	        }

	        if(type == 0){
	        	d1[i] = (float) (y1[i]*(1.0-y1[i])*sum);
	        }
	        else {
	        	d1[i]= gPar(u1[i])*sum;
	        }
	        
	    }
	}
	
	private static void calcPar() {

	    for(int i = 0; i < H1; i++){
	        dEb1[i] += d1[i];
	        for(int j = 0; j < d; j++){
	            dEw1[i][j] += d1[i]*y0[j];
	        }
	    }

	    for(int i = 0; i < H2; i++){
	        dEb2[i] += d2[i];
	        for(int j = 0; j < H1; j++){
	            dEw2[i][j] += d2[i]*y1[j];
	        }
	    }

	    for(int i = 0; i < H3; i++){
	        dEb3[i] += d3[i];
	        for(int j = 0; j < H2; j++){
	            dEw3[i][j] += d3[i]*y2[j];
	        }
	    }
	    
	    for(int i = 0; i < K; i++){
	        dEb4[i] += d4[i];
	        for(int j = 0; j < H3; j++){
	            dEw4[i][j] += d4[i]*y3[j];
	        }
	    }
	}
	private static void backprop(Point p){
	    float y[] = new float[K];

	    forward_pass(p, y);
	    calcError(p, y);
	    calcPar();
	}

	private static void updateWeights(){
	    int i,j;
	    
	    for(i = 0; i < H1; i++){
	        b1[i] -= n*dEb1[i];
	        for(j = 0; j < d; j++){
	            w1[i][j] -= n*dEw1[i][j];
	        }
	    }
	    for(i = 0; i < H2; i++){
	        b2[i] -= n*dEb2[i];
	        for(j = 0; j < H1; j++){
	            w2[i][j] -= n*dEw2[i][j];
	        }
	    }

	    for(i = 0; i < K; i++){
	        b3[i] -= n*dEb3[i];
	        for(j = 0; j < H2; j++){
	            w3[i][j] -= n*dEw3[i][j];
	        }
	    }
	    
	    for(i = 0; i < K; i++){
	        dEb4[i] += d4[i];
	        for(j = 0; j < H3; j++){
	            dEw4[i][j] += d4[i]*y3[j];
	        }
	    }
	    init();
	}

	private static void init(){
	    int i, j;
	    
	    for(i = 0; i < H1; i++){
	        dEb1[i] = 0;
	        for(j = 0; j < d; j++){
	            dEw1[i][j] = 0;
	        }
	    }
	
	    for(i = 0; i < H2; i++){
	        dEb2[i] = 0;
	        for(j = 0; j < H1; j++){
	            dEw2[i][j] = 0;
	        }
	    }
	
	    for(i = 0; i < H3; i++){
	        dEb3[i] = 0;
	        for(j = 0; j < H2; j++){
	            dEw3[i][j] = 0;
	        }
	    }
	    
	    for(i = 0; i < K; i++){
	        dEb4[i] = 0;
	        for(j = 0; j < H3; j++){
	            dEw4[i][j] = 0;
	        }
	    }
	    
	}
	
	private static void gradient_descent(){
	    int epoch = 0;
	    float y[] = new float[K];
	    float error = 0, errorNew=0;
	    int i,j;
	    
	    while(epoch < 700 || Math.abs(error - errorNew) > 0.0001){
	        error = errorNew;
	        
	        for(i = 0; i < N; i++){
	            backprop(trainPoints.get(i));
	            if(i % B == 0){
	               updateWeights(); 
	            }
	        }
	        
	        errorNew = 0;
	        for(i = 0; i < N; i++){
	            forward_pass(trainPoints.get(i),y);
	            
	            for(j = 0; j < K; j++){
	                errorNew += Math.pow(y[j] - (float)trainPoints.get(i).category[j], 2);
	            }
	        }
	        errorNew /= 2.0;
	        
	        epoch++;
	        System.out.println(epoch + ": " + errorNew);

	    }
	}

	private static void test(){
	    int i,j;
	    float y[] = new float[K];
	    int c;
	    int count = 0;
	    
		try {
			PrintWriter writer1 = new PrintWriter(new FileOutputStream("wright.txt"));
			PrintWriter writer2 = new PrintWriter(new FileOutputStream("wrong.txt"));
			for(i = 0; i < N; i++){
		        forward_pass(testPoints.get(i), y);
		        
		        c = 0;
		        for(j = 0; j < K; j++){
		            if(y[c] < y[j]){
		                c = j;
		            }
		        }
		        
		        if(testPoints.get(i).category[c] == 1){
		            count++;
		            writer1.println(testPoints.get(i).x1 + " " + testPoints.get(i).x2);
		        }
		        else{
		            writer2.println(testPoints.get(i).x1 + " " + testPoints.get(i).x2);
		        }
		    }
		    
		    System.out.println("Ratio= " + 100*count/(float)N);
			PrintWriter writer3 = new PrintWriter(new FileOutputStream("stats.txt", true));

		    writer3.println(H1 + "\t" + H2 + "\t" + H3 + "\t" + B + "\t" + type + "\t" + n  + "\t" + 100*count/(float)N);
		    
		    writer1.close();
		    writer2.close();
		    writer3.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}
	public static void main(String[] args) {
		readFromFile("train.txt", trainPoints);
		readFromFile("test.txt", testPoints);
		
		 for(int i = 0; i < H1; i++){
		        b1[i] = myRandom.myRand(-1, 1);
		        for(int j = 0; j < d; j++){
		            w1[i][j] = myRandom.myRand(-1, 1);
		        }
		    }

		    for(int i = 0; i < H2; i++){
		        b2[i]=myRandom.myRand(-1, 1);
		        for(int j = 0; j < H1; j++){
		            w2[i][j] = myRandom.myRand(-1, 1);
		        }
		    }

		    for(int i = 0; i < H3; i++){
		        b3[i] = myRandom.myRand(-1, 1);
		        for(int j = 0; j < H2; j++){
		            w3[i][j] = myRandom.myRand(-1, 1);
		        }
		    }
		    
		    for(int i = 0; i < K; i++){
		        b4[i] = myRandom.myRand(-1, 1);
		        for(int j = 0; j < H3; j++){
		            w4[i][j] = myRandom.myRand(-1, 1);
		        }
		    }
		    init();
		    gradient_descent();
		    test();
	}
}
