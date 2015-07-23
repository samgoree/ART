# ARTNetwork.py
# Adapted from http://mnemstudio.org/neural-networks-art1-example-1.htm

import math
import sys

N = 4 # Number of components in an input vector.
M = 5 # Max number of clusters to be formed.
VIGILANCE = 0.4

PATTERN_ARRAY = [[1, 1, 0, 0], 
                 [0, 0, 0, 1], 
                 [1, 0, 0, 0], 
                 [0, 0, 1, 1], 
                 [0, 1, 0, 0], 
                 [0, 0, 1, 0], 
                 [1, 0, 1, 0]]

class ART1:
    def __init__(self, inputSize, numClusters, vigilance):
        self.mInputSize = inputSize
        self.mNumClusters = numClusters
        self.mVigilance = vigilance
        
        self.bw = [] # Bottom-up weights.
        self.tw = [] # Top-down weights.

        self.f1a = [] # Input layer.
        self.f1b = [] # Interface layer.
        self.f2 = []
		#initialize bottom-up weight matrix.
        for i in range(self.mNumClusters):
            self.bw.append([0.0] * self.mInputSize)
            for j in range(self.mInputSize):
                self.bw[i][j] = 1.0 / (1.0 + self.mInputSize)
        
        # Initialize top-down weight matrix.
        for i in range(self.mNumClusters):
            self.tw.append([0.0] * self.mInputSize)
            for j in range(self.mInputSize):
                self.tw[i][j] = 1.0

        self.f1a = [0.0] * self.mInputSize
        self.f1b = [0.0] * self.mInputSize
        self.f2 = [0.0] * self.mNumClusters
        
    
    def get_vector_sum(self, nodeArray):
        total = 0
        for i in range(len(nodeArray)):
            total += nodeArray[i]
        return total
    
    def get_maximum(self, nodeArray):
        maximum = -1
        maxValue = -0
        unique = True
        for i in range(len(nodeArray)):
            if nodeArray[i] > maxValue:
                maximum = i
                maxValue = nodeArray[i]
        return maximum
    
    def test_for_reset(self, activationSum, inputSum, f2Max):
        if(inputSum == 0): return False
        elif(float(activationSum) / float(inputSum) >= self.mVigilance):
            return False # Candidate is accepted.
        else:
            self.f2[f2Max] = -1.0 # Inhibit.
            return True # Candidate is rejected.
    
    def update_weights(self, activationSum, f2Max):
        # Update bw(f2Max)
        for i in range(self.mInputSize):
            self.bw[f2Max][i] = (2.0 * float(self.f1b[i])) / (1.0 + float(activationSum))
        
        
        # Update tw(f2Max)
        for i in range(self.mInputSize):
            self.tw[f2Max][i] = self.f1b[i]

    def ART1(self, trainingPattern, isTraining):
        inputSum = 0
        activationSum = 0
        f2Max = 0
        reset = True
        

        # Initialize f2 layer activations to 0.0
        for i in range(self.mNumClusters):
            self.f2[i] = 0.0
        
        # Input pattern() to f1 layer.
        for i in range(self.mInputSize):
            self.f1a[i] = float(trainingPattern[i])
        
        # Compute sum of input pattern.
        inputSum = self.get_vector_sum(self.f1a)
		
#        if inputSum == 0:
#            return None
        
        # Compute activations for each node in the f1 layer.
        # Send input signal from f1a to the fF1b layer.
        for i in range(self.mInputSize):
            self.f1b[i] = self.f1a[i]
            
        # Compute net input for each node in the f2 layer.
        for i in range(self.mNumClusters):
            for j in range(self.mInputSize):
                self.f2[i] += self.bw[i][j] * float(self.f1a[j])
           
        reset = True
        while reset:
            # Determine the largest value of the f2 nodes.
            f2Max = self.get_maximum(self.f2)
            
			# If there is no maximum, add a new node
            if f2Max == -1:
                f2Max = self.mNumClusters
                self.f2.append(0.0)
                self.tw.append([1.0] * self.mInputSize)
                self.bw.append([1.0 / (1.0 + self.mInputSize)] * self.mInputSize)
                self.mNumClusters+=1

			
            # Recompute the f1a to f1b activations (perform AND function)
            for i in range(self.mInputSize):
                self.f1b[i] = self.f1a[i] * math.floor(self.tw[f2Max][i])

            # Compute sum of input pattern.
            activationSum = self.get_vector_sum(self.f1b)
            reset = self.test_for_reset(activationSum, inputSum, f2Max)
           
        # if we are training, train the network
        if isTraining:
            self.update_weights(activationSum, f2Max)
            
        return f2Max
    
    def print_results(self):
        sys.stdout.write("Clusters found: " + str(self. mNumClusters) + "\n")
        sys.stdout.write("Rho: " + str(self.mVigilance) + "\n\n")
        sys.stdout.write("Final weight values:\n")
        
        for i in range(self.mNumClusters):
            for j in range(self.mInputSize):
                sys.stdout.write(str(self.bw[i][j]) + ", ")
            
            sys.stdout.write("\n")
        sys.stdout.write("\n")
        
        for i in range(self.mNumClusters):
            for j in range(self.mInputSize):
                sys.stdout.write(str(self.tw[i][j]) + ", ")
            
            sys.stdout.write("\n")
        sys.stdout.write("\n")
        return

if __name__ == '__main__':
    net = ART1(N, M, VIGILANCE)
    for line in PATTERN_ARRAY:
        net.ART1(line, True)
    for line in PATTERN_ARRAY:
        print(str(line) + ',' + str(net.ART1(line, True)))
    