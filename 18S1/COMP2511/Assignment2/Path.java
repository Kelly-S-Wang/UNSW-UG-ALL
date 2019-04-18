import java.util.ArrayList;
/**
 * Path.java -- keeps f, g, h;
 * 			 -- keeps previous path
 * 			 -- keeps unfinished shipments
 * 			 -- modify new value
 * @author z5119666
 *
 */

public class Path implements Comparable<Path>{

	/**
	 * Constructors
	 */
	private int g;
	private int h;
	private int f;
	private Port curr;
	private Path prevPath;
	private ArrayList<Port> ports; // Keeps ports list, the path
	private ArrayList<Shipment> shipments; // Keeps unfinished shipments

	/**
	 * Read values according to previous path and current port
	 * @param prevPath
	 * @param curr
	 * @param all
	 */
	public Path (Path prevPath, Port curr, ArrayList<Shipment> all) {
		
		this.prevPath = prevPath;
		this.curr = curr;
		
		// If its the source
		if (prevPath == null) {
			this.shipments = all;
			this.ports = new ArrayList<Port>();
			ports.add(curr);
			int h = 0;
			for (Shipment s: all) {
				Port from = s.getFrom();
				Port to = s.getTo();
				h += from.getTravelDays(to);
			}
			updateState(0, h, h);
		} else {
			// Shipments remain
			this.shipments = updateShipment(prevPath.getShipments());
			// Path until now
			this.ports = updatePort(prevPath.getPorts());
			// Add new port to the path
			ports.add(curr);
			/**
			 * CurrPort from last Path - curr from this path
			 * form a new shipment
			 */
			Shipment currS = new Shipment(prevPath.getCurrPort(), curr);
			/**
			 * Check if this new shipment in the job list
			 * Using flag to check if remained jobs changed
			 */
			boolean flag = false;
			for (int i = 0; i < shipments.size(); i++) {
				Shipment s = shipments.get(i);
				Port from = s.getFrom();
				Port to = s.getTo();
				// If the new shipment in the job list, then remove this from it
				if (from.equals(currS.getFrom()) && to.equals(currS.getTo())) {
					shipments.remove(s);
					flag = true;
				}
			}
			
			// temp - hold new cost
			Port prev = prevPath.getCurrPort();
			int temp = prev.getTravelDays(curr);
			/**
			 * If removed a job this from shipment list
			 * then also remove the cost of this job in 'h'
			 */
			int h = prevPath.getH();
			int g = prevPath.getG() + temp;
			if (flag) h -= temp;
			updateState(g, h, g + h);
		}
	}
	
	/**
	 * 
	 * @param g
	 * @param h
	 * @param f
	 */
	public void updateState(int g, int h, int f) {
		this.g = g;
		this.h = h;
		this.f = f;
	}
	
	/**
	 * 
	 * @param prevShipments
	 * @return shipments list
	 */
	public ArrayList<Shipment> updateShipment(ArrayList<Shipment> prevShipments) {
		ArrayList<Shipment> s = new ArrayList<Shipment>(prevShipments);
		return s;
	}
	
	/**
	 * 
	 * @param prevPorts
	 * @return ports list
	 */
	public ArrayList<Port> updatePort(ArrayList<Port> prevPorts) {
		ArrayList<Port> p = new ArrayList<Port>(prevPorts);
		return p;
	}
	
	/**
	 * 
	 * @return g
	 */
	public int getG() {
		return g;
	}
	
	/**
	 * 
	 * @return f
	 */
	public int getF() {
		return f;
	}

	/**
	 * 
	 * @return h
	 */
	public int getH() {
		return h;
	}

	/**
	 * 
	 * @return shipments list
	 */
	public ArrayList<Shipment> getShipments() {
		return shipments;
	}
	
	/**
	 * 
	 * @return ports list
	 */
	public ArrayList<Port> getPorts() {
		return ports;
	}
	
	/**
	 * 
	 * @return current port
	 */
	public Port getCurrPort() {
		return curr;
	}
	
	/**
	 * 
	 * @return previous path
	 */
	public Path getPrevPath() {
		return prevPath;
	}

	@Override
	public int compareTo(Path o) {
		if (this.getF() < o.getF()) return -1;
		else if (this.getF() == o.getF()) return 0;
		else return 1;
	}
}
