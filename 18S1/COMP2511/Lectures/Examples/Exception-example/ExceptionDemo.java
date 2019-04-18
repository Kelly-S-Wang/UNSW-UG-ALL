import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;

public class ExceptionDemo {

	
	public void doSomethig(File file) throws FileNotFoundException{
		FileReader fr = new FileReader(file);
	}
	
	
	public static void main(String[] args)  {
		
		File file = new File("E://file.txt");
		ExceptionDemo ex = new ExceptionDemo();
		
		try {
			ex.doSomethig(file);
		}
	    catch (FileNotFoundException fe){
	    	System.out.println("File not found");
	    }
	}
}
