package patterns.strategy;

public class PercentDiscount implements IDiscount {
	
	private double percentDiscount;



	public PercentDiscount(double d) {
		this.percentDiscount = d;
	}
	
	
	@Override
	public double computeDiscount(double basePrice) {
           return basePrice * percentDiscount;
	}


}
