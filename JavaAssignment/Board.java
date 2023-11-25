// THEOXARIS KAZAKIDIS A.M 4679

import java.util.Random;

class Board
{
  private int[] array;
  private int cards;
  private int arraySize;
  private Random rand = new Random();



  private void delay(int sec){
		try {
			Thread.currentThread().sleep(1000*sec);
		}
		catch (InterruptedException e) {
			e.printStackTrace();
		}
	}


  private String header()
  {
    String temp1="";

    for(int i=0;i<arraySize;i++)
    {
        temp1+="  "+i;
    }

    return temp1;
  }

  private void fill()
  {
    //rand.setSeed(20);
    int x=0;
    for(int i=0;i<arraySize;i++)
    {
      if(i==(arraySize/2))
      {x=0;}
      array[i]=x;
      x++;
    }


    for(int i=0;i<arraySize;i++)
    {

      int y=rand.nextInt(arraySize);

      int temp=array[i];
      array[i]=array[y];
      array[y]=temp;

    }
  }






  public Board(int size)
  {
    array=new int[2*size];
    cards=2*size;
    arraySize=2*size;
    fill();
  }



  public void print()
  {

    String temp1="---";
    temp1=temp1.repeat(arraySize);
    if(arraySize>=10)
    {
      for(int i=10;i<=arraySize;i++)
      {temp1+="-";}
    }
    String temp2="";
    for(int i=0;i<arraySize;i++)
    {
      temp2+="  ";
      if(array[i]==-1)
      {
        temp2+=" ";
      }else{
        if(i<10)temp2+="*";
        else temp2+=" *";
      }

    }
    System.out.println(header()+"\n"+temp1+"\n"+temp2);

  }

  public void flash(int first_position,int second_position)
  {
    String temp1="---";
    temp1=temp1.repeat(arraySize);
    if(arraySize>=10)
    {
      for(int i=10;i<=arraySize;i++)
      {temp1+="-";}
    }
    String temp2="";
    String temp3="";
    for(int i=0;i<arraySize;i++)
    {
      temp2+="  ";
      if(array[i]==-1)
      {
        temp2+=" ";
      }
      else
      {
        if(i<10)
        {
          if(i==first_position || i==second_position)
          {temp2+=array[i];}
          else temp2+="*";

        }
        else
        {
        if(i==first_position || i==second_position)
          {
            temp2+=" "+array[i];
          }else temp2+=" *";
        }

      }
    }
    for(int i=0;i<arraySize;i++)
    {
      temp3+="  ";
      if(array[i]==-1)
      {
        temp3+=" ";
      }else{
        if(i<10)temp3+="*";
        else temp3+=" *";
      }

    }

    System.out.println(header());
    System.out.println(temp1);
    System.out.print(temp2);delay(10);System.out.print("\r"+temp3+"\n");

  }


  public boolean openPositions(int position1,int position2)
  {
    if(array[position1]==array[position2])
    {
      System.out.println("Pair found!"+"  ("+array[position1]+","+array[position2]+")");
      array[position1]=-1;array[position2]=-1;cards-=2;
      print();
      return true;
    }
    flash(position1,position2);
    return false;
  }


  public int getRandomPosition()
  {
    int pos=rand.nextInt(arraySize);
    while(!containsCard(pos))
    {
      pos=rand.nextInt(arraySize);
    }

    return pos;
  }

  public int getRandomPosition(int pos)
  {
    int x=rand.nextInt(arraySize);
    while(array[x]==-1 || x==pos)
    {
      x=rand.nextInt(arraySize);
    }

    return x;
  }

  public boolean containsCard(int pos)
  {
    if(array[pos]==-1)
    {return false;}
    else
    {return true;}
  }


  public int getCard(int pos)
  {
    return array[pos];
  }

  public boolean allPairsFound()
  {
    if(cards<=0)return true;
    else return false;
  }



  //to set seed einai sto line 187
  public static void main(String args[])
  {
    Board table = new Board(3);
   table.print();
   for(int i=0;i<6;i++)
   {
     System.out.println(table.getCard(i));
   }

   table.flash(0,table.getRandomPosition(0));
   table.openPositions(0,2);table.openPositions(0,1);
   System.out.println(table.containsCard(0)+"\n"+table.containsCard(2));
   table.openPositions(3, 4);
   System.out.println(table.containsCard(2)+"\n"+table.containsCard(5));
   table.openPositions(2, table.getRandomPosition(2));
   System.out.println(table.allPairsFound());

  }


}
