import java.time.LocalTime;

/**
 * The Timeline class holds unique sessions including cinema name and time.
 * @author z5119666
 * @invariant cinema > 0
 */
public class Timeline {
	
	private int cinema;
	private LocalTime time;
	
	/**
	 * Constructor
	 * @param cinema
	 * @param time
	 */
	public Timeline(int cinema, LocalTime time) {
		this.cinema = cinema;
		this.time = time;
	}
	
	/**
	 * Returns cinema name
	 * @return cinema
	 */
	public int getCinema () {
		return cinema;
	}
	
	/**
	 * Returns session time
	 * @return time
	 */
	public LocalTime getTime () {
		return time;
	}
}