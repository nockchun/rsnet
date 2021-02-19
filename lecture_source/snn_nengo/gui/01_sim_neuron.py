import nengo

model = nengo.Network()
with model:
    stim = nengo.Node([0])
    ens = nengo.Ensemble(
        n_neurons=2,
        dimensions=1,
        encoders=[[1], [-1]],
        max_rates=[30, 30],
        intercepts=[-0.5, -0.5],
        neuron_type=nengo.LIF()
    )
    nengo.Connection(stim, ens)
