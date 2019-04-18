/**
 * @author z5119666
 * Travel.java -- is used to keep the destination port of a travel and the days needed
 * 
 */
public class Travel {

	/**
	 * Constructors
	 */
	private Port port;
	private int days;
	
	/**
	 * 
	 * @param port -- destination
	 * @param days -- time that used
	 */
	public Travel(Port port, int days) {
		this.port = port;
		this.days = days;
	}
	
	/**
	 * Returns destination port of the travel
	 * @return port
	 */
	public Port getPort() {
		return port;
	}
	
	/**
	 * Returns travel days to the destination
	 * @pre days > 0
	 * @return days
	 */
	public int getDays() {
		return days;
	}
}
