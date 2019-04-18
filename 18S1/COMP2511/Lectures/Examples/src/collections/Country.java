/**
 *
 * @author Aarthi
 */
package collections;

import java.util.Comparator;
import java.util.TreeSet;

public class Country implements Comparable<Country> {
    
    public static Comparator<Country> populationComp = new Comparator<Country>() {

        @Override
        public int compare(Country country1, Country country2) {
            return (country1.population < country2.population) ? -1 : (country1.population > country2.population) ? 1 : 0;
        }
    };
    
    public String countryName;
    public int population;
    
    public Country( String name, int population) {
        this.countryName = name;
        this.population = population;
    }

   
    @Override
    public int compareTo(Country country) {
       return this.countryName.compareTo(country.countryName);
    }
    
    public static void main(String[] args)   {
        //Test 1
        TreeSet<Country> c = new TreeSet<>();
        
        Country c1 = new Country("India",1_000_000_000);
        Country c2 = new Country("Japan", 35_000_000);
        Country c3 = new Country("China",2_000_000_000);
        Country c4 = new Country("Australia",32_000_000);
        Country c5 = new Country("Amsterdam",36_000_000);
        
        c.add(c1);
        c.add(c2);
        c.add(c3);
        c.add(c4);
        c.add(c5);
        
        System.out.println("Size:" + c.size());
        for (Country element: c) {
            System.out.println(element.countryName);
        }
     
        // Sort countries with comparator
        c = new TreeSet<>(populationComp);
        
        c1 = new Country("India",1_000_000_000);
        c2 = new Country("Japan", 32_000_000);
        c3 = new Country("China",2_000_000_000);
        c4 = new Country("Australia",32_000_000);
        
        c.add(c1);
        c.add(c2);
        c.add(c3);
        c.add(c4);
        
        System.out.println("Size:" + c.size());
        for (Country element: c) {
            System.out.println(element.countryName);
        }
        
    }
    
    
}
