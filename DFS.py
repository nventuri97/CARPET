from transitions import Machine
import numpy as np
from operator import itemgetter

class DFS(Machine):
    
    #This alphabet is choosen to implement a DFS using in
    #a COVID-19 application
    alphabet=['a(-)', 'a(+)', 's(-)', 's(+)', 'v(-)', 'v(+)']
    callback=['a_less', 'a_plus', 's_less', 's_plus', 'v_less', 'v_plus']

    def __init__(self, states):

        #super constructor of Machine class imported from transitions
        super(model=self, states=states, initial='0').__init__()
        self.alphabet=alphabet
        self.callback=callback

    #Method to generate a matrix which represent the transition function
    #needed to implement OT protocol
    def to_matrix(self):
        #Matrix definition we have states on row
        #and character of the alphabet on column

        transitions=self.get_transitions()
        trans_mat=np.zeros((self.states.__len__, transitions.__len__), int)

        #Sorted transition by source state
        sorted_tran= sorted(transitions, key =itemgetter(1))

        #For each state i check which transitions take to a new state
        #and i build the new transition matrix
        for state in self.states:
            while(sorted_tran.__getitem__(1)==state):
                trans_mat[int(state)][callback.index(sorted_tran.__getitem__(0))]=sorted_tran.__getitem__(2)