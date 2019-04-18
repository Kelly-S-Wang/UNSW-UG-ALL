package relationships;

public class Car {
	Engine engine;
	String make;
	String model;
	Person person;
	
	
	public Car(String make, String model){
		this.make = make;
		this.model = model;
	}
	// Coding for composition
	// Using composition - a life-time lock, but when whole is created, the part is also created
	public Car(int engineSize, int numCylinders, String make, String model){
		this.engine = new Engine(engineSize, numCylinders);
		this.make = make;
		this.model = model;
	}
	
	// Coding for aggregation
	// Using aggregation - a life-time lock, but when whole is created, the part that already
	// exists is passed into the constructor
    public Car(Engine engine, String make, String model){
		this.engine = engine;
		this.make = make;
		this.model = model;
	}
	
	//coding for association - "uses"
	/**
	 * @param person the person to set
	 */
	public void setPerson(Person person) {
		this.person = person;
	}
	
	public static void main(String [] args) {
	
		//Showing association of car to person
		Car car = new Car("Mercedes","E-Class");
		Person person = new Person();
		car.setPerson(person);
		
		//Client using composition
					
		Car car1 = new Car(2000,6,"Ford","Scorpio");
		
		//Client using aggregation - passing in already existing part e.g., Engine
		Engine engine = new Engine(2000,6);
		Car car2 = new Car(engine, "Mercedes", "c-class");
			
	}

}
