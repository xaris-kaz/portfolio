#Theocharis Kazakidis 
import random
#ftiaxnw tis analoges listes
playerslst=[ ]
Round=1
beanslst=[ ]

players=int(input("Please input the number of the players:"))

beans=int(input("Please input the number of beans per player:"))

for i in range(1,players+1):
   playerslst.append(i)

for i in range(0,players):
   beanslst.append(i)

for i in range(0,len(beanslst)):
   beanslst[i]=beans

#epilogi paiktwn
player=random.randint(1,playerslst[-1])


print('-------------------------------------------------------------------------------')
Pot=players
print("Round",Round,"begins: everyone puts 1")
print("Current state:")
print("Pot:",Pot)
for i in range (0,len(playerslst)):
    beanslst[i]-=1
    print("Player",playerslst[i]," 's budget: ",beanslst[i])   


while Pot>0:
    if players==0 or players==1:
      print("The game cannot be played with no players")
      print("Try Again")
      break
    elif players>1:
        
        #tixaia epilogi paiktwn
        act=random.randint(1,6)

        print("\n")

         

        #tixaia epilogi sbouras
        if  act==1:
            print("Player ",player,"spinned Put One")
        elif act==2:
            print("Player",player,"spinned Put Two")
        elif act==3:
            print("Player",player,"spinned Everyone Put One")
        elif act==4:
            print("Player",player,"spinned Take One")
        elif act==5:
            print("Player",player,"spinned Take Two")
        else:
            print("Player",player,"spinned Take Them All")

         
        print("Current state:   ")




        #Pontarisma
        if act==1:
            if beanslst[player-1]>=1:
                Pot=Pot+1
                print("Pot: ",Pot)
        elif act==1 and beanslst[player-1]<1:
            print("Pot: ",Pot)
        elif act==2 and beanslst[player-1]>=2:
            Pot=Pot+2
            print("Pot: ",Pot)
        elif act==2 and beanslst[player-1]==1:
            Pot+=1
            print("Pot:",Pot)
        elif act==2 and beanslst[player-1]<1:
            print("Pot:",Pot)
        elif act==3:
            for i in range(0,len(beanslst)):
                if beanslst[i]>=1:
                    Pot+=1
            print("Pot:",Pot)
        elif act==4 and Pot>=1:
            Pot=Pot-1
            print('Pot: ',Pot)
        elif act==5 and Pot>=2:
            Pot=Pot-2
            print('Pot: ',Pot)
        elif act==6:
            print('Pot: ',0)


        #budget me ta fasolia
        if act==1:
            beanslst[player-1]-=1
            for i in range(len(beanslst)):
                if beanslst[i]>=0:
                    print("Player",playerslst[i]," 's budget: ",beanslst[i])
                elif beanslst[i]<0:
                    print("Player",playerslst[i]," 's budget: eliminated")
        elif act==2:
            beanslst[player-1]-=2
            for i in range (len(beanslst)):
                if beanslst[i]>=0:
                    print("Player",playerslst[i]," 's budget: ",beanslst[i])
                elif beanslst[i]<0:
                    print("Player",playerslst[i]," 's budget: eliminated")
        elif act==3:
            for i in range(len(beanslst)):
                beanslst[i]-=1
                if beanslst[i]>=0:
                    print("Player",playerslst[i]," 's budget: ",beanslst[i])
                elif beanslst[i]<0:
                    print("Player",playerslst[i]," 's budget: eliminated")
        elif act==4:
            if Pot>=1:
                beanslst[player-1]+=1
            elif Pot<1:
                beanslst[player-1]+=0
            for i in range(len(beanslst)):
                if beanslst[i]>=0:
                    print("Player",playerslst[i]," 's budget: ",beanslst[i])
                elif beanslst[i]<0:
                    print("Player",playerslst[i]," 's budget: eliminated")
        elif act==5:
            if Pot>=2:
                beanslst[player-1]+=2
            elif Pot==1:
                beanslst[player-1]+=1
            elif Pot<1:
                beanslst[player-1]+=0
            for i in range(len(beanslst)):
                if beanslst[i]>=0:
                    print("Player",playerslst[i]," 's budget: ",beanslst[i])
                elif beanslst[i]<0:
                    print("Player",playerslst[i]," 's budget: eliminated")
        else:
            beanslst[player-1]+=Pot
            for i in range(len(beanslst)):
                if beanslst[i]>=0:
                    print("Player",playerslst[i]," 's budget: ",beanslst[i])
                elif beanslst[i]<0:
                    print("Player",playerslst[i]," 's budget: eliminated")
            Pot=0
            

        if Pot==0:
            print('Pot is zero: round ends')
            Round+=1
            for i in range(len(beanslst)):
                if beanslst[i]>=1:
                    Pot+=1
            print('-------------------------------------------------------------------------------')
            print('Round',Round,' begins: everyone puts 1')
            print('Current state:')
            print('Pot: ',Pot)
            for i in range(len(beanslst)):
                beanslst[i]-=1
                if beanslst[i]>=0:
                    print("Player",playerslst[i]," 's budget: ",beanslst[i])
                elif beanslst[i]<0:
                    print("Player",playerslst[i]," 's budget: eliminated")
                    


        if player<playerslst[-1]:
            player+=1
        elif player==playerslst[-1]:
            player=playerslst[0]
                    

