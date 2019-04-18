package examples;

public abstract class Shape2D implements Graphics {

	private String name;
	private String color;
	
	
	public Shape2D(String name, String color) {
		this.name = name;
		this.color = color;
	}
	
	public Shape2D(String name) {
		this.name = name;
	}
	
	/**
	 * @return the name
	 */
	public String getName() {
		return name;
	}
	/**
	 * @param name the name to set
	 */
	public void setName(String name) {
		this.name = name;
	}
	/**
	 * @return the color
	 */
	public String getColor() {
		return color;
	}
	/**
	 * @param color the color to set
	 */
	public void setColor(String color) {
		this.color = color;
	}
	
	@Override
	public String toString() {
		return "Shape: " + this.name + ",colour: " + this.color;
	}
	
	public double getArea() {
		
		return 0.0;
	}
	
}
