/**
 * Shipment.java -- keeps all jobs, consider ports pair as a vertex in the graph
 * to assist A* search
 * @author z5119666
 * 
 */
public class Shipment {
	
	/**
	 * Constructors
	 */
	private Port from;
	private Port to;
	
	/**
	 * Consider each shipment as a vertex in the shipments graph
	 * and then use A* search
	 * @param from
	 * @param to
	 */
	public Shipment(Port from, Port to) {
		this.from = from;
		this.to = to;
	}

	/**
	 * Returns the source port of the shipment
	 * @return from
	 */
	public Port getFrom() {
		return from;
	}
	
	/**
	 * Returns the destination port of the shipment
	 * @return to
	 */
	public Port getTo() {
		return to;
	}
}
