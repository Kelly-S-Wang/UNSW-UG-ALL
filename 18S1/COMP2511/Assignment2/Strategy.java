import java.util.ArrayList;

public interface Strategy {
	public void findOptimal (ArrayList<Shipment> shipments, ArrayList<Port> ports);
}