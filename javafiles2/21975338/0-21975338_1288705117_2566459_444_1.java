import java.util.*;
class factorial
{
    int num,f;
    factorial()
    {
        f=1;
    }
    factorial(int n)
    {
        num=n;
    }
    void GetFactorial()
    {
        int ans=1;
        for(f=num;f>=1;f--)
        ans*=f;
        abc(ans);
    }
    void abc(int ans)
    {
        int n;
        Scanner S=new Scanner(System.in);
        n=S.nextInt();
        factorial ob=new factorial(n);
        System.out.print(ans);
    }
}