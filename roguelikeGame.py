import pyglet
from pyglet.window import mouse
from pyglet.window import key
from pyglet.gl import glViewport
from pyglet.math import Mat4
import os
from math import sqrt,floor,ceil
import numpy as np
pyglet.options['dpi_scaling'] = 'real'
#####STUFF TO BE CHANGED OR AT LEAST REVIEWED WILL BE COMMENTED AS 'JANK'

class player:
        
    def __init__(
        self,                                   #lots of this info will be packaged into character arrays that get passed in, other modifiers will be hit by difficulty levels
        maxHp: int,                             #maxHp, character stuff (difficulty modified)
        materials: list[int],                   #materials, starts with a lil smth smth random for good luck
        relics: list[str],                      #character stuff
        deck: list[str],                        #character stuff, difficulty modifier (backpack?)
        drawPile: list[str],                    #empty list that gets made at start of combat
        hand: list[str],                        #ditto
        stack: list[str],                       #ditto
        discardPile: list[str],                 #ditto
        startCombatProcesses,                   #Package all the functions i want to run at the start of a combat   eg. initialize draw pile etc, heal 2 ;), setup position on map, Note: only player stuff
        endCombatProcesses,                     #ditto      eg. generate rewards, heal 6 ;)
        enterFloorProcesses,                    #ditto      eg. if entering shop heal, if entering campfire heal, check type of floor 
        turnNumber: int = 0,                    #Will be rechecked at start of combat
        drawHandSize: int = 5,                  #ditto
        maxHandSize: int = 11,                  #ditto
        energyGenRate: float = 0.8,             #ditto
        maxEnergy: float = 3,                   #ditto
        currentHp: int = 1,                     #if i want to do similar to sts ancient set to 1 and increase but for now idm
        refCoords: list[int] = [0,0],           #needs to be set dependent on room
    ):
        self.maxHp = maxHp
        self.currentHp = currentHp
        self.materials = materials
        self.relics = relics
        self.turnNumber = turnNumber
        self.deck = deck
        self.drawPile = drawPile
        self.hand = hand
        self.stack = stack
        self.discardPile = discardPile
        self.drawHandSize = drawHandSize
        self.maxHandSize = maxHandSize
        self.energyGenRate = energyGenRate
        self.maxEnergy = maxEnergy
        self.startCombatProcesses = startCombatProcesses
        self.endCombatProcesses = endCombatProcesses
        self.enterFloorProcesses = enterFloorProcesses
        self.moveProcesses = [self.move]
        self.moveProcessesDirections: list[int] = []                   #When hovering a card save the directions of the movements here, 0,1,2,3,4,5
        self.refCoords = refCoords
    def move(self,directions:list[int],movespeed: int=1):              #use directions=self.moveProcessesDirections most of the time if not always
        

        pass




    
    #what do i need
    ######CARD STUFF
    #card class arrays deck, draw pile, hand, stack? (currently playing cards), discard pile,  stack? (may as well implement this even if not planning on needing because gives options)
    ######UNIVERSAL STUFF
    #hp, materials, relics
    ######IN FIGHT STUFF
    #card stuff*, energy, turn number
    pass


class enemy:
    pass


class card:
    pass


class game:
    pass


class map:
    pass


currentState='menu'
def initializeMenu():
    characterHover='dia'                    #dia is a filler name
    #display everything that needs to be displayed on the screen
    pass

def initializeSettings():
    #do this later, just a bunch of setting options, set images dependent on the currrently saved settings
    #only update stuff when it's touched
    pass


def initializeGame(difficulty, character):
    #display the character and difficulty in the top left corner, display top hud
    #randomize the map
    #display the floor 0 screen
    #prepare player deck
    #empty player backpack
    #set player hp
    #set player gold?
    #clear player artefacts
    pass



def gameLoop():
    #
    #if realTime=True:
        #check player inputs
            #resolve player inputs
            #store short term info
        #check enemy timings
            #resolve enemy actions
            #store short term info
        #timer+=1 (note that this should be 1/120 but stick to ints for ease)
        #if frame is divisible by 120/fps
            #update graphics
    #pause for 1/120 seconds
    pass


def initalizeGrids(nInRow,nInCol,xPixDisplacement=1,yPixDisplacement=sqrt(3)/2):
    #nInRow is number of normal hex in a row
    #nInCol is number of normal hex in a column
    #setup all the points with coordinates, size, and 6 output locations
        #coordinates are based on an integer system, see design document
        #size is 1,2,3 (small, normal, combined)
        #outputs are default around a clock 1,2,3,4,5,6 and these are saved as the pointer to the hex where it outputs to
    #setup adjacency matrix using output locations
        #this is useful for easily doing range calculations and sht (ie is something in range of a move 4)

    #Refcoords are to be referenced when checking adjacencies (using coordinate grid, see reference doc)
    xRefCoord=0
    yRefCoord=0
    #all this will be done in a scale where 1=sideLength
    #pixcoords are to be scaled directly to pixel coordinates of the center of the hex
    xPixCoord=0
    yPixCoord=0

    numNormalHexes = nInRow*2*nInCol
    numSmallHexes=nInRow*2*(nInCol*2)+(nInRow*2-1)*(nInCol*2+1)
    #grid is generated as total number of hexes and in each row there is size,(xRefCoord,yRefCoord),(xPixCoord,yPixCoord),upOutputLoc,rightUpOutputLoc,rightDownOutputLoc,downOutputLoc,leftDownOutputLoc,leftUpOutputLoc
    grid=np.full((numNormalHexes+numSmallHexes,9),None,dtype=object)
    adjacency=np.zeros((numNormalHexes+numSmallHexes,numNormalHexes+numSmallHexes),dtype=int)
    

    ###For tracking which tiles are inplay, for display and for when tiles are changed
    inPlay=set()
    ####For fast checking for future (dictionary)
    normalCoordToIndex={}
    for i in range(0,2*nInRow):
        for j in range(0,nInCol):
            index=i*nInCol+j
            xRefCoord=i
            yRefCoord=j-floor(i/2)
                                                ########################################################
                                                #####IMPORTANT THIS IS CONVERSION FROM REF TO PIXEL#####
                                                ########################################################
            xPixCoord, yPixCoord = convRefToPix(xRefCoord,yRefCoord,xPixDisplacement,yPixDisplacement)

                                                #####Default Ouput Locations. Note: Some of these locations don't exist but that will be handled later
            upOutputLoc=(xRefCoord+0,yRefCoord-1)
            rightUpOutputLoc=(xRefCoord+1,yRefCoord-1)
            rightDownOutputLoc=(xRefCoord+1,yRefCoord+0)
            downOutputLoc=(xRefCoord+0,yRefCoord+1)
            leftDownOutputLoc=(xRefCoord-1,yRefCoord+1)
            leftUpOutputLoc=(xRefCoord-1,yRefCoord+0)

                                                #####Storing Stuff into the information grid
            grid[index,0]=2
            grid[index,1]=(xRefCoord,yRefCoord)
            grid[index,2]=(xPixCoord,yPixCoord)
            grid[index,3]=upOutputLoc
            grid[index,4]=rightUpOutputLoc
            grid[index,5]=rightDownOutputLoc
            grid[index,6]=downOutputLoc
            grid[index,7]=leftDownOutputLoc
            grid[index,8]=leftUpOutputLoc
            normalCoordToIndex[(xRefCoord,yRefCoord)]=index
            if (upOutputLoc in normalCoordToIndex):
                adjacency[normalCoordToIndex[(xRefCoord,yRefCoord)],normalCoordToIndex[upOutputLoc]]=1
                adjacency[normalCoordToIndex[upOutputLoc],normalCoordToIndex[(xRefCoord,yRefCoord)]]=1
            if (leftDownOutputLoc in normalCoordToIndex):
                adjacency[normalCoordToIndex[(xRefCoord,yRefCoord)],normalCoordToIndex[leftDownOutputLoc]]=1
                adjacency[normalCoordToIndex[leftDownOutputLoc],normalCoordToIndex[(xRefCoord,yRefCoord)]]=1
            if (leftUpOutputLoc in normalCoordToIndex):
                adjacency[normalCoordToIndex[(xRefCoord,yRefCoord)],normalCoordToIndex[leftUpOutputLoc]]=1
                adjacency[normalCoordToIndex[leftUpOutputLoc],normalCoordToIndex[(xRefCoord,yRefCoord)]]=1

            ###Add the index to the inPlay set
            inPlay.add(index)


                                                #####Repeat for the small grid with small adjustments
    smallCoordToIndex={}
    for i in range(0,4*nInRow-1):
        if i%2==0:
            placeHolder001=2*nInCol
        else:
            placeHolder001=2*nInCol+1
        for j in range(0,placeHolder001):
            index=2*nInRow*nInCol+i*2*nInCol+floor(i*1/2)+j
            xRefCoord=i/2
            yRefCoord=(j-ceil(i/2))/2           #####Changed to ceil, check reference doc

                                                #####Conversion remains the same
            xPixCoord, yPixCoord = convRefToPix(xRefCoord,yRefCoord, xPixDisplacement, yPixDisplacement)


                                                #####Default Ouput Locations. Note: Some of these locations don't exist but that will be handled later
                                                #####Scaled to 1/2
            upOutputLoc=(xRefCoord+0,yRefCoord-1/2)
            rightUpOutputLoc=(xRefCoord+1/2,yRefCoord-1/2)
            rightDownOutputLoc=(xRefCoord+1/2,yRefCoord+0)
            downOutputLoc=(xRefCoord+0,yRefCoord+1/2)
            leftDownOutputLoc=(xRefCoord-1/2,yRefCoord+1/2)
            leftUpOutputLoc=(xRefCoord-1/2,yRefCoord+0)

                                                #####Storing Stuff into the information grid (size=1)
            grid[index,0]=1
            grid[index,1]=(xRefCoord,yRefCoord)
            grid[index,2]=(xPixCoord,yPixCoord)
            grid[index,3]=upOutputLoc
            grid[index,4]=rightUpOutputLoc
            grid[index,5]=rightDownOutputLoc
            grid[index,6]=downOutputLoc
            grid[index,7]=leftDownOutputLoc
            grid[index,8]=leftUpOutputLoc
            smallCoordToIndex[(xRefCoord,yRefCoord)]=index
            if (upOutputLoc in smallCoordToIndex):
                adjacency[smallCoordToIndex[(xRefCoord,yRefCoord)],smallCoordToIndex[upOutputLoc]]=1
                adjacency[smallCoordToIndex[upOutputLoc],smallCoordToIndex[(xRefCoord,yRefCoord)]]=1
            if (leftDownOutputLoc in smallCoordToIndex):
                adjacency[smallCoordToIndex[(xRefCoord,yRefCoord)],smallCoordToIndex[leftDownOutputLoc]]=1
                adjacency[smallCoordToIndex[leftDownOutputLoc],smallCoordToIndex[(xRefCoord,yRefCoord)]]=1
            if (leftUpOutputLoc in smallCoordToIndex):
                adjacency[smallCoordToIndex[(xRefCoord,yRefCoord)],smallCoordToIndex[leftUpOutputLoc]]=1
                adjacency[smallCoordToIndex[leftUpOutputLoc],smallCoordToIndex[(xRefCoord,yRefCoord)]]=1

    return grid, adjacency, normalCoordToIndex, smallCoordToIndex, inPlay



####Note: we should pass the centre hexes through this function last when modifying muliple hexes
####Also note: although the function is named normal to small it converts anything to small (ie not in play small to small or normal to small)
def normalToSmall(grid, adjacency, xRefCoord, yRefCoord, normalCoordToIndex, smallCoordToIndex, inPlay, hexes):
    #####Takes an inputed coordinate for a small hex that wants to be created
    ####Checks if that coordinate is already inPlay (as a small hex)
        ####Already inPlay -> return
        ####Not inPlay -> Continue
    ####Checks if that coordinate is a centre or edge hex (does it have an integer coordinate or not)
        ####Centre -> check if all edge hexes are small
            ####All are small -> Put in play, take normal out of play return
            ####Not all small -> return
        ####Edge -> put in play, check type of edge (1/2,int),(int,1/2),(1/2,1/2)
            ####Update all 6 directions with lots of if statements :D
    
    index=smallCoordToIndex[(xRefCoord,yRefCoord)]
    if index in inPlay:
        return grid, adjacency, inPlay
    
    if (xRefCoord % 1 == 0) and (yRefCoord % 1 == 0):
        placeHolder002={smallCoordToIndex[(xRefCoord+0,yRefCoord-1/2)],smallCoordToIndex[(xRefCoord+1/2,yRefCoord-1/2)],smallCoordToIndex[(xRefCoord+1/2,yRefCoord+0)],smallCoordToIndex[(xRefCoord+0,yRefCoord+1/2)],smallCoordToIndex[(xRefCoord-0,yRefCoord+1/2)],smallCoordToIndex[(xRefCoord-1/2,yRefCoord+0)]}
        if placeHolder002 <= inPlay:
            inPlay.discard(normalCoordToIndex[(xRefCoord,yRefCoord)])
            inPlay.add(index)
            grid, adjacency = changePathsForSmall(grid, adjacency, xRefCoord, yRefCoord, normalCoordToIndex, smallCoordToIndex, inPlay, True)
            return grid, adjacency, inPlay, hexes
    else:
        inPlay.add(index)
        grid, adjacency = changePathsForSmall(grid, adjacency, xRefCoord, yRefCoord, normalCoordToIndex, smallCoordToIndex, inPlay, False)
        return grid, adjacency, inPlay, hexes
        
    return grid, adjacency, inPlay, hexes


def changePathsForSmall(grid, adjacency, xRefCoord, yRefCoord, normalCoordToIndex, smallCoordToIndex, inPlay, centre):
    directions=[[0,-0.5,3],[0.5,-0.5,4],[0.5,0,5],[0,0.5,6],[-0.5,0.5,7],[-0.5,0,8]]
    index=smallCoordToIndex(xRefCoord,yRefCoord)

    for i in directions:
        if normalCoordToIndex[(xRefCoord+i[0],yRefCoord+i[1])] in inPlay:
            ###Need 4 indices: Current output, future output, reverse current output of future output, reverse future output of future output
            cO=grid[index, i[2]]
            fO=normalCoordToIndex[(xRefCoord+i[0],yRefCoord+i[1])]
            rCOoFO=grid[fO, 11-i[2]]
            rFOoFO=index

            grid[index,i[2]]=(xRefCoord+i[0],yRefCoord+i[1])
            adjacency[index,fO]=1                   #set the centre to this direction to open
            adjacency[index,cO]=0                   #set the centre to the small spot to closed
            adjacency[fO,rFOoFO]=1                  #set the reverse to open
            adjacency[fO,rCOoFO]=0                  #set the old path from the other to closed

        elif smallCoordToIndex[(xRefCoord+i[0],yRefCoord+i[1])] in inPlay:         
            cO=grid[index, i[2]]
            fO=smallCoordToIndex[(xRefCoord+i[0],yRefCoord+i[1])]
            rCOoFO=grid[fO, 11-i[2]]
            rFOoFO=index

            grid[index,i[2]]=(xRefCoord+i[0],yRefCoord+i[1])
            adjacency[index,fO]=1
            adjacency[index,cO]=0
            adjacency[fO,rFOoFO]=1
            adjacency[fO,rCOoFO]=0

        else:
            #Find which axis it shares with integer hexes
            #Take the dot product of the pixel movement and the axis, move in that direction (no need for projections and scaling lol but you could)
            #Note that we only need to change the current output and future output
                        #####JANK COULD JUST MAKE A CASE TABLE, WOULD BE SLIGHTLY FASTER (but less cool D:)
            dxPixCoord=(i[0]/2)*3
            dyPixCoord=(i[1]/2)*sqrt(3)+(i[0]/2)*sqrt(3)/2
            if xRefCoord % 1 == 0:               #vertical axis
                placeHolder006=dxPixCoord*0+dyPixCoord*1            #dot product
                if placeHolder006>0:
                    oD=[0,0.5,i[2]]                                  #output direction
                else:
                    oD=[0,-0.5,i[2]]
            elif yRefCoord % 1 == 0:                #down right axis
                placeHolder006=dxPixCoord*1.5+dyPixCoord*sqrt(3)/2
                if placeHolder006>0:
                    oD=[0.5,0,i[2]]                                  #output direction
                else:
                    oD=[-0.5,0,i[2]]
            else:
                placeHolder006=dxPixCoord*(-1.5)+dyPixCoord*sqrt(3)/2
                if placeHolder006>0:
                    oD=[-0.5,0.5,i[2]]                                  #output direction
                else:
                    oD=[0.5,-0.5,i[2]]

            fO=normalCoordToIndex[(xRefCoord+oD[0],yRefCoord+oD[1])]
            cO=grid[index, i[2]]

            grid[index,i[2]]=(xRefCoord+oD[0],yRefCoord+oD[1])
            adjacency[index,fO]=1
            adjacency[index,cO]=0

    return grid, adjacency



####Make a function to display all inPlay hexes (do normals first and then draw over them)
####Recieve mouse inputs, highlight hovered hex and set it so i can click a hex to turn it from normal to small

def initializeWindow(x,y):
    window = pyglet.window.Window(width=x, height=y, resizable=True)
    return window

def initializeHexGraphics(grid,inPlay,sideLength):                                                         #####Update this to work with any set of hexes, with variations for level
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backgroundBatch=pyglet.graphics.Batch()
    normalHexes = pyglet.graphics.Group(order=0)
    smallHexes = pyglet.graphics.Group(order=1)
    normalHexPath = os.path.join(script_dir, "scaledImages", 'sandHex.png')
    normalHex=pyglet.image.load(normalHexPath)
    normalHex.anchor_x = normalHex.width // 2
    normalHex.anchor_y = normalHex.height // 2
    smallHexPath = os.path.join(script_dir, "scaledImages", 'sandHexSmall.png')
    smallHex=pyglet.image.load(smallHexPath)
    smallHex.anchor_x = smallHex.width // 2
    smallHex.anchor_y = smallHex.height // 2
    hexes={}

    for index,row in enumerate(grid):
        x=row[2][0]*sideLength
        y=row[2][1]*sideLength
        if row[0]==2:
            sprite = pyglet.sprite.Sprite(img=normalHex, x=x, y=y,batch=backgroundBatch,group=normalHexes)
            hexes[row[0],row[1]]=sprite

        if row[0]==1:
            sprite = pyglet.sprite.Sprite(img=smallHex, x=x, y=y,batch=backgroundBatch,group=smallHexes)
            hexes[row[0],row[1]]=sprite
            hexes[row[0],row[1]].visible=False


    return hexes, backgroundBatch

                ###CONVERSIONS

def convRefToPix(xRefCoord,yRefCoord,xPixDisplacement,yPixDisplacement):
    xPixCoord=xPixDisplacement+xRefCoord*3/2
    yPixCoord=yPixDisplacement+yRefCoord*sqrt(3)+xRefCoord*sqrt(3)/2
    return xPixCoord, yPixCoord

def convPixToRef(xPixCoord,yPixCoord,xPixDisplacement,yPixDisplacement):
    xRefCoord=2/3*((xPixCoord)-xPixDisplacement)
    yRefCoord=(yPixCoord)/sqrt(3)-yPixDisplacement/sqrt(3)-1/3*((xPixCoord)-xPixDisplacement)
    return xRefCoord, yRefCoord

def hexHitbox(xPixCoordReal,yPixCoordReal,targettingType,grid,normalCoordToIndex,smallCoordToIndex,inPlay,sideLength,xPixDisplacement=1,yPixDisplacement=sqrt(3/2)):             #targettingTypes -> normal (target normal hexes only) -> small (target small hexes only) -> in play (target in play hexes (prio small over normal))
    xPixCoord=xPixCoordReal/sideLength
    yPixCoord=yPixCoordReal/sideLength
    xRefCoord, yRefCoord = convPixToRef (xPixCoord, yPixCoord, xPixDisplacement, yPixDisplacement)
    print(xRefCoord,yRefCoord)
    hitIndex=-1

    if targettingType=='normal' or targettingType=='2':
        candidateRefCoords=[(floor(xRefCoord),floor(yRefCoord)),(floor(xRefCoord),ceil(yRefCoord)),(ceil(xRefCoord),floor(yRefCoord)),(ceil(xRefCoord),ceil(yRefCoord))]
        score=1
        for i in candidateRefCoords:
            if i in normalCoordToIndex:
                index=normalCoordToIndex[i]
                currentScore=(xPixCoord-grid[index,2][0])**2+(yPixCoord-grid[index,2][1])**2
                if currentScore<score:
                    hitIndex=index
                    score=currentScore
    
    if targettingType=='small' or targettingType=='1':
        print("HUH")
        candidateRefCoords=[(floor(2*xRefCoord)/2,floor(2*yRefCoord)/2),(floor(2*xRefCoord)/2,ceil(2*yRefCoord)/2),(ceil(2*xRefCoord)/2,floor(2*yRefCoord)/2),(ceil(2*xRefCoord)/2,ceil(2*yRefCoord)/2)]
        score=1
        for i in candidateRefCoords:
            if i in smallCoordToIndex:
                index=smallCoordToIndex[i]
                currentScore=(xPixCoord-grid[index,2][0])**2+(yPixCoord-grid[index,2][1])**2
                if currentScore<score:
                    hitIndex=index
                    score=currentScore
    
    if targettingType=='inPlay' or targettingType=='0':
        normalCandidateRefCoords=[(floor(xRefCoord),floor(yRefCoord)),(floor(xRefCoord),ceil(yRefCoord)),(ceil(xRefCoord),floor(yRefCoord)),(ceil(xRefCoord),ceil(yRefCoord))]
        smallCandidateRefCoords=[(floor(2*xRefCoord)/2,floor(2*yRefCoord)/2),(floor(2*xRefCoord)/2,ceil(2*yRefCoord)/2),(ceil(2*xRefCoord)/2,floor(2*yRefCoord)/2),(ceil(2*xRefCoord)/2,ceil(2*yRefCoord)/2)]
        score=1
        for i in normalCandidateRefCoords:
            if (i in normalCoordToIndex):
                index=normalCoordToIndex[i]
                if index in inPlay:
                    currentScore=(xPixCoord - grid[index,2][0])**2+(yPixCoord - grid[index,2][1])**2
                    ####print(currentScore,i)
                    if currentScore<score:
                        hitIndex=index
                        score=currentScore

        for i in smallCandidateRefCoords:
            if i in smallCoordToIndex:
                index=smallCoordToIndex[i]
                if index in inPlay:
                    currentScore=(xPixCoord - grid[index,2][0])**2+(yPixCoord - grid[index,2][1])**2
                    if currentScore<score:
                        hitIndex=index
                        score=currentScore


    return hitIndex
        

###TESTING

numInRow=5
numInCol=6
sideLength=119
logicalXSize=int(sideLength*(numInRow*1.5+0.25))*2
logicalYSize=int(103*(numInCol+0.5))*2
logicalAspectRatio=logicalXSize/logicalYSize
window=initializeWindow(logicalXSize,logicalYSize)
grid, adjacency, normalCoordToIndex, smallCoordToIndex, inPlay = initalizeGrids(5,6)
hexes, backgroundBatch = initializeHexGraphics(grid, inPlay, 119)
#hexes[1,(8,-3.5)].visbile=True

@window.event
def on_draw():
    window.clear()
    backgroundBatch.draw()

@window.event
def on_resize(width, height):
    windowAspectRatio = width / height
    
    if windowAspectRatio > logicalAspectRatio:
        # Window is wider than game -> Pillarboxes (bars on left/right)
        viewHeight = height
        viewWidth = int(height * logicalAspectRatio)
        viewX = (width - viewWidth) // 2
        viewY = 0
    else:
        # Window is taller than game -> Letterboxes (bars on top/bottom)
        viewWidth = width
        viewHeight = int(width / logicalAspectRatio)
        viewX = 0
        viewY = (height - viewHeight) // 2

    # 2. Apply the centered viewport bounding box
    window.viewport = (viewX, viewY, viewWidth, viewHeight)
    
    # 3. Apply the 800x600 logical coordinate projection matrix
    window.projection = Mat4.orthogonal_projection(0, logicalXSize, 0, logicalYSize, -1, 1)
    


@window.event
def on_mouse_press(x, y, button, modifiers):
    print(x,y)
    hitIndex=hexHitbox(x,y,'normal',grid,normalCoordToIndex,smallCoordToIndex,inPlay,sideLength)
    if hitIndex==-1:
        print("Not in grid")
    else:
        print(grid[hitIndex,1])
    #print(grid[hitIndex,2][0]*sideLength,grid[hitIndex,2][1]*sideLength)

pyglet.app.run(1/120)

