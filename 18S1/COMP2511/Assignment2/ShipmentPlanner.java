import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Find the optimal solution of the shipments
 * @author z5119666
 *
 */
public class ShipmentPlanner {

	// Make a graph contains all ports (vertice) and travels (edges)
	static private Graph graph = new Graph ();
    static private Astar astar = new Astar ();
    
	public static void main(String[] args) {
		
		Scanner sc = null;
		try {
			// Read file passed from arguments
		    sc = new Scanner (new File(args[0]));
		    while (sc.hasNextLine()) {
		    	
		    		String str = sc.nextLine();
		    		// Get rid of comments and unnecessary tabs, spaces ...
		    		str = str.replaceAll("#.*$", "")
		    				.replaceAll("[ \\t\\r\\n]*$", "")
		    				.replaceAll("^[ \t\r\n]*$", "")
		    				.replaceAll("\n", "");
		    		
		    		// If the line is empty, do nothing
		    		if (str.isEmpty()) continue;
		    		// Make a string to String[]
	    	        Pattern p = Pattern.compile("[a-zA-Z0-9]+");
	    	        Matcher m = p.matcher(str);
	    	        
	    	        int size = 0;
	    	        while (m.find()) size++;
	    	        String[] line = new String[size];
	    	        
	    	        m.reset();
	    	        for (int i = 0; m.find(); i++) line[i] = m.group();
	    	        
	    	        // Start dealing with different instruction according to the first word
	    	        if (line[0].equals("Refuelling")) {
	    	        		refuellingMethod(line);
	    	        } else if (line[0].equals("Time")) {
	    	        		travelMethod(line);
	    	        } else if (line[0].equals("Shipment")) {
	    	        		shipmentMethod(line);
	    	        }
		    }
		} catch (FileNotFoundException e) {
		    System.out.println(e.getMessage());
		} finally {
			if (sc != null) sc.close();
		}		
	    astar.findOptimal(graph.getShipments(), graph.getPorts());
	    astar.printMethod();
	}
	
	/**
	 * Adds port info
	 * @param line
	 */
	private static void refuellingMethod (String[] line) {
		graph.addPort(line[2], Integer.parseInt(line[1]));
	}
	
	/**
	 * Adds travel info
	 * @param line
	 */
	private static void travelMethod (String[] line) {
		Port portA = null;
		Port portB = null;
		for (Port p: graph.getPorts()) {
			if (p.getPortName().equals(line[2])) portA = p;
			if (p.getPortName().equals(line[3])) portB = p;
		}
		graph.addTravel(portA, portB, Integer.parseInt(line[1]));
	}
	
	/**
	 * Adds shipment info
	 * @param line
	 */
	private static void shipmentMethod (String[] line) {
		for (Port p: graph.getPorts()) {
			String name = p.getPortName();
			if (name.equals(line[1])) {
				for(Port p2: p.getConnected()) {
					if (p2.getPortName().equals(line[2]))
						graph.addShipment(p, p2);
				}
			}
		}
	}
}