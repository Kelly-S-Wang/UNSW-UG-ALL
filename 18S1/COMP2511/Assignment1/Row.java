/**
 * The class Row holds its name, capacity, and the array that indicates every seat
 * seats[i] = the id of request or  0 if it's not been reserved.
 * @author z5119666
 * @invariant capacity > 0
 */
public class Row {
	
	private String row;
	private int[] seats;
	private int capacity;
	
	/**
	 * Constructor
	 * @param row
	 * @param seats
	 */
	public Row (String row, int seats) {
		this.row = row;
		this.seats = new int[seats];
		this.capacity = seats;
	}
	
	/**
	 * Returns row name
	 * @return row
	 */
	public String getCinemaRow () {
		return row;
	}
	
	/**
	 * Returns seats as an array
	 * @return seats number
	 */	
	public int[] getCinemaSeats() {
		return seats;
	}
	
	/**
	 * Returns the capacity of current row
	 * @return capacity
	 */
	public int getCapacity () {
		return capacity;
	}
}