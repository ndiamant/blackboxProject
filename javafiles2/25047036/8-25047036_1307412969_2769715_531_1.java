import java.util.Scanner;
public class getfactorial{
    public static void main( String [] args){
        int a;
        a = getfactorial();
        System.out.println("the factorial is " + a);
    }
    
    public static int getfactorial(){
        Scanner input = new Scanner (System.in);
        System.out.println("Enter the number of which the factorial is to be calculated: \t");
        int a = input.nextInt();
        int a1 = 1;
        for (int i=1; i<=a; i++){
            a1 *=i;
        }
        return a1;
    }
}