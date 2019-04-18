
public class TestShape {

	public static void main(String[] args) {
		
		// Creating a shape object with a no-arg constructor
		Shape shape2 = new Shape();
		shape2.setName("Circle");
		shape2.setColor("Red");
		
		// Creating a shape object with constructor with two aruments
		Shape shape1 = new Shape("Rectangle","Red");
		shape1.setName("Rectangle");
		shape1.setColor("Red");
		
		//Creating a rectangle object
		Rectangle rect = new Rectangle("Rectangle","red",10,8);
		System.out.println(rect.getArea());
		System.out.println(rect);
		rect.drawARect();
		
		//Defining reference variable to be base class shape and instantiate Rectangle
		Shape shape4 = new Rectangle("Rectangle","red",20,8);
		System.out.println(shape4);
		//Dynamic binding ensures getArea() from rectangle is invoked at run-time
		System.out.println("Shape4 area:" + shape4.getArea());
		
		// The line below is a compiler-error, because shape4 is a reference variable of type Shape
		// Hence cannot access methods in the Rectangle class
		// shape4.drawARect();
		
	}
}
