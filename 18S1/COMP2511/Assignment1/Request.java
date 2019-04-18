import java.time.LocalTime;

/**
 * Store each request including request id, # of tickets and their seat(s) number
 * @author z5119666
 * @invariant id > 0 and tickets >= 1
 */
public class Request extends Timeline {

	private int id;
	private int tickets;
	private String seats;
	
	/**
	 * Constructor
	 * @param id
	 * @param cinema
	 * @param tickets
	 * @param time
	 * @param seats
	 */
	public Request (int id, int cinema, int tickets, LocalTime time, String seats) {
		super (cinema, time);
		this.id = id;
		this.tickets = tickets;
		this.seats = seats;
	}
	
	/**
	 * Returns request ID
	 * @return id
	 */
	public int getId () {
		return id;
	}
	
	/**
	 * Returns the number of tickets
	 * @return tickets
	 */
	public int getTickets () {
		return tickets;
	}
	
	/**
	 * Return their seats such as "A11-A15" or "B4"
	 * @return seats
	 */
	public String getSeats () {
		return seats;
	}
}