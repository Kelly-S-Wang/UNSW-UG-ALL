package collections;

import java.util.List;
import java.util.ArrayList;
import java.util.Iterator;

public class FruitListExample {
	
	public static void main(String[] args) {
		List<String> fruits = new ArrayList<>();
		fruits.add("apple");
		fruits.add("orange");
		
		// Three methods of access
		
		//access via index
		String fruit1 = fruits.get(0);
		String fruit2 = fruits.get(1);
		
		
		//access via new for-loop
		for(String s : fruits) {
		    String f = s;
		}
	}

}
