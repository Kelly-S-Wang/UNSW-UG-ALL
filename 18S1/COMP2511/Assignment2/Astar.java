import java.util.ArrayList;
import java.util.PriorityQueue;
/**
 * Astar.java -- Astar search and print the result
 * @author z5119666
 *
 */

public class Astar implements Strategy{
	
	/**
	 * Constructors
	 */
	private int expanded;
	private int cost;
	private ArrayList<Port> soln; // Keeps the final solution
	private PriorityQueue<Path> open;
	
	public Astar () {
		this.open = new PriorityQueue<Path>();
		this.soln = new ArrayList<Port>();
		this.expanded = 0;
		this.cost = 0;
	}
	
	@Override
	public void findOptimal(ArrayList<Shipment> shipments, ArrayList<Port> ports) {
		
		// All start from Sydney
		for (Port p: ports)
			if (p.getPortName().equals("Sydney"))
				open.add(new Path(null, p, shipments));

		while (!open.isEmpty()) {
			Path curr = open.poll();
			expanded++;
			
			// If no job remains, the end
			if (curr.getShipments().size() == 0) {
				cost = curr.getF();
				soln = curr.getPorts();
				break;
			}

			Port currP = curr.getCurrPort();
			ArrayList<Port> ps = currP.getConnected();
			for (int i = 0; i < ps.size(); i++) 
				open.add(new Path(curr, ps.get(i), shipments));
		}
	}

	public void printMethod() {
		System.out.println(expanded + " nodes expanded");
		System.out.println("cost = " + cost);
		for (int i = 0; i < soln.size() - 1; i++) {
			String from = soln.get(i).getPortName();
			String to = soln.get(i+1).getPortName();
			System.out.println("Ship " + from + " to " + to);
		}
	}
}
