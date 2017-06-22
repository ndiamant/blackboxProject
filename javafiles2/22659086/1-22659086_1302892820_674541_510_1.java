class special
{
    public int factorial(int a)
    {
        int s=1;
        for(int i=1;i<=a;i++)
        {
            s=s*i;
        }
            return s;
        
        }
        public void main(int a)
        
       {int copy=a,g=0;
           while(a<0)
           {
            int d=a%10;
           g=g+factorial(d);
            a=a/10;
        }
        
        if(copy == g)
        System.out.println("special number");
        else 
        System.out.println("not");
    }
}
            