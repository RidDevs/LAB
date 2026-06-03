class Parent {

    void show() {
        System.out.println("Parent Class");
    }
}

class Child extends Parent {

    void show() {
        System.out.println("Child Class");
    }
}

public class Main {

    public static void main(String[] args) {

        Child c = new Child();

        c.show();
    }
}