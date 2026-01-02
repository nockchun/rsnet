import nengo

model = nengo.Network()
with model:
    stim = nengo.Node(0)
    a = nengo.Ensemble(n_neurons=20, dimensions=1, radius=5)
    nengo.Connection(stim, a)
