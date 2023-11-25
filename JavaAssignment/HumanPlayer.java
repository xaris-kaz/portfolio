// THEOXARIS KAZAKIDIS A.M 4679
import java.util.Scanner;

class HumanPlayer
{
  private String name;
  private int points;
  private Scanner input;


  public HumanPlayer(String name)
  {
    this.name=name;
    input=new Scanner(System.in);
  }

  public void play(Board table)
  {
    String temp[] = new String[2];
    int ans[] = new int[2];

    System.out.print("Enter your positions (seperated with whitespace) : ");
    temp=input.nextLine().split(" ");
    ans[0]=Integer.parseInt(temp[0]);ans[1]=Integer.parseInt(temp[1]);

    while((ans[0]<0 || ans[1]<0) || (ans[0]==ans[1]) || (!table.containsCard(ans[0])) || !table.containsCard(ans[1]))
    {
      if(ans[0]<0 || ans[1]<0)
      {
        if(ans[0]<0){ System.out.println("Enter a valid number for your first position (not negative) :");ans[0]=input.nextInt();input.nextLine();
        }
        else {System.out.println("Enter a valid number for your second position (not negative) :");ans[1]=input.nextInt();input.nextLine();}
      }
      else if(ans[0]==ans[1])
      {
        System.out.println("You selected the same position twice. Enter a different position: ");
        ans[0]=input.nextInt();
        input.nextLine();
      }
      else if(!table.containsCard(ans[0]) || !table.containsCard(ans[1]))
      {
        if(table.containsCard(ans[0])==false)
        {
          System.out.println("Your first position does not contain a card. Please enter a valid number : ");
          ans[0]=input.nextInt();input.nextLine();


        }
        else
        {
          System.out.println("Your second position does not contain a card. Please enter a valid number : ");
          ans[1]=input.nextInt();input.nextLine();

        }
      }
    }


    if(table.openPositions(ans[0],ans[1]))
    {
      points++;
    }



  }


  public int getPoints()
  {
    return points;
  }


  public String toString()
  {
    return name;
  }


}
