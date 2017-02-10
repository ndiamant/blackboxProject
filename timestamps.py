import numpy as np
import pickle
import itertools

with open('ids_states', 'rb') as f:
    ids, states = pickle.load(f)

order = np.argsort(ids[:,0])
ids = ids[order]
states = states[order]

def clean_for_states(ids, states, target_states = [1, 7]):
    '''
    returns copy of states, ids such that only file ids that get to state target_state are saved
    '''
    ids_states_list = np.hstack((ids, states[:, np.newaxis])).tolist()
    groups = []
    uniquekeys = []
    for k, g in itertools.groupby(ids_states_list, lambda x: x[0]):
        groups.append(list(g))      # Store group iterator as a list
        uniquekeys.append(k)
    
    new_ids_states_list = []
    for group in groups:
        target_states_copy = target_states[:]
        for entry in group:
            if entry[-1] in target_states_copy:
                target_states_copy.remove(entry[-1])
        if len(target_states_copy) == 0:
            new_ids_states_list += group
    return np.array(new_ids_states_list)

t = clean_for_states(ids, states)
print(tuple(t[:,1].tolist()))
# pie plot of states
#import matplotlib.pyplot as plt
#counts = np.bincount(states)
#plt.pie(counts, labels = [i for i in range(8)])
#plt.show()

#np.savetxt("event_ids.csv", ids[:,1].astype(int))
