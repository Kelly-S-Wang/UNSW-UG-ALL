import java.time.LocalTime;
import java.util.ArrayList;

/**
 * Deal with "Request", "Change", "Cancel", and "Print"
 * by updating the seats situations according to movie's time and location
 * @author z5119666
 * @invariant cinema > 0
 */
public class Record extends Session {
	
	// Contains every row and their seats
	private ArrayList<Row> rowlist;
	
	/**
	 * Constructor
	 * @param cinema
	 * @param time
	 * @param rowList
	 */
	public Record (int cinema, LocalTime time, String movie, ArrayList<Row> rowList) {
		super (cinema, movie, time);
		this.rowlist = rowList;
	}

	/**
	 * Update record -- Either "Booking" or "Change (re-booking)"
	 * @param id
	 * @param tickets
	 * @pre tickets > 0
	 * Request is either "Booking" or "Change"
	 * @param request
	 */
	public String makeRequest (int id, int tickets, String request) {

		// Hold the 'start' seat number and the 'end' one. If tickets = 1, then start = end
		int start = 0, end = 0;
		// Hold the row name;
		String row = "";
		
		for (Row r: rowlist) {
			row = r.getCinemaRow();
			
			// If the tickets > # seats at current row, continue
			if (r.getCapacity() < tickets) continue;
			
			int[] seats = r.getCinemaSeats();
			int counter = 0; // Counting the continuous available seats
			
			int i = 0;
			for (; i < r.getCapacity(); i++) {
				// Check if found 'tickets' number of available seats
				if (counter == tickets) break;
				else {
					if (seats[i] == 0) counter ++; // If current seat is available, counting
					else if (seats[i] != 0) counter = 0; // Otherwise, reset the counter
				}
			}
			
			/**
			 * After checking all seats in current row, 
			 * if can't found 'tickets' number of available seats, then continue
			 */
			if (counter != tickets) continue;
			else {
				end = i;
				start = i - tickets + 1;
				for (; counter > 0; counter --, i--) {
					seats[i-1] = id; // Indicates these seats are occupied by request 'id'
				}
				break; // Break from rows
			}
		}
		
		// If no available seats for this request
		if (end == 0) {

			String[] result = {request, "rejected"};
			String rejected = String.join(" ", result);
			
			System.out.println(rejected);
			return rejected; // Returns "Booking rejected"
		} else {
			// If tickets > 1, print such as "Booking 1 A1-A4"
			if (tickets > 1) {
				
				String[] temp1 = {row, Integer.toString(start), "-", row, Integer.toString(end)};
				String temp2 = String.join("", temp1);
				
				String[] result = {request, Integer.toString(id), temp2};
				String allowed = String.join(" ", result);
				
				System.out.println(allowed);
				return temp2; // Returns seats string such as "A1-A4"
				
			} else { // If tickets = 1, print such as "Booking 1 A1"
				
				String[] temp1 = {row, Integer.toString(start)};
				String temp2 = String.join("", temp1);
				
				String[] result = {request, Integer.toString(id), temp2};
				String allowed = String.join(" ", result);
				
				System.out.println(allowed);
				return temp2; // Returns seats string such as "A1"
			}
		}
	}

	/**
	 * Update record -- Change: Check if the request can be changed
	 * @param id
	 * @param tickets
	 * @pre tickets > 0
	 * @return true or false
	 */
	public boolean makeChange (int id, int tickets) {
		
		for (Row r: rowlist) {
			
			// If the tickets > # seats at current row, continue
			if (r.getCapacity() < tickets) continue;
			
			int[] seats = r.getCinemaSeats();
			int counter = 0;
			
			int i = 0;
			for (; i < r.getCapacity(); i++) {
				// Check if found 'tickets' number of available seats
				if (counter == tickets) return true;
				if (seats[i] == 0 || seats[i] == id) counter ++; // If current seat is available, counting
				else counter = 0; // Otherwise, reset the counter
			}
		}
		return false;
	}

	/**
	 * Update record -- Either "Cancel" or "Change (cancel the original booking)"
	 * @param id
	 * @param request
	 */
	public void makeCancel (int id, String request) {
		
		for (Row r: rowlist) {
			
			int[] seats = r.getCinemaSeats();
			for (int i = 0; i < r.getCapacity(); i++) {
				// Find the seat that occupied by request = 'id', 'free' the seat by assigning to zero
				if (seats[i] == id) seats[i] = 0;
			}
		}
		if (request == "Cancel") System.out.println(request + " " + id);
	}
	
	/**
	 * Print the movie and seats situation for a certain session
	 */
	public void makePrint () {
		System.out.println(getMovie());
		for (Row r: rowlist) {
			int[] seats = r.getCinemaSeats();
			
			boolean first = true;
			int id = 0;
			int seatNum = 0;
			int counter = 0;
			
			int i = 0;
			for (i = 0; i < r.getCapacity(); i++) {

				if (first == true) {
					if (seats[i] != 0) {
						id = seats[i];
						counter++;
						seatNum = i+1;
						System.out.print(r.getCinemaRow() + ": " + seatNum);
						first = false;
					}
				} else {
					if (seats[i] != 0 && seats[i] == id) {
						//id id
						counter++;
						continue;
					} else if (seats[i] != 0 && seats[i] != id) {
						// id1 id2
						if (counter > 1)
							System.out.print("-" + i);
						id = seats[i];
						counter = 1;
						seatNum = i+1;
						System.out.print("," + seatNum);
					} else if (seats[i] == 0 && id == 0) {
						// 0 0
						continue;
					} else if (seats[i] == 0 && id != 0) {
						// id 0
						if (counter > 1)
							System.out.print("-" + i);
						counter = 0;
						id = 0;
					} else if (seats[i] != 0 && id == 0) {
						// 0 id
						id = seats[i];
						counter = 1;
						seatNum = i+1;
						System.out.print("," + seatNum);
					}
				}
			}
			if (counter > 1) System.out.print("-" + i);
			if (first == false) System.out.println();
		}
	}
}