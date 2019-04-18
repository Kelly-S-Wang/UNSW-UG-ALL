import java.util.ArrayList;
/**
 * Graph.java -- keeps the graph of all ports
 * Read all information through functions of Graph.java
 * @author z5119666
 *
 */
public class Graph {

	/**
	 * Constructors
	 */
	private ArrayList<Port> ports; // All ports
	private ArrayList<Shipment> shipments; // All shipments <From, To>
	
	public Graph() {
		this.ports = new ArrayList<Port>();
		this.shipments = new ArrayList<Shipment>();
	}
	
	/**
	 * Returns a list of ports info
	 * @return ports
	 */
	public ArrayList<Port> getPorts() {
		return ports;
	}
	
	/**
	 * Returns all shipments
	 * @return shipments
	 */
	public ArrayList<Shipment> getShipments() {
		return shipments;
	}
	
	/**
	 * Adds a new port to the graph
	 * @param name
	 * @param refuelDays
	 */
	public void addPort(String name, int refuelDays) {
		ports.add(new Port(name, refuelDays));
	}

	/**
	 * Add a new travel to the graph
	 * @pre days > 0
	 * @param portA
	 * @param portB
	 * @param days
	 */
	public void addTravel(Port portA, Port portB, int days) {
		portA.addTravel(portB, days);
		portB.addTravel(portA, days);
	}
	
	/**
	 * Add a new shipment
	 * @param from
	 * @param to
	 */
	public void addShipment(Port from, Port to) {
		shipments.add(new Shipment(from, to));
	}
}
