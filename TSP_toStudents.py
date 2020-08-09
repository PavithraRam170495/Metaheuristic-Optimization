

"""
Author:
file:
Rename this file to TSP_x.py where x is your student number 
"""

import random
import math
from Individual import *
import sys

myStudentNum = 183771 # Replace 12345 with your student number
random.seed(myStudentNum)
f = open(sys.argv[2],"a")
class BasicTSP:
    def __init__(self, _fName, _popSize, _mutationRate, _maxIterations):
        """
        Parameters and general variables
        """

        self.population     = []
        self.matingPool     = []
        self.best           = None
        self.popSize        = _popSize
        self.genSize        = None
        self.mutationRate   = _mutationRate
        self.maxIterations  = _maxIterations
        self.iteration      = 0
        self.fName          = _fName
        self.data           = {}

        self.readInstance()
        self.initPopulation()


    def readInstance(self):
        """
        Reading an instance from fName
        """
        file = open(self.fName, 'r')
        self.genSize = int(file.readline())
        self.data = {}
        for line in file:
            (id, x, y) = line.split()
            self.data[int(id)] = (int(x), int(y))
        file.close()

    def initPopulation(self):
        """
        Creating random individuals in the population
        """
        for i in range(0, self.popSize):
            individual = Individual(self.genSize, self.data)
            individual.computeFitness()
            self.population.append(individual)

        self.best = self.population[0].copy()
        for ind_i in self.population:
            if self.best.getFitness() > ind_i.getFitness():
                self.best = ind_i.copy()
        print ("Best initial sol: ",self.best.getFitness())
        f.write("Best initial sol:"+str(self.best.getFitness())+"\n")
    
    def initPopulation_heuristic(self):
        for i in range(0, self.popSize):
            
            instance = self.data
            cities = list(instance.keys())
            cIndex = random.randint(0, len(instance)-1)
    
            tCost = 0
    
            solution = [cities[cIndex]]
        
            del cities[cIndex]
    
            current_city = solution[0]
            while len(cities) > 0:
                bCity = cities[0]
#                print("c",instance[current_city])
#                print("b",instance[bCity])
                bCost = self.euclideanDistance(instance[current_city], instance[bCity])
#                cost = 0
#                bCost = 0
                bIndex = 0
    #            printbCity,bCost)
                for city_index in range(1, len(cities)):
                    city = cities[city_index]
                    cost = self.euclideanDistance(instance[current_city], instance[city])
    #                print(cities[city_index], "Cost: ",cost)
                    if bCost > cost:
                        bCost = cost
                        bCity = city
                        bIndex = city_index
                tCost += bCost
                current_city = bCity
                solution.append(current_city)
                del cities[bIndex]
                tCost += self.euclideanDistance(instance[current_city], instance[solution[0]])
            individual = Individual(self.genSize, self.data)
            individual.setGene(solution)
            individual.computeFitness()
            self.population.append(individual)
            
        self.best = self.population[0].copy()
        for ind_i in self.population:
            if self.best.getFitness() > ind_i.getFitness():
                self.best = ind_i.copy()
        print ("Best initial sol: ",self.best.getFitness())
        f.write("Best initial sol: "+ str(self.best.getFitness())+"\n")
        return

    def euclideanDistance(self,cityA, cityB):
        ##Euclidean distance
        #return math.sqrt( (cityA[0]-cityB[0])**2 + (cityA[1]-cityB[1])**2 )
        #Rounding nearest integer
        return round( math.sqrt( (cityA[0]-cityB[0])**2 + (cityA[1]-cityB[1])**2 ) )

    def updateBest(self, candidate):
        if self.best == None or candidate.getFitness() < self.best.getFitness():
            self.best = candidate.copy()
            print ("iteration: ",self.iteration, "best: ",self.best.getFitness())
            f.write("iteration: "+str(self.iteration)+ "best: "+ str(self.best.getFitness())+"\n")

    def randomSelection(self):
        """
        Random (uniform) selection of two individuals
        """
        indA = self.matingPool[ random.randint(0, self.popSize-1) ]
        indB = self.matingPool[ random.randint(0, self.popSize-1) ]
        return [indA, indB]

    def stochasticUniversalSampling(self):
        inverse = []
        fit_prob = []
        selected = []
        total = 0
        fit_scale = [0]
        tot_fit = 0
        for i in range(0,self.popSize):
            fitness_parent = 1/self.population[i].fitness
            inverse.append(fitness_parent)
            total += fitness_parent
        for i in inverse:
            fit_prob.append(i/total)
        for i in fit_prob:
            tot_fit = tot_fit + i
            fit_scale.append(tot_fit)
        n = random.randint(round(self.popSize/2),self.popSize)
        pointer = random.uniform(0,1/n)
        pointer_value = pointer
        equal_scale = [pointer]
        for i in range(0,n):
            pointer_value += pointer
            equal_scale.append(pointer_value)
        for i in range(0,len(equal_scale)-1):
            for j in range(0,len(fit_scale)-1):
                if equal_scale[i] <= fit_scale[j] and equal_scale[i] >fit_scale[j-1]:
                    selected.append(self.population[j])
        parent1 = random.choice(selected)
        parent2 = random.choice(selected)
        return parent1,parent2
        
        
        

    def uniformCrossover(self, indAa, indBb):
        indA = indAa.genes
        indB = indBb.genes
        child1 = [0] * self.genSize
        child2 = [0] * self.genSize
        #Pick random positions which will be fixed
        fixed_positions = random.sample(range(0,self.genSize),random.randint(1,self.genSize-1))
        #print(fixed_positions)
        for i in fixed_positions:
            child1[i] = indA[i]
            child2[i] = indB[i]
        for i in range(0,self.genSize):
            for j in range(0,self.genSize):
                if child1[i] == 0 and indB[j] not in child1:
                    child1[i] = indB[j]
                if child2[i] == 0 and indA[j] not in child2:
                    child2[i] = indA[j]
                

        #print(child1,child2)
        return child1

    def pmxCrossover(self, indAa, indBb):
        indA = indAa.genes
        indB = indBb.genes
        child1 = [0] * self.genSize
        child2 = [0] * self.genSize
        block = random.sample(range(0,self.genSize),2)
       # print (block)
        for i in range(min(block),max(block)+1):
            child1[i] = indB[i]
            child2[i] = indA[i]
        for i in range(0,self.genSize):
            if i not in range(min(block),max(block)+1):
                if indA[i] not in child1:
                    child1[i] = indA[i]
                if indB[i] not in child2:
                    child2[i] = indB[i]
            if child1[i] == 0:
                c = 1
                parent_value = indA[i]
                while(c == 1):
                    index = child1.index(parent_value)
                    #print(index)
                    if child2[index] not in child1:
                        child1[i] = child2[index]
                        c = 0
                    else:
                        parent_value = child2[index]
        return child1
            
                    
    
    def reciprocalExchangeMutation(self, ind):
        """
        Mutate an individual by swaping two cities with certain probability (i.e., mutation rate)
        """
        if random.random() > self.mutationRate:
            return
        indexA = random.randint(0, self.genSize-1)
        indexB = random.randint(0, self.genSize-1)

        tmp = ind.genes[indexA]
        ind.genes[indexA] = ind.genes[indexB]
        ind.genes[indexB] = tmp

        ind.computeFitness()
        self.updateBest(ind)
        

    def inversionMutation(self, ind):
        if random.random() > self.mutationRate:
            return
        index = random.sample(range(0,ind.genSize),2)
        invert = []
        for i in range(min(index),max(index)+1):
            invert.append(ind.genes[i])
        invert.reverse()
        #print(invert)
        for i in range(min(index),max(index)+1):
            ind.genes[i] = invert.pop(0)
        ind.computeFitness()
        self.updateBest(ind)
        

    def crossover(self, indA, indB):
        """
        Executes a 1 order crossover and returns a new individual
        """
        child = []
        tmp = {}

        indexA = random.randint(0, self.genSize-1)
        indexB = random.randint(0, self.genSize-1)

        for i in range(0, self.genSize):
            if i >= min(indexA, indexB) and i <= max(indexA, indexB):
                tmp[indA.genes[i]] = False
            else:
                tmp[indA.genes[i]] = True
        aux = []
        for i in range(0, self.genSize):
            if not tmp[indB.genes[i]]:
                child.append(indB.genes[i])
            else:
                aux.append(indB.genes[i])
        child += aux
        return child

    def mutation(self, ind):
        """
        Mutate an individual by swaping two cities with certain probability (i.e., mutation rate)
        """
        if random.random() > self.mutationRate:
            return
        indexA = random.randint(0, self.genSize-1)
        indexB = random.randint(0, self.genSize-1)

        tmp = ind.genes[indexA]
        ind.genes[indexA] = ind.genes[indexB]
        ind.genes[indexB] = tmp

        ind.computeFitness()
        self.updateBest(ind)

    def updateMatingPool(self):
        """
        Updating the mating pool before creating a new generation
        """
        self.matingPool = []
        for ind_i in self.population:
            self.matingPool.append( ind_i.copy() )

    def newGeneration(self):
        """
        Creating a new generation
        1. Selection
        2. Crossover
        3. Mutation
        """
        
        for i in range(0, len(self.population)):
            """
            Depending of your experiment you need to use the most suitable algorithms for:
            1. Select two candidates
            2. Apply Crossover
            3. Apply Mutation
            """
            ind1,ind2 = self.randomSelection()
            #ind1,ind2 = self.stochasticUniversalSampling()
            child = self.pmxCrossover(ind1,ind2)
            new_object = Individual(self.genSize,self.data)
            new_object.setGene(child)
            #print(new_object.genes)
            new_object.computeFitness()
            self.reciprocalExchangeMutation(new_object)
            self.population[i] = new_object
        
        
            

    def GAStep(self):
        """
        One step in the GA main algorithm
        1. Updating mating pool with current population
        2. Creating a new Generation
        """

        self.updateMatingPool()
        self.newGeneration()

    def search(self):
        """
        General search template.
        Iterates for a given number of steps
        """
        self.iteration = 0
        while self.iteration < self.maxIterations:
            self.GAStep()
            self.iteration += 1

        print ("Total iterations: ",self.iteration)
        print ("Best Solution: ", self.best.getFitness())
        f.write("Best Solution:"+str(self.best.getFitness()))

#if len(sys.argv) < 2:
#    print ("Error - Incorrect input")
#    print ("Expecting python BasicTSP.py [instance] ")
#    sys.exit(0)
#
#
#problem_file = sys.argv[1]
for i in range(0,5):
    print("Iteration:",i)
    f.write("Iteration no.:"+str(i)+"\n")
    ga = BasicTSP(sys.argv[1], 300, 0.1, 500)
    ga.search()
f.close()
