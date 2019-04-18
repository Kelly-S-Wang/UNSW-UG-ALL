import java.util.ArrayList;;
/**
 * Port.java -- stores the name, refuel days, and all connections of the port
 * @author z5119666
 *
 */
public class Port {

	/**
	 * Constructors
	 */
	private String portName;
	private int refuelDays;
	private ArrayList<Travel> travels; // Stores all the connected path

	/**
	 * 
	 * @param portName
	 * @param refuelDays
	 */
	public Port(String portName, int refuelDays) {
		this.portName = portName;
		this.refuelDays = refuelDays;
		this.travels = new ArrayList<Travel>();
	}

	/**
	 * Returns travel + refuel time
	 * @param p
	 * @return travel + refuel time
	 */
	public int getTravelDays(Port p) {
		for (Travel t: travels) {
			if (p.equals(t.getPort()))
				return t.getDays() + refuelDays;
		}
		return 0;
	}
	
	/**
	 * Adds connected ports info
	 * @param port
	 * @param days
	 */
	public void addTravel(Port port, int days) {
		travels.add(new Travel(port, days));
	}
	
	/**
	 * Returns the name of port
	 * @return portName
	 */
	public String getPortName() {
		return portName;
	}

	/**
	 * Returns the refuel days of the port
	 * @return refuelDays
	 */
	public int getRefuelDays() {
		return refuelDays;
	}
	
	/**
	 * Gets the list of connected ports to this port
	 * @return list of ports
	 */
	public ArrayList<Port> getConnected() {
		ArrayList<Port> ports = new ArrayList<Port> ();
		for (Travel t: travels) {
			ports.add(t.getPort());
		}
		return ports;
	}
}
