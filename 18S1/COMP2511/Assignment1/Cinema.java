/**
 * Read Cinema name, row, and seats
 * @author z5119666
 * @invariant cinema > 0 and seats > 0
 */
public class Cinema extends Row {

	private int cinema;
	
	/**
	 * Constructor
	 * @param cinema
	 * @param row
	 * @param seats
	 */
	public Cinema (int cinema, String row, int seats) {
		super (row, seats);
		this.cinema = cinema;
	}
	
	/**
	 * Returns cinema name (positive number)
	 * @return cinema
	 */
	public int getCinema () {
		return cinema;
	}
}