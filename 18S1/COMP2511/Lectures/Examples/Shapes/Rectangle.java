
public class Rectangle extends Shape {

	private double width;
	private double height;
	
	public Rectangle(String aName, String aColor, double wid, double hei) {
		super(aName, aColor);
		System.out.println("Inside rectangle constructor, iniliasing height,width");
		this.width = wid;
		this.height = hei;
	}

	/* (non-Javadoc)
	 * @see Shape#toString()
	 */
	@Override
	public String toString() {
		
		String message = super.toString() + ",area: " + this.getArea();
		return message;
	}

	/* (non-Javadoc)
	 * @see Shape#getArea()
	 */
	@Override
	public double getArea() {
		return this.width * this.height;
	}
	
	/*
	 * Some method to draw a rectangle
	 */
	public void drawARect() {
		//code to draw a rectangle
	}

	/**
	    * Check if one object is equal to this employee
	    * @param otherObject object to compare if is equal to this object
	    */
    public boolean equals(Object otherObject)
    {
	       if (this == otherObject) return true;
	       if (otherObject == null) return false;
	       if (getClass() != otherObject.getClass()) return false;
	       Rectangle other = (Rectangle) otherObject;
	       return this.getName().equals(other.getName()) && this.height == other.height && this.width == other.width;
    }
   
   
	
	
	
	
}
