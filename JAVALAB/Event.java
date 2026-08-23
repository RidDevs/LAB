import java.awt.*;
import java.awt.event.*;

class EventExample extends Frame implements ActionListener{

    TextField tf;

    EventExample(){
        tf=new TextField(); //create components
        tf.setBounds(60,50,170,20);

        Button b=new Button("click me");
        b.setBounds(100,120,80,30);
        b.addActionListener(this);//register listener &passing current instance

        add(b); add(tf); //add components and set size, layout and visibility
        setSize(300,300);
        setLayout(null);
        setVisible(true);
    }

    public void actionPerformed(ActionEvent e){
    tf.setText("Welcome");
    }

    public static void main(String args[]){
    new EventExample();
    }
}
