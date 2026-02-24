class Box{
double volume(int width, int height, int depth)
  {return width * height * depth;}

public static void main (String args[]) {
Box mybox1 = new Box();
Box mybox2 = new Box();
double vol;

vol = mybox1.volume(5,99,22);
System.out.println("Volume is " + vol);
 
vol = mybox2.volume(1,7,2);
System.out.println("Volume is " + vol);
}
}
