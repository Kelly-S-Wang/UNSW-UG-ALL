
public class CatShelter extends AnimalShelter {


	/* 
	 * @see AnimalShelter#putAnimal(Animal)
	 */
	// Java sees this as an unrelated method.  
	// This is not actually overriding parent method
	@Override
	public void putAnimal(Object someAnimal) {
		// do something
	}


	
	
	/* 
	 * @see AnimalShelter#getAnimalForAdoption()
	 */
	@Override
	public Cat getAnimalForAdoption() {

           //Returning a narrower type than parent
		   return new Cat();
	}


	

}
