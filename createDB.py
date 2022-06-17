import csv, sqlite3, os 

conn = sqlite3.connect("imdbDB.db")
curs = conn.cursor()

def defaultInsert(row,tableName):
    toExecute = """INSERT INTO """+tableName+""" VALUES ("""+("?,"*len(list(row)))[:-1]+")"
    curs.execute(toExecute,row)

def crewInsert(row,tableName="crew"):
    if list(row)[1]!='\\N':
        directors = list(row)[1].split(',')
        for director in directors:
            toExecute = f"""INSERT INTO crew VALUES (?,?,?)"""
            curs.execute(toExecute,[list(row)[0],director,'director'])
    if list(row)[2]!='\\N':
        writers = list(row)[2].split(',')
        for writer in writers:
            toExecute = f"""INSERT INTO crew VALUES (?,?,?)"""
            curs.execute(toExecute,[list(row)[0],writer,'writer'])


def namesInsert(row,tableName="namesBasics"):
    professions = list(row)[4].split(',')
    titles = list(row)[5].split(',')
    for profession in professions:
        for title in titles:
            toExecute = f"""INSERT INTO {tableName} VALUES (?,?,?,?,?,?)"""
            curs.execute(toExecute,list(row)[:4]+[profession,title])





names = ["nameBasics.tsv",
"akas.tsv",
"basics.tsv",
"crew.tsv",
"episode.tsv",
"principals.tsv",
"ratings.tsv"]


#if i dont do this the database is like 50gigs
maxEntries = 10e4
#iterate through every tsv file
for file in names:
    tsvFile = open("data\\"+file,encoding="utf8")
    readTsv = csv.reader(tsvFile,delimiter='\t')
    #insert data of tsv file into new db
    #https://www.adamsmith.haus/python/answers/how-to-insert-the-contents-of-a-csv-file-into-an-sqlite3-database-in-python
    row = next(readTsv)
    ######
    tableName = file.__str__()[:file.__str__().find('.')]
    tableKey = '('+",".join(row)+')'
    if tableName=="crew":
        tableKey="(id,p,profession)"
    if tableName == "nameBasics":
        tableKey = "(nconst,primaryName,birthYear,deathYear,profession,title)"
    toExecute = """CREATE TABLE IF NOT EXISTS """+tableName+" "+tableKey
    curs.execute(toExecute)
    row = next(readTsv)
    i=0
    while row:
        if i>maxEntries:
            break
        if tableName!="crew" and tableName!="nameBasics":
            defaultInsert(row,tableName)
        else:
            if tableName=="crew":
                crewInsert(row,tableName)
            else:
                namesInsert(row,tableName)
        row=next(readTsv)
        i+=1  
conn.commit()
