class Calculation{
void sum(int a, int b)
{
System.out.println(a+b);
}
void sum(int a, int b, int c)
{
System.out.println(a+b+c);
}
void sum(double a, double b)
{
System.out.println(a+b);
}
}
class CalDemo{
public static void main(String args[]){
Calculation obj = new Calculation();
obj.sum(10,10,10);
obj.sum(20,20);
obj.sum(20.50,20.00);
}
}
