from transitions import Machine
import numpy as np
from operator import itemgetter, attrgetter

class DFS(object):
    
    #This alphabet is choosen to implement a DFS using in
    #a COVID-19 application
    alphabet=['a(-)', 'a(+)', 's(-)', 's(+)', 'v(-)', 'v(+)']
    callback=['a_less', 'a_plus', 's_less', 's_plus', 'v_less', 'v_plus']

    def __init__(self, states, accept_states):
        self.states=states
        self.accept_states=accept_states
        self.machine=Machine(model=self, states=states, initial='0', auto_transitions=False)

    #Method to generate a matrix which represent the transition function
    #needed to implement OT protocol
    def to_matrix(self):
        #Matrix definition we have states on row
        #and character of the alphabet on column

        transitions=self.machine.get_transitions()
        trans_mat=np.zeros((len(self.states), len(self.alphabet)), int)

        #Sorted transition by source state
        sorted_tran= sorted(transitions, key=attrgetter('source'))

        #For each state i check which transitions take to a new state
        #and i build the new transition matrix
        for state in self.states:
            for trans in sorted_tran:
                if trans.source==state :
                    index=self.alphabet.index(trans.conditions[0].func)
                    trans_mat[int(state)][index]=trans.dest
                else:
                    break
            sorted_tran.reverse()
        
        return trans_mat.transpose() 