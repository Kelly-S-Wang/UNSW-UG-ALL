package patterns.strategy;

public class TestDiscount {
public static void main(String[] args) {
		
		Product ball = new Product("a ball", 20, new PercentDiscount(0.2));
		System.out.println("Price of " + ball.name + ":"  + ball.computePrice());
	}
}
