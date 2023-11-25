// THEOXARIS KAZAKIDIS A.M 4679
import java.util.Random;


class ComputerPlayerBonus
{
  private String name;
  private int[][] array;
  private int points;


  public ComputerPlayerBonus(String name,int N)
  {
    this.name=name;
    array= new int[N][2];

    for(int i=0;i<N;i++)
    {
      for(int j=0;j<array[i].length;j++)
      {
        array[i][j]=-1;
      }
    }

  }

  public void play(Board table)
  {
    int[] pairArr = new int[2];
    pairArr= pairsFound(table);
    if(pairArr[0]!=-1)
    {System.out.println("Computer Player "+toString()+" selected positions :"+pairArr[0]+" "+pairArr[1]);table.openPositions(pairArr[0], pairArr[1]);points++;}
    else
    {
      int position1=table.getRandomPosition();
      int position2=-2;

      if(array[table.getCard(position1)][0]!=-1)
      {
        position2=array[table.getCard(position1)][0];
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
         if(array[table.getCard(position1)][0]==-1)
        {
        array[table.getCard(position1)][0]=position1;
        }
        else if(array[table.getCard(position1)][0]!=-1 && array[table.getCard(position1)][1]==-1 && position1!=array[table.getCard(position1)][0])
        {
          array[table.getCard(position1)][1]=position1;
        }
        if(array[table.getCard(position2)][0]==-1)
        {
        array[table.getCard(position2)][0]=position2;
        }
        else if(array[table.getCard(position2)][0]!=-1  && array[table.getCard(position2)][1]==-1 && position2!=array[table.getCard(position2)][0])
        {
          array[table.getCard(position2)][1]=position2;
        }
      }
    }
  }

  private int[] pairsFound(Board table)
  {
    int[] arr= new int[2];
    arr[0]=-1;arr[1]=-1;
    for(int i=0;i<array.length;i++)
    {
      if(array[i][0]!=-1 && array[i][1]!=-1)
      {

        if(table.containsCard(array[i][0])==true)
        {
          arr[0]=array[i][0];
          arr[1]=array[i][1];
          array[i][0]=-1;
          array[i][1]=-1;
          return arr;
        }
        else
        {
          array[i][0]=-1;array[i][1]=-1;
          continue;
        }
      }
    }

    return arr;
  }


  public void print()
  {
    for(int i=0;i<array.length;i++)
    {
      System.out.println(array[i][0]+" "+array[i][1]);
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
  Board table = new Board(10);
  ComputerPlayerBonus cp = new ComputerPlayerBonus("aa",10);
  while(!table.allPairsFound()){cp.print();cp.play(table);}

}

}
