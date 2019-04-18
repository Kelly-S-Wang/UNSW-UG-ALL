package examples;

import java.util.ArrayList;
import java.util.List;

public class UnsafeList {


	static long sum(Number[] numbers) {
		long sum=0;
		for (Number n:numbers) {
			sum += n.longValue();
		}
		return sum;
	}
	
	static long sum(List<? extends Number> numbers) {
		long sum=0;
		for (Number n:numbers) {
			sum += n.longValue();
		}
		return sum;
	}
	
	static boolean addNumber(List<? super Integer> list, Number n) {
		list.add((Integer) n);
		return true;
	}
	
	public static void main(String[] args) {
		// Example 1: Co-variant arrays
		Number[] numbers = new Number[3];
		numbers[0] = new Integer(10);
		numbers[1] = new Double(3.14);
		numbers[2] = new Byte((byte) 0);

		// Example 2: If s <= t, then s[] <= t[]
		Integer[] intArray = { 1,3,5,7};
		Double[]  doubleArray = {1.5, 3.0, 4.5};
		Number[]  numArray = intArray;
		
		System.out.println(UnsafeList.sum(intArray));
		System.out.println(UnsafeList.sum(doubleArray));
		
		// Example 3: Lists are not covariant
		List<Integer> intList1 = new ArrayList<Integer>();
		intList1.add(1);
		intList1.add(2);
		// Type mismatch compiler error
		// Compiler rejects unsafe code because at run-time, we cannot determine the true type of the generic
		//List<Number> numList = intList1; 
		
		// Compiler rejects the following code as it is unsafe
		// Negative impact on polymorphism
		System.out.println(UnsafeList.sum(intList1));
//		// Solution: Instead of using T, use wildcard ? extends T
//		
//		List<Integer> intList2 = new ArrayList<Integer>();
//		intList2.add(2);
//		intList2.add(3);
//		System.out.println(UnsafeList.sum(intList2));
		
//		//OR  Generics using lower bounded wildcard.
//		List<? super Integer> intList3 = new ArrayList<Integer>();
//		UnsafeList.addNumber(intList3, new Integer(3));
		
		
		
		
		
	}
}
