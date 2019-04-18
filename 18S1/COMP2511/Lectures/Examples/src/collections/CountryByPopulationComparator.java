/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package collections;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.Iterator;
import java.util.List;
import java.util.TreeSet;

/**
 *
 * @author Aarthi
 */
public class CountryByPopulationComparator implements Comparator<Country>{
    @Override
    public int compare(Country country1, Country country2) {
        return (country1.population < country2.population) ? -1 : (country1.population > country2.population) ? 1 : 0;
    }
    
    public static void main(String[] args) {
        
//        // TreeSet with comparable
//        TreeSet<Country> c = new TreeSet<>(new CountryByPopulationComparator());
//        
//        
        Country c1 = new Country("India",1_000_000_000);
        Country c2 = new Country("Japan", 35_000_000);
        Country c3 = new Country("China",2_000_000_000);
        Country c4 = new Country("Australia",32_000_000);
//        
//        c.add(c1);
//        c.add(c2);
//        c.add(c3);
//        c.add(c4);
//        
//        System.out.println("Size:" + c.size());
//        for (Country element: c) {
//            System.out.println(element.countryName);
//        }
        
        List<Country> cos = new ArrayList<>();
        cos.add(c1);
        cos.add(c2);
        cos.add(c3);
        cos.add(c4);

        for (int i=0; i< cos.size(); i++ ){
      	  Country c = cos.get(i);
      	  System.out.println(c.countryName);
      }

//        for (Country element: cos) {
//            Country c = element;
//            if (c.countryName.equals("Japan")) {
//            	cos.remove(c);
//            }
//        	System.out.println(element.countryName);
//        }

        for (int i=0; i< cos.size(); i++ ){
        	  Country c = cos.get(i);
        	  if (c.countryName.equals("India")) {
              	cos.remove(i);
              }
        }
//        Iterator<Country> it = cos.iterator();
//        while (it.hasNext()) {
//        	Country c = it.next();
//        	if (c.countryName.equals("Japan")) {
//            	it.remove();
//            }
//        }
        System.out.println("Printing list after removal");
        for (Country element: cos) {
            System.out.println(element.countryName);
        }
        
        
        
        
        
    }
}

