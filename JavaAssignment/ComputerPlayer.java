// THEOXARIS KAZAKIDIS A.M 4679

import java.util.Random;


class ComputerPlayer
{
  private String name;
  private int[] array;
  private int points;


  public ComputerPlayer(String name,int size)
  {
    array= new int[size];
    this.name=name;

    for(int i=0;i<size;i++)
    {
      array[i]=-1;
    }

  }

  public void play(Board table)
  {
    int position1=table.getRandomPosition();
    int position2=-2;
    int card1=array[table.getCard(position1)];


    if(card1!=-1)
    {
      position2=card1;

      if(position1==position2)
      {
        position2=table.getRandomPosition(position1);
      }
    }
    else position2=table.getRandomPosition(position1);

    System.out.println("Computer Player "+toString()+" selected positions :"+position1+" "+position2);

    if(table.openPositions(position1,position2)) points++;
    else
    {
      int card2=array[table.getCard(position2)];

      if(card1==-1)
      {
      array[table.getCard(position1)]=position1;
      }
      if(card2==-1)
      {
      array[table.getCard(position2)]=position2;
      }
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


public static void main(String args[])
{
  Board table = new Board(10);ComputerPlayer puppet = new ComputerPlayer("aa",10);
  while(!table.allPairsFound())
  {puppet.play(table);}

}

}
