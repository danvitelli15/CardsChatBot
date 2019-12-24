import sqlite3 as sql
import os.path
from .Deck import Rank, Suit
from _sqlite3 import IntegrityError

#region Database attribute variables
name = "name"
columns = "columns"
blanks = "blanks"

databaseFile = 'CardGamesDatabase.db'
cardTable = {
    name: "Cards",
    columns: ["Rank", "Suit", "Value"],
    blanks: "?,?,?"
}
deckTable = {
    name: "Decks",
    columns: "DeckId, CardId, HasBeenDrawn, PlayerId",
    blanks: "?,?,?,?"
}
gameTable = {
    name: "Games",
    columns: ["Type", "DeckId"],
    blanks: "?,?"
}
playerTable = {
    name: "Players",
    columns: ["UserName"],
    blanks: "?"
}
playerGameXRefTable = {
    name: "PlayerGameXRef",
    columns: ["PlayerId", "GameId", "Money"],
    blanks: "?,?,?"
}
#endregion

#region Card actions
def getCards():
    connection = sql.connect(databaseFile)
    cursor = connection.cursor()
    cursor.execute('SELECT CardId FROM Cards')
    cards = cursor.fetchall()
    connection.close()
    return cards

def getCardId(rank, suit):
    connection = sql.connect(databaseFile)
    cursor = connection.cursor()
    cursor.execute(f'SELECT Id FROM {cardTable[name]} WHERE Rank=? AND Suit=?', (rank, suit))
    cardId = cursor.fetchone()
    connection.close()
    return cardId
#endregion

#region Deck actions
def createDeck():
    deckId = determineDeckId()
    deck = list()
    cards = getCards()
    for card in cards:
        deck.append((deckId, card[0], False, None))
    print(deck)
    insertManyInto(deckTable, deck)
    return deckId

def determineDeckId():
    connection = sql.connect(databaseFile)
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT DeckId FROM Decks ORDER BY DeckId DESC')
    maxIndex = cursor.fetchone()
    connection.close()
    return 1 if maxIndex is None else maxIndex + 1

def drawCard(deckId, rank, suit, player):
    cardId = getCardId(rank, suit)
    playerId = getPlayerId(player)
    connection = sql.connect(databaseFile)
    cursor = connection.cursor()
    cursor.execute('UPDATE Decks SET HasBeenDrawn=true, PlayerId=? WHERE DeckId=? AND CardId=?', (playerId, deckId, cardId))
    connection.close()
    return
#endregion

#region Player actions
def addPlayer(username):
    return insertInto(playerTable, [username])

def getPlayerId(username):
    connection = sql.connect(databaseFile)
    cursor = connection.cursor()
    cursor.execute(f'SELECT Id FROM {playerTable[name]} WHERE UserName=?', (username,))
    playerId = cursor.fetchone()
    connection.close()
    return playerId
#endregion

#region CRUD functions
def insertInto(table, values):
    if len(table[columns]) != len(values):
        return "Error: columns and values must have the same number of elements. (columns: " + str(len(columns)) + ", values: " + str(len(values)) + ")"
    connection = sql.connect(databaseFile)
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO {table[name]}({table[columns]}) VALUES({table[blanks]})', tuple(values))
    connection.commit()
    connection.close()
    return "Success"

def insertManyInto(table, values):
    connection = sql.connect(databaseFile)
    cursor = connection.cursor()
    cursor.executemany(f'INSERT INTO {table[name]}({table[columns]}) VALUES({table[blanks]})', values)
    connection.commit()
    connection.close()
    return "Success"

def select(table, id):
    connection = sql.connect(databaseFile)
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM {table[name]} WHERE {table[name] + "Id"} = ?', (id,))
    result = cursor.fetchone()
    connection.close()
    return result
#endregion

#region Database build scripts
def buildDatabase():
    print("Building database if none exists. Checking for " + databaseFile)
    connection = sql.connect(databaseFile)
    cursor = connection.cursor()

    if not tableExists(cardTable[name], cursor):
        print("Adding Cards table to " + databaseFile)
        buildCards(cursor, connection)
    if not tableExists(playerTable[name], cursor):
        print("Adding Players table to " + databaseFile)
        buildPlayers(cursor, connection)
    if not tableExists(deckTable[name], cursor):
        print("Adding Decks table to " + databaseFile)
        buildDecks(cursor, connection) 
    if not tableExists(gameTable[name], cursor):
        print("Adding Games table to " + databaseFile)
        buildGames(cursor, connection)
    if not tableExists(playerGameXRefTable[name], cursor):
        print("Adding PlayerGameXRef to " + databaseFile)
    connection.close()
    return

def buildCards(cursor, connection):
    cursor.execute('''CREATE TABLE Cards(CardId INTEGER PRIMARY KEY AUTOINCREMENT,
                                         Rank TEXT,
                                         Suit TEXT,
                                         Value INTEGER)''')
    connection.commit()

    for suit in Suit:
            for rank in Rank:
                cursor.execute('''INSERT INTO Cards (Rank, Suit, Value) VALUES (?,?,?)''', (rank.getName(), suit.value, rank.value))
    return

def buildDecks(cursor, connection):
    cursor.execute('''CREATE TABLE Decks(DeckId INTEGER,
                                         CardId INTEGERY,
                                         HasBeenDrawn INTEGER,
                                         PlayerId INTEGER,
                                         PRIMARY KEY (DeckId, CardId),
                                         FOREIGN KEY (CardId) REFERENCES Cards(CardId),
                                         FOREIGN KEY (PlayerId) REFERENCES Players(PlayerId))''')
    connection.commit()
    return

def buildGames(cursor, connection):
    cursor.execute('''CREATE TABLE Games(GameId INTEGER PRIMARY KEY AUTOINCREMENT,
                                         Type TEXT,
                                         DeckId INTEGER,
                                         FOREIGN KEY (DeckId) REFERENCES Decks(DeckId)) 
                                        ''')
    connection.commit()
    return

def buildPlayers(cursor, connection):
    cursor.execute('''CREATE TABLE Players (PlayerId INTEGER PRIMARY KEY AUTOINCREMENT,
                                            UserName TEXT UNIQUE)''')
    connection.commit()
    return

def buildPlayerGameXRef(cursor, connection):
    cursor.execute('''CREATE TABLE PlayerGameXRef(PlayerId INTEGER,
                                                  GameId INTEGER,
                                                  Money FLOAT,
                                                  FOREIGN KEY (PlayerId) REFERENCES Players(PlayerId),
                                                  FOREIGN KEY (GameId) REFERENCES Games(GameId))''')
    connection.commit()
    return

def tableExists(table, cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
    return cursor.fetchone() is not None

#endregion