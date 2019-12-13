import sqlite3 as sql
import os.path
from Deck import Rank, Suit

#region Database attribute variables
name = "name"
columns = "columns"

databaseFile = 'CardGamesDatabase.db'
cardTable = {
    name: "Cards", 
    columns: ["Id", "Rank", "Suit", "Value"]
}
deckTable = {
    name: "Decks",
    columns: ["DeckId", "CardId", "HasBeenDrawn", "PlayerId"]
}
gameTable = {
    name: "Games",
    columns: ["Id", "Type", "DeckId"]    
}
playerTable = {
    name: "Players",
    columns: ["PLayerId", "GameId", "UserName"]
}
#endregion

#region Database build scripts
def buildDatabase():
    connection = sql.connect()
    cursor = connection.cursor()

    if not tableExists(cardTable[name], cursor):
        buildCards(cursor, connection)
    if not tableExists(deckTable[name], cursor):
        buildDecks(cursor, connection)
    if not tableExists(gameTable[name], cursor):
        buildGames(cursor, connection)
    if not tableExists(playerTable[name], cursor):
        buildPlayers(cursor, connection)
    return

def buildCards(cursor, connection):
    cursor.execute('''CREATE TABLE Cards(Id INTEGER PRIMARY KEY AUTOINCREMENT,
                                         Rank TEXT,
                                         Suit TEXT,
                                         Value INTEGER)''')
    connection.commit()

    for suit in Suit:
            for rank in Rank:
                cursor.execute('''INSERT INTO ? VALUES (?,?,?,?)''')
    return

def buildDecks(cursor, connection):
    cursor.execute('''CREATE TABLE Decks(DeckId INTEGER PRIMARY KEY AUTOINCREMENT,
                                         CardId INTEGER,
                                         HasBeenDrawn INTEGER,
                                         PlayerId INTEGER)''')
    return

def buildGames(cursor, connection):
    cursor.execute('''CREATE TABLE ? (? INTEGER PRIMARY KEY AUTOINCREMENT,?,?)''', gameTable[name], gameTable[columns])
    return

def buildPlayers(cursor, connection):
    cursor.execute('''CREATE TABLE ? (? INTEGER PRIMARY KEY AUTOINCREMENT,?,?)''', playerTable[name], playerTable[columns])
    return

def tableExists(table, cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='?'", table)
    return cursor.fetchone() is not None

#endregion