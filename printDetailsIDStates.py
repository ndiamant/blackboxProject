import markov
import pickle
with open('tl.txt') as f:
    tl = pickle.load(f)

tl = filter(lambda x: 'printDetails' in x[0] and markov.isAscii(x[0]), tl)

tl = tl[0:10000]

ids = [x[1] for x in tl]
print(len(ids), ids[0:10])
states, agreements = markov.printDetailsState4(tl)
print(len(states), states[0:10])
print(len(agreements), agreements[0:10])
ids = np.array(ids)
states = np.array(states)
agreements = np.array(agreements)
ids = ids[agreements]
states = states[agreements]
print(states.shape, ids.shape)
with open('ids_states', 'wb') as f:
    pickle.dump((ids, states), f)
