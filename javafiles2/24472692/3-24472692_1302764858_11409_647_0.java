import java.math.BigInteger;
import java.util.Scanner;

public class Factorial2 {

   public static void main(String[] args) {
       Scanner s = new Scanner(System.in);
       System.out.print("Enter a number: ");
       int n = s.nextInt();
       for(int j = 0; j <= n;j++)
       {
           System.out.println("Factorial is " + factorial(j) + "\nLength -> " + fact.length() + " digits");
       }
       
   }

   public static String factorial(int n) {
       BigInteger fact = new BigInteger("1");
       for (int i = 1; i <= n; i++) {
           fact = fact.multiply(new BigInteger(i + ""));
       }
       return fact.toString();
   }
}