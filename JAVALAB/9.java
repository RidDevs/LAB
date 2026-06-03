import java.awt.*;
import java.awt.event.*;

public class MyFrame extends Frame implements ActionListener {

    TextField tf;
    Button b;

    MyFrame() {

        tf = new TextField();
        tf.setBounds(50,50,150,30);

        b = new Button("Click");
        b.setBounds(50,100,80,30);

        b.addActionListener(this);

        add(tf);
        add(b);

        setSize(300,200);
        setLayout(null);
        setVisible(true);
    }

    public void actionPerformed(ActionEvent e) {
        tf.setText("Button Clicked");
    }

    public static void main(String[] args) {
        new MyFrame();
    }
}