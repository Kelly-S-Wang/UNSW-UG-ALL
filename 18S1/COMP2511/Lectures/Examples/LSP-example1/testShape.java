public class testShape {

//	
	public void someMethod(Rectangle r) {
		r.setWidth(10);
		r.setHeight(5);
		System.out.println(r.getArea());
	}
	
	public static void main(String[] args){
		
		Shape s = new Rectangle();
		
		Rectangle rect1 = new Rectangle();
		rect1.setWidth(10);
		rect1.setHeight(5);
		
		System.out.println(Shape.numShapes);
		
		System.out.println("Rect:" + rect1.getArea());
		
		Rectangle r2 = new Square();
		r2.setWidth(5);
		System.out.println("Square:" + r2.getArea());
		
		testShape s1 = new testShape();
		s1.someMethod(rect1);
		
		s1.someMethod(r2);			
	}
}
