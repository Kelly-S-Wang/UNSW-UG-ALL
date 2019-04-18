package relationships;

public class Engine {
	
	private int engineSize;
	private int numOfCylinders;
	
	public Engine(int engineSize2, int numCylinders) {
		this.setEngineSize(engineSize2);
		this.setNumOfCylinders(numCylinders);
	}

	public int getNumOfCylinders() {
		return numOfCylinders;
	}

	public void setNumOfCylinders(int numOfCylinders) {
		this.numOfCylinders = numOfCylinders;
	}

	public int getEngineSize() {
		return engineSize;
	}

	public void setEngineSize(int engineSize) {
		this.engineSize = engineSize;
	}
}

