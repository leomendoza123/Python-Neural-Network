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

    f.write (str(len(self.ci)) + ' ' + str(len(self.ci[0])) + '\n')
    f.write (str(self.ci))
    f.write (str ('\n') )
    f.write (str(self.wi))
    f.write (str ('\n') )

    f.write (str(len(self.co)) + ' ' + str(len(self.co[0])) + '\n')
    
    f.write ( str(self.wo))
    f.write (str ('\n') )
    f.write (str(self.co) )
    f.write (str ('\n') )


    print ('NN saved')


def dbloadWeights (self, FileName):
    

    f = open(FileName, 'r')

   
    heigh_width = f.readline().split('\n')[0].split(' ')
    ci = np.matrix(f.readline())
    self.ci = makeMatrix (int(heigh_width[0]),int(heigh_width[1]),0)
    fillMatrix (self.ci, ci, heigh_width[0], heigh_width[1])

    wi = np.matrix(f.readline())
    self.wi = makeMatrix (int(heigh_width[0]),int(heigh_width[1]),0)
    fillMatrix (self.wi, wi, heigh_width[0], heigh_width[1])


    heigh_width = f.readline().split('\n')[0].split(' ')

    wo = np.matrix(f.readline())
    self.wo = makeMatrix (int(heigh_width[0]),int(heigh_width[1]),0)
    fillMatrix (self.wo, wo, heigh_width[0], heigh_width[1])
    
    co = np.matrix(f.readline())
    
    self.co = makeMatrix (int(heigh_width[0]),int(heigh_width[1]),0)
    fillMatrix (self.co, co, heigh_width[0], heigh_width[1])

    ##print ci.shape
    #print wi.shape
    #print wo.shape
    print co.shape



def fillMatrix(matrix, numpyMatrix, sizeX, sizeY):
    for k in range(int(sizeX)):
    
                matrix[int(sizeX)/int(sizeY)][k%int(sizeY)] = numpyMatrix.item((0, k))



