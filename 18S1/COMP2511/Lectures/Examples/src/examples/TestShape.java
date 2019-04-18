package examples;
public class TestShape {

	public static void main(String[] args) {
		
		
		//Defining reference variable to be base class shape and instantiate Rectangle
		//Assignment b = a is valid if actual type of a is a sub-type of b
		Shape2D shape4 = new Rectangle("Rectangle","red",20,8);
		System.out.println(shape4);
		
		//Polymorphism and Dynamic binding ensures getArea() from rectangle is invoked at run-time
		System.out.println("Shape4 area:" + shape4.getArea());
		
		// The line below is a compiler-error, because shape4 is a reference variable of type Shape
		// Hence cannot access methods in the Rectangle class
		// shape4.drawARect();
		
		//Defining reference variable to be interface type
		Graphics graphicObject = new Rectangle("Rectangle", "blue", 10, 6);
		graphicObject.drawShape();
		
		
	}
}
