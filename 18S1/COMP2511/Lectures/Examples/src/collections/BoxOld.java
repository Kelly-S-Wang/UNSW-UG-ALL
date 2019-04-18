package collections;

public class BoxOld {
	
	private Object t;
	public Object get() {
		return t;
	}

	public void set(Object t) {
		this.t = t;
	}

        public static void main(String args[]){
		BoxOld type = new BoxOld();
		type.set("apple");
		String s = (String) type.get(); //type casting, - ClassCastException (return type is Object)
		
	}

}
