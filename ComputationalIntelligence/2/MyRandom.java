import java.util.Random;

public class MyRandom {
	private Random random = new Random();
	
	public float myRand(float min, float max) {
		return random.nextFloat()*(max - min) + min;
	}
	
	public int myRand(int N) {
		return random.nextInt(N);
	}
}
