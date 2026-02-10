#Metropolis deck builder city builder by Lucas

#TODO:
#left off at line 
#make game baseline working
#add markers: print extra info during Game.showBoard() such as flags, pointing at coord, highlight unsatisfied houses.
#upgrade system: some rounds you can add one of 3 options to your deck, this is a command thus you can first place Resources if you want.
#change function and method names to have underscores



def main():
    #REPLACE comment out tests when exporting
    # print(int('hi'))

    startup()
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



def startup():
    print('Welcome to Metropolis, the deck builder city builder.')

def newGame():
    print('starting new game.')
    sizeX, sizeY = getBoardSize()
    game = Game(sizeX, sizeY)
    return game

def getBoardSize():
    while True:
        s = input('enter map size: ')
        #TODO allow entering custom size
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
        self.distanceCache = {}
        self.actionsRemaining = []

    def showBoard(self):
        line = '    '
        for x in range(self.sizeX):
            s = changeBase(str(x +1), '0123456789', 'zabcdefghijklmnopqrstuvwxy')
            line += ' ' *(2 -len(s))  +s
        print(line)
        print('   #'  +'##' *self.sizeX)
        for y in range(self.sizeY):
            line = ' ' *(2 -len(str(y +1)))  +str(y +1)  +' #'
            for x in range(self.sizeX):
                line += ' '  #REPLACE append markings or flags instead
                thing = self.board[y][x]
                if thing == None:
                    line += '.'
                    continue
                if type(thing) == str:
                    line += thing
                    continue
                if isinstance(thing, Building):
                    line += thing.short
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
    
    def replace(self, x, y, value, allowed: tuple) -> bool:
        if self.board[y][x] in allowed:
            del self.board[y][x]
            self.board[y].insert(x, value)
            return True
        return False
    
    def triggerEvents(self):
        self.actionsRemaining = []
        for event in self.deck:
            if event.automatic:
                event.play()
            else:
                self.actionsRemaining.append(event)
    
    def nextRound(self):
        #TODO check if has actions or options remaining
        #TODO check all buildings
        self.round += 1
        #TODO add new random events
        self.distanceCache = {}
        self.triggerEvents()
        self.showAll()
        #TODO choice of new acions in deck or single use actions.
    
    def handleInput(self, inp: list):
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
        if inp[0] in ('quit', '!q', ':q', 'exit'):
            exit()
        if inp[0] in ('h', 'help'):
            #TODO make default help and detailed help if input command given
            print('sorry i didnt make the help message yet.')
            return
        if inp[0] in ('status', 'sta', 'lives', 'deck', 'round', 'turn'):
            print('Round ' +str(self.round) +'.')
            print('lives remaining: ' +str(self.lives))
            line = 'deck: '
            for event in self.deck:
                line += event.short
            print(line)
            return
        if inp[0] in ('end', 'endturn', 'next'):
            self.nextRound()
            return
        if inp[0] == 'debug' and allowDebug:
            if inp[1] == 'lives':
                try:
                    self.lives = int(inp[2])
                except (IndexError, ValueError):
                    print('enter valid number to set lives to.')
                return
            if inp[1] == 'dist':
                #REPLACE rewrite this command to accept short name of a building and check all installed buildings
                pass
            #TODO add more debug tools: change board, change deck, change events, trigger input events
            print('didnt recognise debug tool.')
            return
        for event in self.deck:
            if inp[0] == event.short:
                print('you already used that action.')
                return
        #TODO handle more inputs: help, new game, point coord, flag coord, test houses and display, status game inventory
        print('input not recognised, input help for a list of all inputs.')



class Building:
    def __init__(self, game, posX, posY):
        self.game = game
        self.posX = posX
        self.posY = posY
        self.short = '*'

    def depart(self):
        self.game.board[self.posY][self.posX] = None
        del self
    
    def generateDistanceBoard(self):
        '''child classes should replace this and calculate a board of numbers showing how far away this building is from its resource.'''
        return [[0 for x in range(self.game.sizeX)] for y in range(self.game.sizeY)]

    def checkSatisfaction(self) -> None:
        '''child classes MUST extend this method to return a number, where postive values and zero are good and negative values are bad.'''
        if self.short not in self.game.distanceCache:
            self.game.distanceCache[self.short] = self.generateDistanceBoard()


class GroceriesHouse(Building):
    def __init__(self, game, posX, posY):
        super().__init__(game, posX, posY)
        self.short = 'g'
    
    def generateDistanceBoard(self):
        bx = self.game.sizeX
        by = self.game.sizeY
        dists = [[999 for x in range(bx)] for y in range(by)]
        active = []
        for y in range(by):
            for x in range(bx):
                if self.game.board[y][x] == self.resource:
                    dists[y][x] = 0
                    active.append((x, y))
        index = 0
        while index < len(active):
            x, y = active[index]
            pathDist = dists[y][x] +1
            for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                if not(0 <= x +dx < bx and 0 <= y +dy < by):
                    continue
                if dists[y +dy][x +dx] <= pathDist:
                    continue
                dists[y +dy][x +dx] = pathDist
                if self.game.board[y +dy][x +dx] in (None, StreetBuilding) and (x +dx, y +dy) not in active[index:]:
                    active.append((x +dx, y +dy))
            index += 1
        return dists

    def checkSatisfaction(self) -> float:
        super().checkSatisfaction()
        return 6 -self.game.distanceCache[self.short][self.posY][self.posX]


class GroceriesResource(Building):
    def __init__(self, game, posX, posY):
        super().__init__(game, posX, posY)
        self.short = 'G'


class StreetBuilding(Building):
    def __init__(self, game, posX, posY):
        super().__init__(game, posX, posY)
        self.short = '_'



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



if __name__ == '__main__':
    allowDebug = True  #REPLACE to false when exporting
    import random
    main()
