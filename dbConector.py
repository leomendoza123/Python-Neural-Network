import numpy as np
from nn import *

def dbconnector (name):
    f = open(name, 'r')
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


def dbsaveWeights (self, outputFileName):
    

    f = open(outputFileName, 'w')


    f.write (str(self.ci))
    f.write (str ('\n') )
    f.write (str(self.wi))
    
    f.write (str ('\n') )
    f.write ( str(self.wo))
    f.write (str ('\n') )
    f.write (str(self.co) )
    f.write (str ('\n') )


    print ('NN saved')


def dbloadWeights (self, FileName):
    

    f = open(FileName, 'r')

    ci = np.matrix(f.readline())
    self.ci = makeMatrix (ci.shape[0],ci.shape[1],0)
    print ci.shape
    ##fillMatrix (self.ci, ci)

    wi = np.matrix(f.readline())
    self.wi = makeMatrix (wi.shape[0],ci.shape[1],0)
    ##fillMatrix (self.wi, wi)

    wo = np.matrix(f.readline())
    self.wo = makeMatrix (wo.shape[0],ci.shape[1],0)
    ##fillMatrix (self.wo, wo)

    co = np.matrix(f.readline())
    self.co = makeMatrix (co.shape[0],co.shape[1],0)
    ##fillMatrix (self.co, co)

    print ci.shape
    print wi.shape
    print wo.shape
    print co.shape



def fillMatrix(matrix, numpyMatrix):
    for k in range(len(matrix[0])):
        
        for j in range(len(matrix[0])):
                matrix[k][j] = numpyMatrix.item((k, j))



