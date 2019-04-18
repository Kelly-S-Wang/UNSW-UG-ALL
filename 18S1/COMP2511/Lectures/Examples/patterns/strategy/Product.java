package patterns.strategy;

public class Product {
	
	String name;
	double price;
	IDiscount discount;
	
	public Product(String name, double price, IDiscount discount) {
		this.name = name;
		this.price = price;
		this.discount = discount;
	}
	
	double computePrice() {
		return this.price - discount.computeDiscount(this.price);
	}
	
	
	

}
