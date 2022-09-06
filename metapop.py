

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np 

class Metapopulation():

    def __init__(self, V, N, b_W, beta, mu):

        self.V = V                                         # number of nodes
        self.N = N                                         # population size per node 
        self.S = np.ones(self.V, dtype=np.int64) * self.N  # suscpeptible per node
        self.I = np.zeros(self.V, dtype=np.int64)          # infected per node 
        self.S -= self.I
        self.b_W = b_W                                     # max value of individuals moving between nodes

        # setting SIS parameters
        self.beta = beta
        self.mu = mu
    
        # movement matrix, we assume the flow of ppl to be simmetric 
        self.W = np.tril(np.random.randint(self.b_W, size=(self.V, self.V)), k=-1)


    def run(self, t):
        self.I[0] = 100
        self.I[1] = 100
        self.S -= self.I
        
        for i in range(t):
            I_ratio =  self.I / (self.S + self.I)

            # infected & recovered 
            I_t = [np.random.binomial(self.S[i], self.beta * I_ratio[i]) for i in range(self.V)]
            S_t = [np.random.binomial(self.I[i], self.mu) for i in range(self.V)]
            print(I_t)
            print(S_t)

            # movement
            X_I = np.zeros((self.V, self.V))
            
            for j in range(self.V):
                print([np.random.binomial(self.W[i, j], I_ratio[i]) for i in range(self.V)])
                X_I[:,j] = [np.random.binomial(self.W[i, j], I_ratio[i]) for i in range(self.V)]
           
            X_S = self.W - X_I
            print(X_I)

            # update
            for i in range(self.V):
                print(X_I[j, i], X_I[i, j])
                print(np.sum([X_I[j, i] - X_I[i, j] for j in range(self.V) if j < i]))
                print(np.sum([X_S[j, i] - X_S[i, j] for j in range(self.V) if j < i]))
                self.I[i] += np.sum([X_I[j, i] - X_I[i, j] for j in range(self.V) if j < i]) + I_t[i] - S_t[i]
                self.S[i] += np.sum([X_S[j, i] - X_S[i, j] for j in range(self.V) if j < i]) - I_t[i] + S_t[i]

    
            print(self.I, self.S)
            print(self.V * self.N)
            print(np.sum(self.I) + np.sum(self.S))

if __name__ == '__main__':
    model = Metapopulation(10, 10000, 1000, 0.3, 0.1)
    model.run(1)
