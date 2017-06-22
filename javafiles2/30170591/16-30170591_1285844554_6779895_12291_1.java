/**
 * ##### # ########### ## ##### ##### ####.
 * 
 * @###### ####### ######### 
 * @####### (# ####### ###### ## # ####)
 */
public class CodingBat
{
    public static void main(String [] args)
    {System.out.print("\f");
        //************* Prob 1 ***********************
        // Write the method sleepIn below main.
        //  test by running this segment        
        System.out.println("sleepIn(false, false) =" +sleepIn(false,false) + " should be true");
        System.out.println("sleepIn(true, false) =" +sleepIn(true,false) + " should be false");
        System.out.println("sleepIn(false, true) =" +sleepIn(false,true) + " should be true");
        System.out.println("sleepIn(true, true) =" +sleepIn(true,true) + " should be true");
               
        //************** End Prob 1 ******************/
        /************* Prob 2 ***********************
        // We have two monkeys, a and b. We are in trouble if they 
        //   are both smiling or if neither of them is smiling. 
        //  Write the method monkeyTrouble below main. The first 
        //  parameter, aSmile, is true if monkey a is smiling.
        //  The method should return true if we are in trouble.  
        
        //  test by running this segment        
        System.out.println("monkeyTrouble(false, false) =" +monkeyTrouble(false,false) + " should be true");
        System.out.println("monkeyTrouble(true, false) =" +monkeyTrouble(true,false) + " should be false");
        System.out.println("monkeyTrouble(false, true) =" +monkeyTrouble(false,true) + " should be false");
        System.out.println("monkeyTrouble(true, true) =" +monkeyTrouble(true,true) + " should be true");
        
       
        //************** End Prob 2 ******************/
        /************* Prob 3 ***********************
        // Write a method where indicated below main named sumDouble. 
        // Given two int values, it returns their sum. 
        // Unless the two values are the same, 
        //   then return double their sum. Test your method below.
        System.out.println("sumDouble(1,2) =" + sumDouble(1,2) + " should be 3");
        System.out.println("sumDouble(3,2) =" + sumDouble(3,2) + " should be 5");
        System.out.println("sumDouble(2,2) =" + sumDouble(2,2) + " should be 8");
        System.out.println("sumDouble(3,3) =" + sumDouble(3,3) + " should be 12");
        
        
        //************** End Prob 3 ******************/
        /************* Prob 4 ***********************
        // Write a method where indicated below main named cigarParty. 
        // Test your method by running the statements below.
        System.out.println("cigarParty(30, false) =" + cigarParty(30, false) + " should be false");
        System.out.println("cigarParty(50, false) =" + cigarParty(50, false) + " should be true");
        System.out.println("cigarParty(70, true) =" + cigarParty(70, true) + " should be true");
        System.out.println("cigarParty(80, false) =" + cigarParty(80, false) + " should be false");
        
        
        //************** End Prob 4 ******************/    
        /************* Prob 5 ***********************
        // Write a method below main named caughtSpeeding. 
        // Test your method here.
        System.out.println("caughtSpeeding(60,false) =" + caughtSpeeding(60,false) + " should be 0");
        System.out.println("caughtSpeeding(65,false) =" + caughtSpeeding(65,false) + " should be 1");
        System.out.println("caughtSpeeding(65,true) =" + caughtSpeeding(65,true) + " should be 0");
        System.out.println("caughtSpeeding(85,true) =" + caughtSpeeding(85,true) + " should be 1");
        System.out.println("caughtSpeeding(81,false) =" + caughtSpeeding(81,false) + " should be 2");
        
        
        //************** End Prob 5 ******************/    
        /************* Prob 6 ***********************
        // Write a method below main named teenSum. 
        // Given two int values, it returns their sum. 
        // However, "teen" values in the range 13..19 inclusive, 
        // are extra lucky. So if either value is a teen, 
        // just return 19.  Test your method below.
        
        System.out.println("teenSum(3,4) =" + teenSum(3,4) + " should be 7");
        System.out.println("teenSum(10,13) =" + teenSum(10,13) + " should be 19");
        System.out.println("teenSum(13,2) =" + teenSum(13,2) + " should be 19");
        System.out.println("teenSum(6,7) =" + teenSum(6,7) + " should be 13");
        System.out.println("teenSum(2,20) =" + teenSum(2,20) + " should be 22");
        
        
        //************** End Prob 6 ******************/    
        /************* Prob 7 ***********************
        // Write a method below main named factorial. 
        // Use recursion. See hint on CodingBat for this problem
        // Test your method below.
        System.out.println("factorial(1) =" + factorial(1) + " should be 1");
        System.out.println("factorial(2) =" + factorial(2) + " should be 2");
        System.out.println("factorial(4) =" + factorial(4) + " should be 24");
        System.out.println("factorial(10) =" + factorial(10) + " should be 3628800");
        
        
        //************** End Prob 7 ******************/    
        /************* Prob 8 ***********************
        // Write a method below named sumDigits. 
        System.out.println("sumDigits(126) =" + sumDigits(126) + " should be 9");        System.out.println("sumDigits(49) =" + sumDigits(49) + " should be 13");
        System.out.println("sumDigits(12) =" + sumDigits(12) + " should be 3");
        System.out.println("sumDigits(126) =" + sumDigits(126) + " should be 9");
        System.out.println("sumDigits(0) =" + sumDigits(0) + " should be 0");
        System.out.println("sumDigits(11111) =" + sumDigits(11111) + " should be 5");
        
        
        //************** End Prob 8 ******************/    
        /************* Prob 9 ***********************
        // Write a method below named blackjack. 
        System.out.println("blackjack(19,21) =" + blackjack(19,21) + " should be 21");
        System.out.println("blackjack(21,19) =" + blackjack(21,19) + " should be 21");
        System.out.println("blackjack(19,21) =" + blackjack(19,21) + " should be 21");
        System.out.println("blackjack(19,22) =" + blackjack(19,22) + " should be 19");
        System.out.println("blackjack(19,21) =" + blackjack(19,21) + " should be 21");
        System.out.println("blackjack(22,22) =" + blackjack(22,22) + " should be 0");
        System.out.println("blackjack(22,50) =" + blackjack(22,50) + " should be 0");
        System.out.println("blackjack(9,6) =" + blackjack(9,6) + " should be 9");
       
        
        //************** End Prob 9 ******************/    
    
    }
    
 /* 1) sleepIn
  *    The parameter weekday is true if it is a weekday, 
  *    and the parameter vacation is true if we are on vacation. 
  *    We sleep in if it is not a weekday or we're on vacation. 
  *    Return true if we sleep in. 
  */
    public static boolean sleepIn(boolean weekday, boolean vacation) 
    {
        if(!weekday || vacation)
            return true;
        //else
            return false; 
    }      
    
   /* 2) monkeyTrouble 
    *    We have two monkeys, a and b, and the parameters 
    *    aSmile and bSmile indicate if each is smiling. 
    *    We are in trouble if they are both smiling 
    *    or if neither of them is smiling. 
    *    Return true if we are in trouble. 
    */
    public static boolean monkeyTrouble(boolean aSmile, boolean bSmile) 
    {    
         if((aSmile && bSmile) || (!aSmile && !bSmile))
            return true;
         else
            return false;  
    }   
    
    /* 3) sumDouble 
     *    Given two int values, return their sum. 
     *    Unless the two values are the same, 
     *    then return double their sum.
     *    
     *    write your sumDouble method here:
     */
        public static int sumDouble(int a, int b)
        {
            if(a != b)
            {
                return a + b;
            }
            else return 2 * (a + b);
        }
    
    /* 4) cigarParty
     *    When squirrels get together for a party, they like
     *    to have cigars. A squirrel party is successful when
     *    the number of cigars is between 40 and 60, inclusive.
     *    Unless it is the weekend, in which case there is no
     *    upper bound on the number of cigars. 
     *    Return true if the party with the given values is 
     *    successful, or false otherwise. See assignment handout 
     *    for hints.
     *    write your cigarParty method here:  
     */
    public static boolean cigarParty(int cigars, boolean isWeekend) 
    {
        if((cigars >= 40 && cigars <= 60) || isWeekend)
            return true;
        else 
            return false; // fix this        
    }    
    
  /* 5) caughtSpeeding 
   * You are driving a little too fast, and a police officer 
   * stops you. Write code to compute the result, encoded as 
   * an int value: 0=no ticket, 1=small ticket, 2=big ticket. 
   * If speed is 60 or less, the result is 0. 
   * If speed is between 61 and 80 inclusive, the result is 1. 
   * If speed is 81 or more, the result is 2. 
   * Unless it is your birthday -- on that day, your speed can
   * be 5 higher in all cases. 
   * 
   * write your caughtSpeeding method here
   */
    public static int caughtSpeeding(int speed, boolean isBirthday) {
        if(!isBirthday)
        {
            if(speed <= 60)
            {
                return 0;
            }
            else if(speed <= 80)
            {
                return 1;
            }
            else
                return 2;
            
        }
        else
        {
            speed = speed - 5;
            if(speed <= 60)
            {
                return 0;
            }
            else if(speed <= 80)
            {
                return 1;
            }
            else
                return 2;
        }
        
    }
    
  /* 6) teenSum
   * Given 2 ints, a and b, return their sum. 
   * However, "teen" values in the range 13..19 inclusive,
   * are extra lucky. So if either value is a teen, 
   * just return 19.
   *    
   * write your teenSum method here
   */
    public static int teenSum(int a, int b)
    {
       if((a >= 13 && a <= 19) || (b >= 13 && b <= 19))
       {
           return 19;
       }
       else
       {
          return a + b; 
       }
    }
  // 7) write your factorial method here
      public static int factorial(int x)
      {
          if(x == 0)
          {
              return 1;
          }
          else
          {
              return x * factorial(x - 1);
          }
      }
  /* 8) sumDigits
   *    Given a non-negative int n, return the sum of its digits 
   *    recursively (no loops). Note that mod (%) by 10 yields 
   *    the rightmost digit (126 % 10 is 6), while divide (/) 
   *    by 10 removes the rightmost digit (126 / 10 is 12). 
   *    
   *    write your sumDigits method here
   */
        public static int sumDigits(int x)
        {
           if(x == 0)
          {
              return 0;
          }
          else
          {
              int ones = x % 10;
             
              int result = sumDigits(x / 10);
              
              return  result + ones;
          }
        }
  /* 9) blackjack
   *    Given 2 int values greater than 0, return whichever value 
   *    is nearest to 21 without going over. Return 0 if they both 
   *    go over. 
   *    
   *    write your blackjack method here
   */    
     public static int blackjack(int card1, int card2)
     {
        if(card1 <= 21 && card2 <= 21)
        {
            if(card1 > card2)
                return card1;
            else
                return card2;
        }
         
        else if (card1 > 21 || card2 > 21)
       {
                if(card1 > 21 && card2 > 21)
                    return 0;
                else if(card1 < card2)
                    return card1;
                else
                    return card2;
                
       }
      else
            return 0;
     } 
     
         
         
}