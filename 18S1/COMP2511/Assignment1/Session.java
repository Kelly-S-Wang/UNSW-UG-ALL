import java.time.LocalTime;

/**
 * Read sessions including location (cinema), time and movie
 * @author z5119666
 * @invariant cinema > 0
 */
public class Session extends Timeline {
	
	private String movie;
	
	/**
	 * Constructor
	 * @param cinema
	 * @param movie
	 * @param time
	 */
	public Session (int cinema, String movie, LocalTime time) {
		super (cinema, time);
		this.movie = movie;
	}
	
	/**
	 * Returns movie's name
	 * @return movie
	 */
	public String getMovie () {
		return movie;
	}
}