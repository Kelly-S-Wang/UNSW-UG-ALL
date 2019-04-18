import java.io.File;
import java.util.Scanner;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.time.LocalTime;

/**
 * Cinema Booking System
 * @author z5119666
 */
public class CinemaBookingSystem {
	
	// Store all cinemas rows' name and capacity
	static private ArrayList<Cinema> cinemas = new ArrayList<Cinema> ();
	// Store all sessions with their cinema and time
	static private ArrayList<Session> sessions = new ArrayList<Session> ();
	// Keep updating the seats situation for each session
	static private ArrayList<Record> records = new ArrayList<Record> ();
	// Keep a record of requests
	static private ArrayList<Request> requests = new ArrayList<Request> ();
	
	public static void main(String[] args) {
		
		Scanner sc = null;
		try
		{
			// Read file passed from arguments
		    sc = new Scanner (new File(args[0]));
		    while (sc.hasNextLine()) {
		    	
		    		String str = sc.nextLine();
		    		// Get rid of comments and unnecessary tabs, spaces ...
		    		str = str.replaceAll("#.*$", "")
		    				.replaceAll("[ \\t\\r\\n]*$", "")
		    				.replaceAll("^[ \t\r\n]*$", "")
		    				.replaceAll("\n", "")
		    				.replaceAll(":", " ");
		    		
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
	    	        if (line[0].equals("Cinema")) {
	    	        		cinemaMethod (line);
	    	        } else if (line[0].equals("Session")) {
	    	        		sessionMethod (line, size);
	    	        } else if (line[0].equals("Request")) {
	    	        		requestMethod (line);
	    	        } else if (line[0].equals("Change")) {
	    	        		changeMethod (line);
	    	        } else if (line[0].equals("Cancel")) {
	    	        		cancelMethod (line);
	    	        } else if (line[0].equals("Print")) {
	    	        		printMethod (line);
	    	        }
		    }
		}
		catch (FileNotFoundException e)
		{
		    System.out.println(e.getMessage());
		}
		finally 
		{
			if (sc != null) sc.close();
		}
	}
	
	private static void cinemaMethod (String[] line) {
		int cinemaName = Integer.parseInt(line[1]);
		String row = line[2];
		int seats = Integer.parseInt(line[3]);
		
		Cinema cinema = new Cinema (cinemaName, row, seats);
		cinemas.add(cinema);
	}
	
	private static void sessionMethod (String[] line, int size) {
		// Deal with the movie that has more than one word
		String[] temp = new String[size-4];
		for (int i = 4; i < size; i++) temp[i-4] = line[i];
		String movie = String.join(" ", temp); 
		
		LocalTime time = LocalTime.of(Integer.parseInt(line[2]), Integer.parseInt(line[3]));
		int cinemaName = Integer.parseInt(line[1]);
		
		Session session = new Session (cinemaName, movie, time);
		sessions.add(session);
		
		// Find all rows in each cinema
		ArrayList<Row> rowlist = new ArrayList<Row> ();
		for (Cinema c: cinemas) {
			if (cinemaName == c.getCinema()) {
				Row row = new Row(c.getCinemaRow(), c.getCapacity());
				rowlist.add(row);
			}
		}
		
		// Initialise record with the combination of sessions and cinema capacity
		Record record = new Record (cinemaName, time, movie, rowlist);
		records.add(record);
	}
	
	private static void requestMethod (String[] line) {
		int id = Integer.parseInt(line[1]);
		int cinemaName = Integer.parseInt(line[2]);
		int tickets = Integer.parseInt(line[5]);
		LocalTime time = LocalTime.of(Integer.parseInt(line[3]), Integer.parseInt(line[4]));
		String timeStr = time.toString();
		
		// Find the record of the request session
		for (Record r: records) {
			
			LocalTime rTime = r.getTime();
			String rTimeStr = rTime.toString();
			
			if (r.getCinema() == cinemaName && rTimeStr.equals(timeStr)) {
				
				String seats = null;
				
				// Booking ...
		seats = r.makeRequest (id, tickets, "Booking");
		// If there are the 'tickets' number of seats available, booking succeed!
				if (!seats.equals("Booking rejected")) {
					
					Request request = new Request (id, cinemaName, tickets, time, seats);
					requests.add(request); // Keep a record of valid booking
				}
				// Else do nothing, since Record.java will print the reject message
				break;
			}
		}
	}
	
	private static void changeMethod (String[] line) {
		int id = Integer.parseInt(line[1]);
		int cinemaName = Integer.parseInt(line[2]);
		int tickets = Integer.parseInt(line[5]);
    		LocalTime time = LocalTime.of(Integer.parseInt(line[3]), Integer.parseInt(line[4]));
    		String timeStr = time.toString();
    		
			boolean validId = false;
			for (Request rq: requests) {
				
				if (rq.getId() == id) { // If there exist such a booking
					
					validId = true;
    	        		boolean canChange = true;

        				for (Record r: records) {
        					
        					LocalTime rTime = r.getTime();
    	        			String rTimeStr = rTime.toString();
    	        			
    	        			if (r.getCinema() == cinemaName && rTimeStr.equals(timeStr)) {
    	        				
    	        				// Check if there are available seats for the new request
    	        				canChange = r.makeChange(id, tickets);
    	        				
    	        				// If no enough seats available, print the message and keep the original booking
    	        				if (canChange == false) {
    	        					System.out.println("Change rejected");
    	        				}
    	        				break;
    	        			}
        				}
        				
        				/**
        				 * If the booking can be changed
        				 * 1) Cancel the old booking
        				 * 2) Make a new request
        				 */
        				if (canChange == true) {
        					
        					// 1) Cancel the old booking, and remove from requests list
        					for (Record r: records) {
        						
        						String rTimeStr = r.getTime().toString();
        						String rqTimeStr = rq.getTime().toString();
        						
        						if (r.getCinema() == rq.getCinema() && rTimeStr.equals(rqTimeStr)) {
        							
        							r.makeCancel(id, "Change");
        							requests.remove(rq);
        							break;
        						}
        					}
        					
        					// 2) Make a new request using the old id, and add to requests list
	        				for (Record r: records) {
	        					
	        					LocalTime rTime = r.getTime();
	    	        			String rTimeStr = rTime.toString();
	    	        			
	    	        			if (r.getCinema() == cinemaName && rTimeStr.equals(timeStr)) {
	    	        				
	    	        				String seats = null;
						seats = r.makeRequest (id, tickets, "Change");
	    	        				Request request = new Request (id, cinemaName, tickets, time, seats);
	    	        				requests.add(request);
	    	        				break;
	    	        			}
	        				}
        				}
        				break;
				}
			}
			
			// If there is no such a booking
			if (validId == false) System.out.println("Change rejected");			
	}
	
	private static void cancelMethod (String[] line) {
		int id = Integer.parseInt(line[1]);
		boolean validId = false;
		
		for (Request rq: requests) {
			
			if (rq.getId() == id) { // If there exist such a booking
				
				validId = true;
				
				// Cancel the booking, and remove from the requests list
				for (Record r: records) {
					
					String rTimeStr = r.getTime().toString();
					String rqTimeStr = rq.getTime().toString();
					
					if (r.getCinema() == rq.getCinema() && rTimeStr.equals(rqTimeStr)) {
						
						r.makeCancel(id, "Cancel");
						requests.remove(rq);
						break;
					}
				}
				break;
			}
		}
		
		// If there is no such a booking
		if (validId == false) System.out.println("Cancel rejected");
	}
	
	private static void printMethod (String[] line) {
		int cinemaName = Integer.parseInt(line[1]);
		LocalTime time = LocalTime.of(Integer.parseInt(line[2]), Integer.parseInt(line[3]));
		String timeStr = time.toString();
		
		for (Record r: records) {
			
			LocalTime rTime = r.getTime();
			String rTimeStr = rTime.toString();
			
			if (r.getCinema() == cinemaName && rTimeStr.equals(timeStr)) {
				r.makePrint();
			}
		}
	}
}