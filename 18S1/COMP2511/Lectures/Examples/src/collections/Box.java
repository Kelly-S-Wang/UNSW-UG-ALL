/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package collections;

import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author Aarthi
 */
public class Box<T> {
    
    private List<T> list = new ArrayList<T>();
    
    public void add(T element){
        list.add(element);
    }
    
    public T get(int i) {
        return list.get(i);
    }
    
    public static void main(String[] args) {
     Box<Integer> integerBox = new Box<>();
     integerBox.add(0);
     integerBox.add(1);
     
     
     System.out.println(integerBox.get(0));
     System.out.println(integerBox.get(1));
     
    } 
    
}
