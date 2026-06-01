class Student {
    int roll;
    String name;

    void getData(int r, String n) {
        roll = r;
        name = n;
    }

    void display() {
        System.out.println("Roll: " + roll);
        System.out.println("Name: " + name);
    }
}

public class Main {
    public static void main(String[] args) {
        Student s1 = new Student();

        s1.getData(1, "Human1");
        s1.display();
    }
}