#Metropolis deck builder city builder by Lucas

#TODO:
#left off at 
#rename options to upgrades
#change all occurances of decodeCoords(string) to newDecodeCoords(string, Game)
#when multiple houses are unsatisfied at end turn, only show lives remaining once after showing unsatisfied messages
#add command test, similar to dist but only points at dissatisfied houses, doesnt show board if all satisfied
#when showing deck or remaining actions show sorted
#debug commands for directly changing the board or your deck
#make SimpleResource, SimpleAction, and SimpleEvent classes that simple game classes can inherit from such as: place Building or Resource
#make upgrades system and decay system
#most of Game.nextRound()

#future game content plans:
    #more Houses:
        #mansion: no Resource, must have visibility from itself to at least 8 tiles in cardinal directions.
        #squirrel: same as Groceries but Resource does not block path. (yes the squirrel also lives in a House)
        #friend: no Resource, must be within 6 tiles of 2 other friends. (cannot use Game.distanceCache)
        #euclidean: must be within radius 4 of any Resource in a straight euclidean distance, ignores path blockers.
        #rock: Event, no Resource, does nothing, is always satisfied, just blocks placement.
    #upgrade system:
        #some rounds you are presented with 3 choices, you can pick any of the choices at any time during the round with a command.
        #these choices are often extra Resources or other things to add to your deck that will help you.
        #some ideas for options that are not simply introducing a new lettered House's Resource:
            #action that has a chance to destroy Building on inputted coord.
            #action that destroys Building with small chance to miss and destroy random adjacent instead.
            #one time action that refreshes your other actions.
            #event that places , 2 times wich blocks random Houses appearing on it but does not block pathing or you building on it.
            #one time action that places a long street. (requires inputting 2 coords in a line)
        #Game must have a method to display the options in a nice visual.
        #the options can change depending on how far you are or if any House is almost unsatisfied.
    #overall game balance:
        #Events that place Houses should be changed such that each tile is given a weighted chance,
            #this chance should be lowered the more satisfied the House would be if placed there,
            #this chance should be increased on tiles with many neighbouring Buildings of any kind.
        #in rounds that you are not given options you are given packs instead:
            #this will sometimes be a mechanic, including House and its relative Resource as an Event, Action pair added to your deck.
            #it can also be a mechanic already in your deck, in wich case will get no Resource or 2 Events.
        #decay keeps the board from going stale in many ways and allow advanced strategy for more experienced players:
            #Houses can depart naturally if it has existed for long enough wich will not reduce lives.
                #this can be excellerated each turn if it is barely satisfied.
            #Actions will degrade slowly, reducing chance to succeed, and eventually break completely.
                #Actions will degrade each turn, this amount is randomly decided upon __init__().
                #Actions will keep track of how many turns it was used in a row, degrading upon use depending on streak.
                #upon __init__() a random threshhold between 50% and 100% is decided for how degraded the Action must be before having a chance to fail.
                #upon 100% degraded the Action is removed from your deck, fresh Actions are easy to add back cuz less Actions gives a higher chance to appear in upgrades.
            #Resources should also have some mechanic to dissapear eventually but i have not decided on its cause yet.
                #maybe if a Resource provides for no House, it dissapears at round end.
                #maybe on turn 5 you get an Event that removes a random Resource each turn.
            #(bad) Events in your deck should eventually duplicate if youve had them for a while. (without giving you more Resources)
        #maybe allow some Houses to pathfind outside the board.
    #allow saving and loading, storing multiple Game objects in a seperate save file.



def main():
    #REPLACE comment out tests when exporting
    # print(int('hi'))
    # print(max([n for n in range(5), 7, -3]))

    game = newGame()
    game.nextRound()
    while game.lives > 0:
        inp = input().split(' ')
        game.handleInput(inp)
    #TODO handle game end (show score, ask to play again)



def changeBase(string: str, baseIn: str, baseOut: str) -> str:
    '''changes the base of the given string, base parameters are strings of digit values starting at 0.
        does not handle floats or negative numbers.
        >>> changeBase('13', '0123456789', '01')
        '1101'
        >>> changeBase('33', '0123456789', 'zabcdefghijklmnopqrstuvwxy')
        'ag'
        >>> changeBase('11001000', '01', '0123456789')
        '200'
        '''
    if len(baseIn) < 2 or len(baseOut) < 2:
        raise ValueError('base lengths must be at least 2.')
    value = 0
    magnitude = 1
    for l in string[::-1]:
        value += baseIn.find(l) *magnitude
        magnitude *= len(baseIn)
    result = ''
    magnitude = 1
    while magnitude <= value:
        result += baseOut[value //magnitude %len(baseOut)]
        magnitude *= len(baseOut)
    if result == '':
        return baseOut[0]
    return result[::-1]

def decodeCoords(string: str):
    chars = ''
    nums = ''
    for c in string:
        if c in 'zabcdefghijklmnopqrstuvwxy':
            chars += c
            continue
        if c in '0123456789':
            nums += c
            continue
        if c in '.-':
            print('coordinates do not support negative or float numbers.')
            return (0, 0, False)
        chars = ''
        break
    if '' in (chars, nums):
        print('coordinates not recognised, please enter coords such as: e11, 4h')
        return (0, 0, False)
    return (int(changeBase(chars, 'zabcdefghijklmnopqrstuvwxy', '0123456789')), int(nums), True)

def newDecodeCoords(string, game):
    '''turns input text into x, y coordinates,
    also returns error message if and what went wrong.
    '''
    chars = ''
    nums = ''
    for c in string:
        if c in 'zabcdefghijklmnopqrstuvwxy':
            chars += c
            continue
        if c in '0123456789':
            nums += c
            continue
        return (0, 0, 'please only enter letters and numbers as a coordinate.')
    if '' in (chars, nums):
        return (0, 0, 'coordinates not recognised, please enter coords such as: e11, 4h.')
    if len(chars) > 5 or len(nums) > 5:
        return (0, 0, 'coordinates too big to convert.')
    x = int(changeBase(chars, 'zabcdefghijklmnopqrstuvwxy', '0123456789')) -1
    y = int(nums) -1
    if not(0 <= x < game.sizeX and 0 <= y < game.sizeY):
        return (x, y, 'coordinates are outside of board.')
    return (x, y, '')

def newGame():
    print('starting new game.')
    sizeX, sizeY = getBoardSize()
    game = Game(sizeX, sizeY)
    return game

def getBoardSize():
    return (25, 15)  #REPLACE remove this and allow custom board sizes
    while True:
        s = input('enter map size: ')
        #TODO allow entering custom size as two numbers or a coordinate
        if s in ('s', 'S', 'small'):
            return (10, 7)
        if s in ('m', 'M', 'medium'):
            return (20, 15)
        if s in ('l', 'L', 'large'):
            return (30, 22)
        print('please choose from small, medium, large.')



class Game:
    def __init__(self, sizeX, sizeY):
        self.round = 0
        self.lives = 5
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.board = [[None for x in range(self.sizeX)] for y in range(self.sizeY)]
        self.deck = [GroceriesEvent(self), GroceriesAction(self), StreetAction(self)]
        # self.deck.append(CornerEvent(self))  #TEMP
        # self.deck.append(CornerAction(self))  #TEMP
        # self.deck.append(MansionEvent(self))  #TEMP
        self.distanceCache = {}
        self.actionsRemaining = []
        self.flags = [' ' *self.sizeX for y in range(self.sizeY)]
        self.marks = [' ' *self.sizeX for y in range(self.sizeY)]
        self.packs = []
        self.installPacks([[GroceriesEvent, GroceriesAction], [CornerEvent, CornerAction], [MansionEvent]])  #TODO add more packs
        self.options = [Option(self), StreetOption(self), Option(self), GroceriesOption(self)]  #TEMP change back to [] after testing

    def installPacks(self, packs):
        for pack in packs:
            #weight is the base likeliness of each pack and is decided upon starting new game
            #avoid is the weight multiplier depending on how recently it was chosen
            self.packs.append({'content': pack, 'weight': 1, 'avoid': 0})
        #REPLACE maybe change bias curve
        amount = len(self.packs)
        for n in range(len(self.packs)):
            self.packs[n]['weight'] = 1 -n /amount

    def showBoard(self):
        line = '    '
        for x in range(self.sizeX):
            s = changeBase(str(x +1), '0123456789', 'zabcdefghijklmnopqrstuvwxy')
            line += ' ' *(2 -len(s))  +s
        print(line)
        print('   +'  +'--' *self.sizeX)
        visual = self.flags[:]
        if True in [False in [tile == ' ' for tile in line] for line in self.marks]:
            visual = self.marks[:]
            self.marks = [' ' *self.sizeX for y in range(self.sizeY)]
        for y in range(self.sizeY):
            line = ' ' *(2 -len(str(y +1)))  +str(y +1)  +' |'
            for x in range(self.sizeX):
                line += visual[y][x]
                thing = self.board[y][x]
                if not thing:
                    line += '.'
                    continue
                if isinstance(thing, Building):
                    line += thing.short
                    continue
                if type(thing) == str:
                    line += thing
                    continue
                raise TypeError('unsupported tile occupant type found.')
            print(line)
    
    def showActionsRemaining(self):
        line = 'actions remaining: '
        for event in self.actionsRemaining:
            line += event.short
        print(line)
    
    def showAll(self):
        print('Round ' +str(self.round) +'.')
        self.showBoard()
        self.showActionsRemaining()
    
    def showUpgrades(self):
        if not self.options:
            print('no upgrades are currently available.')
            return
        raw = [[upgrade.short] +upgrade.message for upgrade in self.options]
        height = max([len(lines) for lines in raw]) -1  #subtract 1 to exclude title from vertical padding calculation
        boxes = []
        for index in range(len(raw)):
            message = raw[index]
            title = ' ' +str(index +1) +': ' +message[0] +' '
            width = max(len(title), max([len(line) for line in message[1:]]))
            header = '-' *((width -len(title)) //2) +title
            header += '-' *(width -len(header))
            box = [header]
            for y in range((height -len(message) +1) //2):
                box.append(' ' *width)
            for text in message[1:]:
                line = ' ' *((width -len(text)) //2) +text
                line += ' ' *(width -len(line))
                box.append(line)
            for y in range(height -len(box) +1):
                box.append(' ' *width)
            boxes.append(box)
        line = '+-'
        for box in boxes:
            line += box[0] +'-+-'
        print(line[:-1])
        for y in range(height):
            line = '| '
            for box in boxes:
                line += box[y +1] +' | '
            print(line[:-1])
        line = '+-'
        for box in boxes:
            line += '-' *len(box[0]) +'-+-'
        print(line[:-1])

    def replace(self, x, y, value, allowed: tuple) -> bool:
        if self.board[y][x] in allowed:
            del self.board[y][x]
            self.board[y].insert(x, value)
            self.distanceCache = {}
            return True
        return False
    
    def triggerEvents(self):
        self.actionsRemaining = []
        for event in self.deck:
            if event.automatic:
                event.play()
            else:
                self.actionsRemaining.append(event)
    
    def resolveBuildings(self):
        for y in range(self.sizeY):
            for x in range(self.sizeX):
                thing = self.board[y][x]
                if not thing:
                    continue
                if thing.checkSatisfaction() > 0:
                    continue
                coords = changeBase(str(x +1), '0123456789', 'zabcdefghijklmnopqrstuvwxy') +str(y +1)
                print(thing.short +' at ' +coords +' was unsatisfied and departed.')
                self.board[y][x] = None
                self.lives -= 1
                print('lives remaining: ' +str(self.lives))
                self.marks[y] = self.marks[y][:x] +'>' +self.marks[y][x +1:]

    def addContent(self):
        if self.round %3 == 2:
            self.addPack()
        #TODO add different content on other modulos of 3

    def addPack(self):
        total = 0
        for pack in self.packs:
            total += pack['weight'] *(1 -pack['avoid'])
        index = random.random() *total
        choice = self.packs[-1]
        for pack in self.packs:
            index -= pack['weight'] *(1 -pack['avoid'])
            if index <= 0:
                choice = pack
                break
        for thing in pack['content']:
            self.deck.append(thing(self))
        for pack in self.packs:
            pack['avoid'] *= .5
        choice['avoid'] = 1

    def nextRound(self):
        #TODO maybe check if has actions or options remaining
        self.distanceCache = {}
        self.resolveBuildings()
        self.round += 1
        self.addContent()
        self.triggerEvents()
        self.showAll()
        #TODO choice of new acions in deck or single use actions.
    
    def handleInput(self, inp: list):
        '''handles all inputs given. this method is VERY long, fold all lines except for commands you want to view.'''
        if False in [type(i) == str for i in inp]:
            raise TypeError('all items in input list must be of type string.')
        if inp in ([], ['']):  #empty input, show basic info
            self.showAll()
            return
        for event in self.actionsRemaining:  #play action
            if inp[0] == event.short:
                if event.handleInput(inp[1:]):
                    self.actionsRemaining.remove(event)
                    if self.actionsRemaining == []:
                        self.nextRound()
                #DECIDE maybe print actions remaining
                return
        if inp[0] in ('end', 'endturn', 'next'):
            self.nextRound()
            return
        x, y, error = newDecodeCoords(inp[0], self)
        if not error:  #point at coord
            self.marks[y] = '-' *self.sizeX
            for row in range(self.sizeY):
                self.marks[row] = self.marks[row][:x] +'|' +self.marks[row][x +1:]
            self.marks[y] = self.marks[y][:x] +'>' +self.marks[y][x +1:]
            self.showBoard()
            return
        if inp[0] in ('options', 'upgrades'):
            self.showUpgrades()
            return
        if inp[0] in ('f', 'flag', 'm', 'mark'):
            if len(inp) < 2:
                print('enter coordinate you want to flag or unflag, and optionally the name of the flag, or clear to clear.')
                return
            if inp[1] in ('c', 'clr', 'clear', 'r', 'reset'):
                self.flags = [' ' *self.sizeX for y in range(self.sizeY)]
                return
            x, y, success = decodeCoords(inp[1])
            if not success:
                return
            x -= 1  #offset cuz board pos 0,0 is labled as 1,1
            y -= 1
            if not(0 <= x < self.sizeX and 0 <= y < self.sizeY):
                print('coordinates are outside of board.')
                return
            if len(inp) > 2:
                inp[2] += ' '
                self.flags[y] = self.flags[y][:x] +inp[2][0] +self.flags[y][x +1:]
                return
            if self.flags[y][x] == ' ':
                self.flags[y] = self.flags[y][:x] +'F' +self.flags[y][x +1:]
                return
            self.flags[y] = self.flags[y][:x] +' ' +self.flags[y][x +1:]
            return
        if inp[0] in ('d', 'dist', 'test', 'view'):
            if len(inp) < 2:

                #show all dist of all Houses to its Resource
                for y in range(self.sizeY):
                    for x in range(self.sizeX):
                        thing = self.board[y][x]
                        if not thing:
                            continue
                        #REPLACE proper check for if thing can be satisfied
                        if not hasattr(thing, 'generateDistanceBoard'):
                            continue
                        if thing.short not in self.distanceCache:
                            self.distanceCache[thing.short] = thing.generateDistanceBoard()
                        self.marks[y] = self.marks[y][:x] +str(self.distanceCache[thing.short][y][x])[-1] +self.marks[y][x +1:]
                self.showBoard()
                #TODO print wether any House not satisfied
                return
            
            #find input House on board
            thing = None
            for y in range(self.sizeY):
                for x in range(self.sizeX):
                    if not self.board[y][x]:
                        continue
                    if self.board[y][x].short == inp[1]:
                        thing = self.board[y][x]
                        break
                else:
                    continue
                break
            if not thing:
                print('house not found on board, enter house or nothing to show distances.')
                return
            
            #show distances to House for each tile
            if thing.short not in self.distanceCache:
                self.distanceCache[thing.short] = thing.generateDistanceBoard()
            self.marks = ['' for y in range(self.sizeY)]
            for y in range(self.sizeY):
                for x in range(self.sizeX):
                    self.marks[y] += str(self.distanceCache[thing.short][y][x])[-1]
            self.showBoard()
            #TODO print wether any House not satisfied
            return
        if inp[0] in ('status', 'sta', 'lives', 'deck', 'round', 'turn'):
            print('Round ' +str(self.round) +'.')
            print('lives remaining: ' +str(self.lives))
            line = 'deck: '
            for event in self.deck:
                line += event.short
            print(line)
            return
        if inp[0] in ('h', 'help'):
            #TODO make default help and detailed help if input command given
            print('sorry i didnt make the help message yet.')
            return
        if inp[0] == 'debug' and allowDebug:
            if inp[1] == 'lives':
                try:
                    self.lives = int(inp[2])
                except (IndexError, ValueError):
                    print('enter valid number to set lives to.')
                return
            #TODO add more debug tools: change board, change deck, change events, trigger input events
            print('didnt recognise debug tool.')
            return
        for event in self.deck:  #action already used
            if inp[0] == event.short:
                if event.automatic:
                    print('that action plays automatically on round start.')
                else:
                    print('you already used that action.')
                return
        #TODO handle more inputs: place Building, remove Building, add Playable, remove Playable, help, new game, status game inventory
        print('input not recognised, input help for a list of all inputs.')



class Building:
    def __init__(self, game, posX, posY):
        self.game = game
        self.posX = posX
        self.posY = posY
        self.blocksPath = True
        self.short = '*'

    def checkSatisfaction(self) -> int:
        '''child House classes should replace this method, postive values are good and negative values and zero are bad.'''
        return 9

class GroceriesHouse(Building):
    def __init__(self, game, posX, posY):
        super().__init__(game, posX, posY)
        self.short = 'g'
        self.resource = GroceriesResource
    
    def generateDistanceBoard(self):
        bx = self.game.sizeX
        by = self.game.sizeY
        dists = [[9 for x in range(bx)] for y in range(by)]
        active = []

        #look for wanted Resources
        for y in range(by):
            for x in range(bx):
                if isinstance(self.game.board[y][x], self.resource):
                    dists[y][x] = 0
                    active.append((x, y))
        
        index = 0
        while index < len(active):
            x, y = active[index]
            pathDist = dists[y][x] +1
            for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):

                #distance to adjacent tile
                if not(0 <= x +dx < bx and 0 <= y +dy < by):
                    continue
                if dists[y +dy][x +dx] <= pathDist:
                    continue
                dists[y +dy][x +dx] = pathDist

                #also check adjacent tile if not blocking path
                if (x +dx, y +dy) in active[index:]:
                    continue
                if not self.game.board[y +dy][x +dx]:
                    active.append((x +dx, y +dy))
                    continue
                if self.game.board[y +dy][x +dx].blocksPath:
                    continue
                active.append((x +dx, y +dy))

            index += 1
        return dists

    def checkSatisfaction(self) -> int:
        if self.short not in self.game.distanceCache:
            self.game.distanceCache[self.short] = self.generateDistanceBoard()
        return 6 -self.game.distanceCache[self.short][self.posY][self.posX]

class GroceriesResource(Building):
    def __init__(self, game, posX, posY):
        super().__init__(game, posX, posY)
        self.short = 'G'

class StreetBuilding(Building):
    def __init__(self, game, posX, posY):
        super().__init__(game, posX, posY)
        self.short = '_'
        self.blocksPath = False

class CornerHouse(Building):
    def __init__(self, game, posX, posY):
        super().__init__(game, posX, posY)
        self.short = 'c'
        self.resource = CornerResource
    
    def generateDistanceBoard(self):
        bx = self.game.sizeX
        by = self.game.sizeY
        dists = [[9 for x in range(bx)] for y in range(by)]
        active = []

        #look for wanted Resources
        for y in range(by):
            for x in range(bx):
                if isinstance(self.game.board[y][x], self.resource):
                    dists[y][x] = 0
                    active.append((x, y))
        
        index = 0
        while index < len(active):
            x, y = active[index]
            pathDist = dists[y][x] +1

            #walk in each direction
            for rx, ry in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                dx = 0
                dy = 0
                while True:
                    dx += rx
                    dy += ry
                    if not(0 <= x +dx < bx and 0 <= y +dy < by):
                        break
                    if pathDist > dists[y +dy][x +dx]:
                        break
                    dists[y +dy][x +dx] = pathDist
                    if (x +dx, y +dy) in active[index:]:
                        continue
                    if not self.game.board[y +dy][x +dx]:
                        active.append((x +dx, y +dy))
                        continue
                    if self.game.board[y +dy][x +dx].blocksPath:
                        break
                    active.append((x +dx, y +dy))
            
            index += 1
        return dists

    def checkSatisfaction(self) -> int:
        if self.short not in self.game.distanceCache:
            self.game.distanceCache[self.short] = self.generateDistanceBoard()
        return 3 -self.game.distanceCache[self.short][self.posY][self.posX]

class CornerResource(Building):
    def __init__(self, game, posX, posY):
        super().__init__(game, posX, posY)
        self.short = 'C'

class MansionHouse(Building):
    def __init__(self, game, posX, posY):
        super().__init__(game, posX, posY)
        self.short = 'm'
    
    def calculateSight(self, atX, atY):
        sight = 0
        for vec in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            dist = 0
            while True:
                dist += 1
                x = atX +vec[0] *dist
                y = atY +vec[1] *dist
                if not(0 <= x < self.game.sizeX and 0 <= y < self.game.sizeY):
                    break
                if not self.game.board[y][x]:
                    continue
                if self.game.board[y][x].blocksPath:
                    break
            sight += dist -1
        return sight
    
    def generateDistanceBoard(self):
        return [[min(max(self.calculateSight(x, y), 0), 9) for x in range(self.game.sizeX)] for y in range(self.game.sizeY)]

    def checkSatisfaction(self) -> int:
        return self.calculateSight(self.posX, self.posY) -8



class Playable:
    def __init__(self, game):
        self.game = game
        self.placeResult = Building
        self.short = '*'
        self.automatic = False
    
    def play(self):
        #REPLACE make method better by selecting random of available tiles instead
        for n in range(100):
            x = random.randrange(0, self.game.sizeX)
            y = random.randrange(0, self.game.sizeY)
            if self.game.replace(x, y, self.placeResult(self.game, x, y), (None, )):
                self.game.marks[y] = self.game.marks[y][:x] +'>' +self.game.marks[y][x +1:]
                return
        print(self.short +' could not find an empty property and decided not to move in.')
    
    def handleInput(self, inp: list) -> bool:
        '''most child classes do not replace this method as most child classes are this simple placement.'''
        if len(inp) == 0:
            print('enter coordinate where you want to place ' +self.short +'.')
            return False
        x, y, success = decodeCoords(inp[0])
        if not success:
            return False
        x -= 1  #offset cuz board pos 0,0 is labled as 1,1
        y -= 1
        if not(0 <= x < self.game.sizeX and 0 <= y < self.game.sizeY):
            print('coordinates are outside of board.')
            return False
        if not self.game.replace(x, y, self.placeResult(self.game, x, y), (None, )):
            #REPLACE not important, show coords with proper syntax
            print(inp[0] +' is already occupied.')
            return False
        return True

class GroceriesEvent(Playable):
    def __init__(self, game):
        super().__init__(game)
        self.placeResult = GroceriesHouse
        self.short = 'g'
        self.automatic = True

class GroceriesAction(Playable):
    def __init__(self, game):
        super().__init__(game)
        self.placeResult = GroceriesResource
        self.short = 'G'

class StreetAction(Playable):
    def __init__(self, game):
        super().__init__(game)
        self.placeResult = StreetBuilding
        self.short = '_'

class CornerEvent(Playable):
    def __init__(self, game):
        super().__init__(game)
        self.placeResult = CornerHouse
        self.short = 'c'
        self.automatic = True

class CornerAction(Playable):
    def __init__(self, game):
        super().__init__(game)
        self.placeResult = CornerResource
        self.short = 'C'

class MansionEvent(Playable):
    def __init__(self, game):
        super().__init__(game)
        self.placeResult = MansionHouse
        self.short = 'm'
        self.automatic = True



class Option:
    def __init__(self, game):
        self.game = game
        self.short = 'base class'
        self.message = ['parent default Option', 'this should never appear']

class StreetOption(Option):
    def __init__(self, game):
        super().__init__(game)
        self.short = 'Street'
        self.message = ['adds one _', 'to your deck.']

class GroceriesOption(Option):
    def __init__(self, game):
        super().__init__(game)
        self.short = 'temporary'
        self.message = ['this message', 'is temporary.', 'this is for testing', 'the code for showing', 'very very very long messages.']



if __name__ == '__main__':
    allowDebug = True  #REPLACE to false when exporting
    import random
    print('Welcome to Metropolis, the deck builder city builder.')
    main()
