from warnings import resetwarnings

from z3 import *
from Node import *
from Interaction import *
from RegulationConditions import *
from itertools import product, chain, permutations, combinations
from RegulationConditions_Optional import *

class BoolNetwork:
    def __init__(self):
        self.components = {}
        self.conditions = {}
        self.experiments=[]
        self.possible_interactions=[]
        self.definite_interactions=[]
        self.regConds={}
        self.perm_interactions = self.generate_permutations()
        self.perm_index=0

    def add_component(self, name, RegConditions):
        A = RegConditions.split('-')
        B = RegConditions.split(',')
        regulation = []
        if len(A)>1:#if we have a x-y reg then add all regulation conditions in the range
            regulation = list(range(int(A[0]),int(A[1])+1))
        else:
            regulation =[int(i) for i in B] #else we have individual reg cond
        self.components[name] = (Node(name,regulation)) #add component +reg

    def eval_regulation_conditions(self): #this method synthesizes the reg conditions to nuXmv
        arr=self.experiments[0][0][1] #-change it-
        h= len(self.experiments)
        for i in self.components.values():
            for k in range(h):
                self.regConds[i.name+str(k)]=RegulationConditions(i,arr).eval_dict(k) #create a dictionary for name with all regulation conditions


        for i in self.regConds.keys():
            print(f"{i}: {self.regConds[i]}")

    def eval_regulation_conditions_optional(self):  # this method synthesizes the reg conditions to nuXmv
        arr = self.experiments[0][0][1]  # -change it-
        h = len(self.experiments)
        # (red,black,positive,optional),(red,green,positive,optional),(kkk,black,positive,optional) [kkk.
        all_possible_interactions = self.possible_interactions
        possible_idx = set((x[1], i) for i, x in enumerate(all_possible_interactions))
        print(f"possibleidx={possible_idx}")
        for i in self.components.values():
            edges = [(all_possible_interactions[j][0],all_possible_interactions[j][2]) for name, j in possible_idx if name == i.name]
            print(f"{i.name} edgesssss {edges}")
            for k in range(h):
                self.regConds[i.name + str(k)] = RegulationConditions_Optional(i, arr,edges).eval_dict(k)  # create a dictionary for name with all regulation conditions

        for i in self.regConds.keys():
            print(f"{i}: {self.regConds[i]}")
        return self.regConds

    def add_interaction(self,l):
        self.components[l[1]].add_source(l[0],l[2],None,l[3]) #add the interactions
        if l[3]=='True':
            self.possible_interactions.append((l[0],l[1],l[2]))
        else:
            self.definite_interactions.append((l[0],l[1],l[2]))

    def add_perm(self):
        definite_interactions=self.perm_interactions[self.perm_index]
        print(f"def int{definite_interactions}")
        for i in self.components.values():
            i.reset() #reset regulation condition because now some connections are present/not present, the network has changed
        for i in definite_interactions: #add the new interactions of the new permutation
            self.components[i[1]].add_source(i[0],i[2],True)
        for i in self.components.values():
            if i.sources == {}:
                i.sources = {i.name: ("positive", False)}
            print(f"{i.name}: {i.sources}")
        self.eval_regulation_conditions() #create the regulation conditions for current permutation
        self.perm_index+=1#move to next permutation
        return definite_interactions


    def add_condition(self, condition, name):  # add a condition
        #condition = condition.split()  # spilt the string ("A=1 and B=1" -> [A=1,AND,B=1]
        final = {}
        for i in condition:
            if i != "and":  # add all parts of the equation that are not "and"
                # if len(i) == 4:  # for example: "S1=1" THE LEN IS 4 so we need the first two letters
                #     final[i[0:2]] = i[-1]
                # else:
                #     final[i[0]] = i[-1]
                final[i[0:len(i)-2]] = i[-1] #split the condition and get the real value for each node
        self.conditions[name] = final


    def add_experiment(self, conditions):
        timestamps={}
        i=0
        while i<len(conditions):
            timestamps[conditions[i]] = {}
            j=i+1
            while j<len(conditions) and not str(conditions[j]).isnumeric(): #iterate over each experiment
                #timestamps[conditions[i]].append(self.conditions[conditions[j]])
                # print(f"dfsadasfdas{timestamps[conditions[i]] | self.conditions[conditions[j]]}")
                timestamps[conditions[i]]=timestamps[conditions[i]] | self.conditions[conditions[j]] #add conditions and expressions (which are part of same exp) together
                j=j+1
                print(f"print {timestamps[conditions[i]]}")
            i=j
        lst=[]
        # print(f"timestamps {timestamps}") #{'0': {'a': '1', 'B': '1', 'C': '0', 'S1': '0', 'S2': '1'}, '18': {'a': '0', 'B': '1', 'C': '1', 'S1': '0', 'S2': '1'}}

        #converting to list of tuples
        for i in timestamps.keys():
            lst.append((i,timestamps[i]))
        self.experiments.append(lst)


    def printall(self):
        for i in self.components.values():
            i.printall()
        for i in self.experiments:
            print(i)


    def print_interactions(self):
        print(f"{self.possible_interactions} possible interactions")
        print(f"{self.definite_interactions} definite interactions")


    def generate_permutations(self): #generate all possible permutations of optional connections
        sublists = []
        for r in range(len(self.possible_interactions) + 1):
            sublists.extend(combinations(self.possible_interactions, r))
        return( [self.definite_interactions+i for i in  [list(sublist) for sublist in sublists]])


    def possible_permutations(self):
        pos_interactions = self.definite_interactions
        return





