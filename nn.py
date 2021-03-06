import math
import random
from dbConector import *

random.seed(0)


def rand(a, b):
    return (b-a)*random.random() + a


def makeMatrix(I, J, fill=0.0):
    m = []
    for i in range(I):
        m.append([fill]*J)
    return m


def sigmoid(x):
    return math.tanh(x)


def dsigmoid(y):
    return 1.0 - y**2

    

class NN:
    def __init__(self, ni, nh, no, regression = False, NNcurrentWeights = ''):
        """NN constructor.
        
        ni, nh, no are the number of input, hidden and output nodes.
        """

        self.regression = regression
        
        #Number of input, hidden and output nodes.
        self.ni = ni  + 1 # +1 for bias node
        self.nh = nh  + 1 # +1 for bias node
        self.no = no

        # activations for nodes
        self.ai = [1.0]*self.ni
        self.ah = [1.0]*self.nh
        self.ao = [1.0]*self.no


        
        # create weights
        self.wi = makeMatrix(self.ni, self.nh)
        self.wo = makeMatrix(self.nh, self.no)
        
        # set them to random vaules
        for i in range(self.ni):
            for j in range(self.nh):
                self.wi[i][j] = rand(-1, 1)
        for j in range(self.nh):
            for k in range(self.no):
                self.wo[j][k] = rand(-1, 1)

        if NNcurrentWeights != '':
            dbloadWeights(self, NNcurrentWeights)



        # last change in weights for momentum   
        self.ci = makeMatrix(self.ni, self.nh)
        self.co = makeMatrix(self.nh, self.no)


    def update(self, inputs):
	##print (len(inputs), self.ni-1)
        if len(inputs) != self.ni-1:
            raise ValueError, 'wrong number of inputs'

        # input activations
        for i in range(self.ni - 1):
            self.ai[i] = inputs[i]

        # hidden activations
        for j in range(self.nh - 1):
            total = 0.0
            for i in range(self.ni):
                total += self.ai[i] * self.wi[i][j]
            self.ah[j] = sigmoid(total)

        # output activations
        for k in range(self.no):
            total = 0.0
            for j in range(self.nh):
                total += self.ah[j] * self.wo[j][k]
            self.ao[k] = total
            if not self.regression:
                self.ao[k] = sigmoid(total)
            
        
        return self.ao[:]


    def backPropagate(self, targets, N, M):
        if len(targets) != self.no:
            raise ValueError, 'wrong number of target values'

        # calculate error terms for output
        output_deltas = [0.0] * self.no
        for k in range(self.no):
            output_deltas[k] = targets[k] - self.ao[k]
            if not self.regression:
                output_deltas[k] = dsigmoid(self.ao[k]) * output_deltas[k]

        
        # calculate error terms for hidden
        hidden_deltas = [0.0] * self.nh
        for j in range(self.nh):
            error = 0.0
            for k in range(self.no):
                error += output_deltas[k]*self.wo[j][k]
            hidden_deltas[j] = dsigmoid(self.ah[j]) * error

        # update output weights
        for j in range(self.nh):
            for k in range(self.no):
                change = output_deltas[k]*self.ah[j]
                self.wo[j][k] = self.wo[j][k] + N*change + M*self.co[j][k]
                self.co[j][k] = change

        # update input weights
        for i in range(self.ni):
            for j in range(self.nh):
                change = hidden_deltas[j]*self.ai[i]
                self.wi[i][j] = self.wi[i][j] + N*change + M*self.ci[i][j]
                self.ci[i][j] = change

        # calculate error
        error = 0.0
        for k in range(len(targets)):
            error += 0.5*((targets[k]-self.ao[k])**2)
        return error

    @staticmethod
    def test( NNfileName, patternsfileName, verbose = False):


	fileLoaded = dbconnector(patternsfileName)
	patterns = fileLoaded[0]
	databaseInfo = fileLoaded[1]
        self = NN(int(databaseInfo[1]), int(databaseInfo[2]), int(databaseInfo[3]), regression = False, NNcurrentWeights = NNfileName)
	
        tmp = []
        for p in patterns:
            if verbose:
                expected = p[1]
                NNRoundResult = self.roundResult (self.update(p[0]))
                print expected, '->', NNRoundResult, '->',  (expected==NNRoundResult)
            tmp.append(self.update(p[0]))

        return tmp


    def roundResult (self, result): 
        roundedResult = []
        for x in result:
            if (x>0.5):
                roundedResult.append (1)
            else:
                roundedResult.append (0)
        return roundedResult; 
        
        
    def weights(self):
        print 'Input weights:'
        for i in range(self.ni):
            print self.wi[i]
        print
        print 'Output weigoutputFileNamehts:'
        for j in range(self.nh):
            print self.wo[j]


    @staticmethod
    def train(patternsfileName, NNfileName, outputFileName, min_error, max_iterations=1000, N=0.5, M=0.2, verbose = False):
	
        db = dbconnector(patternsfileName)
	patterns = db[0]
	patternsInfo = db [1]
	self = NN(int(patternsInfo[1]), int(patternsInfo[2]), int(patternsInfo[3]), regression = False, NNcurrentWeights = NNfileName)


	self.trainWork (patterns, outputFileName ,min_error, N, M, max_iterations)


    @staticmethod
    def newtrain(patternsfileName, outputFileName,  min_error, max_iterations=1000, N=0.5, M=0.2, verbose = False):


        db = dbconnector(patternsfileName)
	patterns = db[0]
	patternsInfo = db [1]
	self = NN(int(patternsInfo[1]), int(patternsInfo[2]), int(patternsInfo[3]), regression = False)


        """Train the neural network.  
        
        N is the learning rate.
        M is the momentum factor.
        """



	self.trainWork (patterns, outputFileName ,min_error, N, M, max_iterations)
	

    def trainWork (self, patterns, outputFileName ,min_error, N, M,  max_iterations=1000):
        for i in xrange(max_iterations):
            error = 0.0
            for p in patterns:
                self.update(p[0])
                tmp = self.backPropagate(p[1], N, M)
                error += tmp
                
            if i % 100 == 0 or min_error == error:
                print 'error %-14f' % error
		dbsaveWeights(self, outputFileName)
		if min_error > error:
                    break

            

def Demo():


	## XOR EXAMPLE

   ##NN.newtrain('exampleData/xorDb', 'exampleData/xorNn', 0.5,  100000000, 0.001, 0.001)
   ##NN.train('exampleData/xorDb', 'exampleData/xorNn', 'exampleData/xorNn', 5,  10000000, 0.001, 0.001)
   ##print NN.test('exampleData/xorNn', 'exampleData/xorDb', True )
  
	## Numbers EXAMPLE

   ##NN.newtrain('exampleData/numbersDb', 'exampleData/numbersNn-new', 0.5,  100000000, 0.001, 0.001)
   ##NN.train('exampleData/numbersDb', 'exampleData/numbersNn-working', 'exampleData/numbersNn-working-2', 0.5,  10000000, 0.01, 0.01)
   ##print NN.test('exampleData/numbersNn-new', 'exampleData/numbersDb', True )
  

if __name__ == '__main__':
    Demo()

