package patterns.strategy;

public class FlatDiscount implements IDiscount {
	
	private double percentDiscount;



	public FlatDiscount(double d) {
		this.percentDiscount = d;
	}
	
	
	@Override
	public double computeDiscount(double basePrice) {
           return basePrice * percentDiscount;
	}


}
