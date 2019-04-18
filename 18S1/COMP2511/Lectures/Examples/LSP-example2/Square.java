
public class Square extends Rectangle {

	
	public Square() {
		super();
	}
	
	public Square(String aName, String aColor, float aLength){
		super(aName,aColor,aLength,aLength);
	}
	
    @Override
	public void setWidth(float aWidth){
		super.setWidth(aWidth);
		super.setHeight(aWidth);
	}
	
	public void setHeight(float aHeight){
		super.setWidth(aHeight);
		super.setHeight(aHeight);
	}
}
