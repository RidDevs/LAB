import java.awt.*;
import java.util.*;
import java.awit.event.*;

public class MyFrame extends Frame implements ActionListener {

    TextField t;
    Button b;



    MyFrame(){
        setSize(300,300);
        setLayout(null);
        setVisible(true);

        t= new TextField();
        t.setBounds(120,100,80,30);

        b= new Button("click button");
        b.setBounds(120,100,80,30);
        b.ActionListener(this);

        add(t);
        add(b);
    }

    public void run(ActionEvent e){
        t.setText("clicked");
    }
    
    public static void main (String[] args){
        
     new MyFrame();
    }
}