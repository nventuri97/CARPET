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

    #Method to generate a matrix which represent the transition function
    #needed to implement OT protocol
    def to_matrix(self):
        #Matrix definition we have states on row
        #and character of the alphabet on column

        transitions=self.get_transitions()
        trans_mat=np.zeros((self.states.__len__, transitions.__len__), int)

        sorted_tran= sorted(transitions, key =itemgetter(1))

        for state in self.states:
            #now i have to create the transition matrix