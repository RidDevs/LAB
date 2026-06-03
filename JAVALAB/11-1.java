class Demo {

    void add(int a, int b) {
        System.out.println(a + b);
    }

    void add(int a, int b, int c) {
        System.out.println(a + b + c);
    }
}

public class Main {
    public static void main(String[] args) {

        Demo d = new Demo();

        d.add(10,20);
        d.add(10,20,30);
    }
}