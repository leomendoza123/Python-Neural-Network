def dbconnector ():
    f = open('NumbersDB', 'r')
    db = f.readline().split('\n')[0].split(' ')
    databaseSize = int(db[0])
    database = []
    f.readline()

    for element in range (databaseSize) :
        
        f.readline()
        f.readline()
        inputElement  =  map(int,f.readline().split('\n')[0].split(' '))
        print len(inputElement)
        f.readline()
        outputElement =   map(int,f.readline().split('\n')[0].split(' '))
        print len(outputElement)
        f.readline()

        database.append ([inputElement, outputElement])

    return database
