package collections;

import java.util.List;
import java.util.ArrayList;
import java.util.Iterator;

public class ListExample {
	
	@SuppressWarnings("unused")
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
		    System.out.println(s);
		}
		
		//access via iterator
		Iterator<String> it = fruits.iterator();
		while (it.hasNext()) {
			String fruitName = it.next();
		    System.out.println(fruitName);
		}

	}
}

