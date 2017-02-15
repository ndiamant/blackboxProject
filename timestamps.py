import numpy as np
import datetime
import pickle
import itertools
from dateutil.parser import parse as date_parse
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

plt.rcParams['axes.facecolor'] = 'gray'
# source file id, master event id

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

def read_stamps_csv(file_name):
    import pandas as pd
    return pd.read_csv(file_name, sep ='|').as_matrix()

times = read_stamps_csv('./all_stamps.csv')

time_order = np.argsort(times[:,0])
times = times[time_order]

t_order = np.argsort(t[:,1])
t = t[t_order]
t_time = np.hstack((t, times[:,1][:,np.newaxis]))
t_reorder = np.argsort(t_time[:,0])
t_time = t_time[t_reorder]

t_time2 = []

for i in t_time:
    date = None
    try: 
        date = date_parse(i[-1])
    except:
        continue
    t_time2.append(np.hstack((i[:-1], date)))

t_time2 = np.array(t_time2)

print(t_time2[0], t_time.shape, t_time2.shape)

def plot_deltas(data):
    '''
    Each row has the format:
    file id, event id, asdf, compile success, state, datetime
    The file ids should all be the same
    '''
    r = data.copy()
    r = r[np.argsort(r[:,-1])]

    deltas = r[:,-1].copy()
    d1 = np.hstack((deltas, np.array(datetime.datetime.max))) 
    d2 = np.hstack((np.array(datetime.datetime.max), deltas)) 
    deltas = (d1 - d2)[1:-1]
    deltas = map(lambda x: x.total_seconds(), deltas)

    times = r[:,-1] 
    times -= times[0]
    times = map(lambda x: x.total_seconds(), times)[:-1]

    points = np.array([times, deltas]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    
    cmap = ListedColormap(['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'])
    norm = BoundaryNorm(np.array(range(0,9)), cmap.N)
    lc = LineCollection(segments, cmap=cmap, norm = norm)
    lc.set_array(r[:,-2])
    lc.set_linewidth(3)

    fig1 = plt.figure()
    plt.gca().add_collection(lc)
    plt.xlim(min(times), max(times))
    plt.ylim(min(deltas), max(deltas))
   

plot_deltas(t_time2[t_time2[:,0] == 3432383])
plt.show()

# print t to copy to query mysql database
#print(tuple(t[:,1].tolist()))

# pie plot of states
#import matplotlib.pyplot as plt
#counts = np.bincount(states)
#plt.pie(counts, labels = [i for i in range(8)])
#plt.show()

#np.savetxt("event_ids.csv", ids[:,1].astype(int))
