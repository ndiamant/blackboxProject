import numpy as np
import pickle

with open('ids_states', 'rb') as f:
    ids, states = pickle.load(f)

order = np.argsort(ids[:,0])
ids = ids[order]
states = states[order]

import matplotlib.pyplot as plt

counts = np.bincount(states)

# pie plot of states
#plt.pie(counts, labels = [i for i in range(8)])
#plt.show()

np.savetxt("event_ids.csv", ids[:,1].astype(int))
