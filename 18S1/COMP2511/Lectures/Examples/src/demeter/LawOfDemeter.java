package demeter;

public class LawOfDemeter {

	
		  private Topping cheeseTopping;
		  
		  /**
		   * Good examples of following the Law of Demeter.
		   */
		  public void goodExamples(Pizza pizza)
		  {
		    
		    // (1) it's okay to call our own methods
		    printToppings(pizza);
		    
		    // (2) it's okay to call methods on objects passed in to our method
		    float price = pizza.getPrice();
		    
		    // (3) it's okay to call methods on any objects we create
		    cheeseTopping = new CheeseTopping();
		    float weight = cheeseTopping.getWeightUsed();
		    
		    // (4) any directly held component objects
		    Foo foo = new Foo();
		    foo.doBar();
		  }
		  
		  private void printToppings(Pizza pizza) {
			// code to print toppings
		  }
		  
		  public void badExamples(Pizza pizza)
		  {
			  //chaining violates the law of demeter
			  pizza.getTopping().getWeightUsed();
		  }
		  	
}
