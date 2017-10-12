#!/usr/bin/env python
from flask import Flask
from flask import request
nextId=0
waitingForGame=0
positions=[]
app = Flask(__name__)
#game=Game(Player(1),Player(2))



class Game:
    def __init__(self, player1, player2):
        self.GameID = (player1.sessionID, player2.sessionID)
        self.player1=player1
        self.player2=player2
        #arrow keys are cool
    def __str__(self):
        return str(self.GameID)
    def update(self):
        print("update called")
        self.player1.update()
        self.player2.update()
        a=0
        def checkForHit(playershoot, playerhit):
            print(playershoot.sessionID, playerhit.sessionID)
            for i in playershoot.pellets:
                if i.position[0]<=playerhit.x2 and i.position[0]>=playerhit.x1 and i.position[1]<=playerhit.y2 and i.position[1]>=playerhit.y1:
                    playerhit.hp-=i.damage
                    if playerhit.hp<=0:
                        print("ENDGAME")
                        playerhit.dead=True
                        break;
                    print(i.position)
                    print(playerhit.x2, playerhit.x1, playerhit.y2, playerhit.y1)
                    print(playerhit.sessionID)
                    print(playerhit.hp)
                else:
                    print("miss")
        #for i in self.player1.pellets:
        #    i.position=[0,0]
            
        #for i in self.player2.pellets:
        #    i.position=[0,0]
        
        checkForHit(self.player1, self.player2)
        checkForHit(self.player2, self.player1)
    def whowon(self):
        if self.player1.dead==True and self.player2.dead==True:
            print("Tie")
        elif self.player2.dead==True and self.player1.dead==False:
            print("Player 1 wins!")
        else:
            print("Player 2 wins!")    
    def maingameloop(self):
        while(self.player1.dead==False and self.player2.dead==False):
            self.update()       
        self.whowon()       



            #print("new position")
            #print(a)
            #print(i.position)
class Pellets:
    def __init__(self, damage=1, size=1, speed=1, position=[0,0]):
        self.damage = damage
        self.size = size
        self.speed=speed
        self.position=position
    def update(self):
       # print("updating")
       # print(self.position)
        self.position[1]+=self.speed
      #  print(self.position)
    
class Player:
    def __init__(self, sessionID, pellets=[], hp=10, name="cats", speed=10, position=[0,0], pelletspeed=1):
        self.sessionID=sessionID
        self.hp=hp
        self.name=name
        self.speed=speed
        self.position=position
        self.pellets=list(pellets) 
        #lists in parameters dont clone
        self.x1=self.position[0]-5
        self.x2=self.position[0]+5
        self.y1=self.position[1]-5
        self.y2=self.position[1]+5
        self.pelletspeed=pelletspeed
        self.dead=False

    def update(self):
     #   print(self.sessionID)
        self.pellets.append(Pellets(1,1,self.pelletspeed,list(self.position)))
     #   print("position")
    #    print(self.pellets[0].position)
        for i in self.pellets:
            i.update()
           # print("debug")
           # print (i.position)
    #    for i in self.pellets:
            # print('w;')
           # print(i.position)
         
#i=Game(Player(1, [], 10, "cats", 10, [0,0], 1), Player(2, [], 10, "Cats",10, [0,10], -1))
#i.maingameloop()
game=Game(Player(1),Player(2))
allltheinformation={"player1position": game.player1.position, "player2position": game.player2.position, "pelletsposition": [i.position for i in game.player1.pellets]}
@app.route('/cats/<string:name>')
def hello_world(name):
    return 'Hello {0}!'.format(name)

@app.route('/newSession')
def newSession():
    global nextId
    global waitingForGame
    global game
    nextId+=1
    pid=nextId
    if waitingForGame!=0:
        newGame=Game(Player(waitingForGame),Player(pid))
        waitingForGame=0
        game=newGame
        #print("new game created")
        return str(newGame)
    else:
        waitingForGame=pid
    return str(waitingForGame)

#@app.route('/move', methods=['POST', 'GET'])
@app.route('/move')
def move():
    global positions
    """
    if request.method=='POST':
        sessionID=request.form["sessionID"]
        
        position=request.form["playerposition"]
        if sessionID==game.player1.sessionID:
            game.player1.position=position
            
        else:
            game.player2.position=position
    return str(1)
    """
    sessionID = request.args.get("sessionID")
    position = request.args.get("position")
    if sessionID==game.player1.sessionID:
        game.player1.position=position
    else:
        game.player2.position=position
    return str(1)
    
@app.route('/')
def mainPage():
  return open("./client.html").read()


app.run(port=8888, debug=True)
