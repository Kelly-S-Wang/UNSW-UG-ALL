/**
 *
 * @author Aarthi
 */
package patterns.strategy;

/**
 * This class implements the interface Comparable and overrides the method compareTo
 * The implementation of compareTo provides a natural sort order for the class
 * so if a collection of countries is sorted using the method Collections.sort() OR if countries
 * are added to a TreeSet (a data-structure that maintains elements in a sorted order), then this natural sort
 * order specified by the comapreTo method is used.
 * 
 * Additionally, the class also implements an anonymous inner class, which enables countries to be sorted
 * by population.
 */
public class Country implements Comparable<Country> { 

//    public static Comparator<Country> populationComp = new Comparator<Country>() {
//
//        @Override
//        public int compare(Country country1, Country country2) {
//            return (country1.population < country2.population) ? -1 : (country1.population > country2.population) ? 1 : 0;
//        }
//    };
    
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
    
}
    
    

