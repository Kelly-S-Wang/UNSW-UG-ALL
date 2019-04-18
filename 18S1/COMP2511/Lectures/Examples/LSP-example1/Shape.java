
public class Shape {
  
	private String name;
	private String color;
    public static int numShapes;
    
	public Shape() {}
	public Shape(String aName, String aColor) {
	     numShapes++;
	     this.name = aName;	
	     this.color = aColor;
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

	/**
	 * @return the area
	 */
	public float getArea() {
		return 0;
	}
}
