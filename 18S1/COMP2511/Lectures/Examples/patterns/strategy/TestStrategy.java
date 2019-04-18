package patterns.strategy;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Iterator;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;

public class TestStrategy {
    public static void main(String[] args)   {
      //Test 1

      Country c1 = new Country("India",1_000_000_000);
      Country c2 = new Country("Japan", 35_000_000);
      Country c3 = new Country("China",2_000_000_000);
      Country c4 = new Country("Australia",32_000_000);
      Country c5 = new Country("Amsterdam",36_000_000);

      List<Country> countries = new ArrayList<>();
      countries.add(c1);
      countries.add(c2);
      countries.add(c3);
      countries.add(c4);
      countries.add(c5);
      
      // Using an iterator to access the list elements
      System.out.println("Printing list of countries");
      Iterator<Country> it = countries.iterator();
      while (it.hasNext()) {
      	Country c = it.next();
      	System.out.println(c.countryName + ":" + c.population);
      }	
      
      // Test 2
      // calling sort on the list of countries
      // this sort will sort the countries in the "natural sort order" specified by the compareTo method implemented
      // in the class Country i.e. sort by country name
      System.out.println("Printing list of countries sorted in natural order");
      Collections.sort(countries);
      for (Country c: countries) {
    	  System.out.println(c.countryName + ":" + c.population);
      }
      
      //Test 3
      // Sorting a list of countries by using a different comparator CountryByPopulationCompartor
      countries.sort(new CountryByPopulationComparator());
      System.out.println("Printing list of countries sorted by population");
      for (Country c: countries) {
    	  System.out.println(c.countryName + ":" + c.population);
      }
      
      //Test 4
      // Create a TreeSet of countries
      // TreeSet is a data-structure that maintains the elements added in a sorted order.
      // TreeSet uses the "natural sort-order" provided by the compareTo method implemented in Country as 
      // the elements are added to the set
      
      Set<Country> countrySetNaturalOrder = new TreeSet<>();
      countrySetNaturalOrder.add(c1);
      countrySetNaturalOrder.add(c2);
      countrySetNaturalOrder.add(c3);
      countrySetNaturalOrder.add(c4);
      countrySetNaturalOrder.add(c5);
      System.out.println("Printing SET of countries sorted in natural order");
      for (Country c: countrySetNaturalOrder) {
    	  System.out.println(c.countryName);
      }
      
      //Test 5
      // Create a tree-set using a comparator
      // This time, as elements are added to the set, the elements are not ordered by their "natural sort order"
      // but ordered as specified in the comparator CountryByPopulationComparator
      
      // Sort countries with comparator
      Comparator<Country> populationComp = new CountryByPopulationComparator();
      Set<Country> countrySetPopulationOrder = new TreeSet<>(populationComp);
      
      countrySetPopulationOrder.add(c1);
      countrySetPopulationOrder.add(c2);
      countrySetPopulationOrder.add(c3);
      countrySetPopulationOrder.add(c4);
      countrySetPopulationOrder.add(c5);

      System.out.println("Printing SET of countries sorted by population as specified by comparator");
      for (Country c: countrySetPopulationOrder) {
    	  System.out.println(c.countryName + ":" + c.population);
      }
    }
}
