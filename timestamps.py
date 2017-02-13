import numpy as np
import pickle
import itertools
from dateutil.parser import parse as date_parse
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

def parse_time(string):
    if 'AM' in string or 'PM' in string:
        return parse_AM(string)
    if '.' in string:
        return parse_period(string)
    if '-' in string:
        return parse_dash(string)
    else:
        return parse_spacey(string)


def parse_period(string):
# 1007774150 | 14.des.2015 14:51:08       
    pass

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


# print t to copy to query mysql database
#print(tuple(t[:,1].tolist()))

# pie plot of states
#import matplotlib.pyplot as plt
#counts = np.bincount(states)
#plt.pie(counts, labels = [i for i in range(8)])
#plt.show()

#np.savetxt("event_ids.csv", ids[:,1].astype(int))
