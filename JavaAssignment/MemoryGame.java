// THEOXARIS KAZAKIDIS A.M 4679
import java.util.Scanner;

class MemoryGame
{

  public static void main(String args[])
  {
    Scanner input = new Scanner(System.in);
    System.out.println("Enter a number for the pairs: ");
    int pairs=input.nextInt();
    input.nextLine();
    while(pairs<=0)
    {
      System.out.println("Enter a valid number (at least 1) :");

    }
    Board table = new Board(pairs);


    System.out.println("Do you want to play between you and a ComputerPlayer? (yes/no) :");
    String answer=input.nextLine().strip().toLowerCase();
    while(!answer.equals("yes") || !answer.equals("no"))
    {
      if(answer.equals("yes") || answer.equals("no")){break;}
      System.out.println("Please enter a valid answer( yes or no) :");
      answer=input.nextLine().strip().toLowerCase();
    }

    if(answer.equals("yes"))
    {

      System.out.println("Please enter your name: ");
      HumanPlayer humanPlayer1 = new HumanPlayer(input.nextLine());
      ComputerPlayer puppet = new ComputerPlayer("MasterOfPuppets",pairs);

      while(!table.allPairsFound())
      {
        System.out.println("Its "+puppet+" turn!");
        puppet.play(table);
        System.out.println("Its your turn, "+humanPlayer1);
        humanPlayer1.play(table);
        System.out.println("---------------"+"\n"+humanPlayer1+" points: "+humanPlayer1.getPoints());
        System.out.println("---------------"+"\n"+puppet+" points: "+puppet.getPoints());
        System.out.println("---------------");
      }

      if(humanPlayer1.getPoints() < puppet.getPoints())
      {
        System.out.println("You lost!!!!");
      }
      else if(humanPlayer1.getPoints() > puppet.getPoints())
      {
        System.out.println("You won!");
      }
      else System.out.println("Its a tie!");

    }
    else
    {
      System.out.println(" Enter your name: ");
      HumanPlayer humanPlayer1 = new HumanPlayer(input.nextLine());
      System.out.println("Enter a name for the second player: ");
      HumanPlayer humanPlayer2 = new HumanPlayer(input.nextLine());
      input.close();

      while(!table.allPairsFound())
      {
        System.out.println("Its "+humanPlayer2+" turn!");
        humanPlayer2.play(table);
        System.out.println("Its your turn, "+humanPlayer1);
        humanPlayer1.play(table);
        System.out.println("---------------"+"\n"+humanPlayer1+" points: "+humanPlayer1.getPoints());
        System.out.println("---------------"+"\n"+humanPlayer2+" points: "+humanPlayer2.getPoints());
      }

      if(humanPlayer1.getPoints() < humanPlayer2.getPoints())
      {
        System.out.println("You won, "+humanPlayer2+"!!");
      }
      else if(humanPlayer1.getPoints() > humanPlayer2.getPoints())
      {
        System.out.println("You won, "+humanPlayer1+"!");
      }
      else System.out.println("Its a tie!");




    }


  }







}
