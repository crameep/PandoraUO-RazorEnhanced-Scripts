# original from Alexdan on bitbucket
# Generalized and cleaned up a bit by Chickenpekah
import sys
if not Misc.CurrentScriptDirectory() in sys.path:
    sys.path.append(Misc.CurrentScriptDirectory())


class runeBook():
    # If useChiv is non-zero, runeIndexList is updated
    # to use the chiv buttons
    def __init__(self, serl, gump, useChiv=0):
        self.delay = \
        {
            'base' : 500,
            'drag' : 600,
        }

        self.defaultLocList = \
        {
            '1': 4, '2': 10, '3': 16, '4': 22,
            '5': 28, '6': 34, '7': 40, '8': 46,
            '9': 52, '10': 58, '11': 64, '12': 70,
            '13': 76, '14': 82, '15': 88, '16': 94
        }

        self.runeIndexList = \
        {
            '1': 5, '2': 11, '3': 17, '4': 23,
            '5': 29, '6': 35, '7': 41, '8': 47,
            '9': 53, '10': 59, '11': 65, '12': 71,
            '13': 77, '14': 83, '15': 89, '16': 95
        }

        if serl == None or gump == None:
            throw("Invalid parameters given to runeBook")

        self.bookSerial = serl
        self.gump = gump
        self.empties = 0
        if useChiv:
            for key in self.runeIndexList.keys():
                self.runeIndexList[key] += 2

    def doRecall(self, bookIndex):
        currentX = Player.Position.X
        currentY = Player.Position.Y
        Items.UseItem(self.bookSerial)
        Gumps.WaitForGump(self.gump, 10000)
        Gumps.SendAction(self.gump, bookIndex)
        return self.checkPositionChanged(currentX, currentY, True)

    #--------------------------------------------------------------------
    #member function:   recall
    #author:            Epoch
    #parameters:        a rune index (as a string)
    #returns:           "blocked" = rune is blocked
    #                   "mana" = not enough mana to recall
    #                   "success" = successfully recalled
    #purpose:           recall to a location given an index
    #--------------------------------------------------------------------        
    def recall(self, runeIndex):
        Misc.SendMessage("attempting to recall to rune index: " +
                str(self.runeIndexList[runeIndex]), 70)
        return self.doRecall(self.runeIndexList[runeIndex])
            
    #--------------------------------------------------------------------
    #member function:   setDefault
    #author:            Epoch
    #parameters:        a rune index
    #returns:           Nothing
    #purpose:           set a rune as defualt location given a rune index
    #--------------------------------------------------------------------        
    def setDefault(self, defaultIndex):
        Items.UseItem(self.bookSerial)
        Gumps.WaitForGump(self.gump, 10000)
        Gumps.SendAction(self.gump, self.defaultLocList[defaultIndex])

    #--------------------------------------------------------------------
    #member function:   checkPositionChanged
    #author:            Epoch
    #parameters:        character position X and character position Y
    #returns:           "blocked" = rune is blocked
    #                   "mana" = not enough mana to recall
    #                   "success" = successfully recalled
    #purpose:           waits for character position to change
    #                   or for "blocked" or "mana" to be in journal
    #--------------------------------------------------------------------           
    def checkPositionChanged(self, posX, posY, noise=False):
        recallStatus = None
        while Player.Position.X == posX and Player.Position.Y == posY:
            if Journal.Search("blocked"):
                Journal.Clear()
                if noise:
                    Misc.SendMessage("Rune Blocked", 100)
                recallStatus = "blocked"
                return recallStatus
            elif Journal.Search("mana"):
                Journal.Clear()
                if noise:
                    Misc.SendMessage("out of mana", 100)
                recallStatus = "mana"
            else:
                recallStatus = "good"

        return recallStatus
        
    #--------------------------------------------------------------------
    #member function:   moveRuneToBook
    #author:            Epoch
    #parameters:        serial for a rune
    #returns:           True or False depending on success
    #purpose:           moves a rune to this book
    #--------------------------------------------------------------------        
    def moveRuneToBook(self, runeSrl):
        if self.getEmpty() != 0:
            #move a rune to the book
            rne = Items.FindBySerial(runeSrl)
            Items.Move(rne, self.bookSerial, 1)
            Misc.Pause(self.delay['drag'])
            return True
        else:
            Misc.SendMessage("runeBook full", 100)
            return False
    
    #--------------------------------------------------------------------
    #member function:   getEmpty
    #author:            Epoch
    #parameters:        none
    #returns:           number of empty rune spots in book
    #purpose:           used to determine if we can fit a new rune in book
    #-------------------------------------------------------------------- 
    def getEmpty(self):
        tempEmpty = 0
        Items.UseItem(self.bookSerial)
        Gumps.WaitForGump(self.gump, 10000)
        Misc.Pause(500)
        totalLines = Gumps.LastGumpGetLineList()
        for line in totalLines:
            if "Empty" in line:
                tempEmpty += 1        
        self.empties = tempEmpty / 2
        #close the book
        Gumps.SendAction(self.gump, 0)
        return self.empties
    

    #--------------------------------------------------------------------
    #member function:   recallFromBook
    #author:            Epoch
    #parameters:        None
    #returns:           "blocked" = rune is blocked
    #                   "mana" = not enough mana to recall
    #                   "success" = successfully recalled
    #purpose:           recall directly off of the book (no rune index)
    #--------------------------------------------------------------------
    def recallFromBook(self):
        Spells.CastMagery("Recall")
        currentX = Player.Position.X
        currentY = Player.Position.Y
        Target.WaitForTarget(15000, True)
        Target.TargetExecute(self.bookSerial)
        return self.checkPositionChanged(currentX, currentY, True)

     def MasterBook(serial, book, rune, spell="R"):
        nbook = book + 1
        baseRune = 0
        if spell == 'R':  # recall
            baseRune = 5
        elif spell == 'G':   # gate
            baseRune = 6
        elif spell == 'S':   # sacred journey
            baseRune = 7
        else:
            Misc.SendMessage("Spell should be one of R, G or S, quitting", 4095)
            return

        newrune = (rune - 1) * 6 + baseRune
        Mbook = Items.FindByID(serial, -1, Player.Backpack.Serial)
        Items.UseItem(Mbook)
        Gumps.WaitForGump(354527139, 10000)
        Gumps.SendAction(354527139, nbook)
        Gumps.WaitForGump(128397316, 10000)
        Gumps.SendAction(128397316, newrune)

"""
#=======================================================================
#Just some examples of how to use the class:        
Journal.Clear()
#-------------------------create runebook object------------------------
testBook = runeBook(myRuneBookSerial, yourShardGumpIdForRunebooks)
#----------------figure out how many times "Empty" occurs---------------
rBookSpace = testBook.getEmpty()
Misc.SendMessage(rBookSpace, 200)
#------------------------Move a rune to this book-----------------------
if not testBook.moveRuneToBook(0x401F7338):
    Misc.SendMessage("couldnt add rune to book", 70)
    #do whatever... the runebook is full
else:
    #do whatever... the rune was placed in the book.
    Misc.SendMessage("success!!!! rune placed in book", 70)
    #might to call populateRunesList to update the runes list
    space = testBook.getEmpty()
    Misc.SendMessage(space, 70)    
#----------------------------recall to places---------------------------
testBook.recall('1')
testBook.recall('2')
testBook.recall('3')
#----------set default location and then recall off of the book---------
testBook.setDefault('9')
testBook.recallFromBook()
"""
wc = Misc.ReadSharedValue("charconstants")
from Scripts import hoboconstants as hc
rb = runeBook(hc.mRunebook, hc.mRunebookGumpId, True)
rb.recall('1')

