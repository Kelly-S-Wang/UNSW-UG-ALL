
public class Rectangle extends Shape {

	public float height;
	public float width;
	
	public Rectangle(String aName, String aColor, float aHeight, float aWidth) {
		super(aName, aColor);
		this.height = aHeight;
		this.width = aWidth;
	}
	
	public Rectangle(String aName, String aColor){
		super(aName,aColor);
	}
	
	public Rectangle(){}

	/* (non-Javadoc)
	 * @see Shape#getArea()
	 */
	@Override
	public float getArea() {
        
        return this.height * this.width;
	}

	/**
	 * @return the height
	 */
	public float getHeight() {
		return height;
	}

	/**
	 * @param height the height to set
	 */
	public void setHeight(float height) {
		this.height = height;
	}

	/**
	 * @return the width
	 */
	public float getWidth() {
		return width;
	}

	/**
	 * @param width the width to set
	 */
	public void setWidth(float width) {
		this.width = width;
	}

}
