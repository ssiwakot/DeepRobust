Introduction to Graph Defense with Examples
=======================
In this section, we introduce the graph attack algorithms provided 
in DeepRobust. 

.. contents::
    :local: 

Test your model's robustness on poisoned graph
-------
DeepRobust provides a series of defense methods that aim to enhance the robustness
of GNNs.

Victim Models:

- :class:`deeprobust.graph.defense.GCN`
- :class:`deeprobust.graph.defense.GAT`
- :class:`deeprobust.graph.defense.ChebNet`
- :class:`deeprobust.graph.defense.SGC`

Node Embedding Victim Models: (see more details `here <https://deeprobust.readthedocs.io/en/latest/graph/node_embedding.html>`_)

- :class:`deeprobust.graph.defense.DeepWalk`
- :class:`deeprobust.graph.defense.Node2Vec`

Defense Methods:

- :class:`deeprobust.graph.defense.GCNJaccard`
- :class:`deeprobust.graph.defense.GCNSVD`
- :class:`deeprobust.graph.defense.ProGNN`
- :class:`deeprobust.graph.defense.RGCN`
- :class:`deeprobust.graph.defense.SimPGCN`
- :class:`deeprobust.graph.defense.AdvTraining`

#. Load pre-attacked graph data 

    .. code-block:: python
       
       from deeprobust.graph.data import Dataset, PrePtbDataset
       data = Dataset(root='/tmp/', name='cora', seed=15) # make sure random seed is set to 15, 
                                                          # since the attacked graph are generated under seed 15
       adj, features, labels = data.adj, data.features, data.labels
       idx_train, idx_val, idx_test = data.idx_train, data.idx_val, data.idx_test
       # Load meta attacked data
       perturbed_data = PrePtbDataset(root='/tmp/',
                           name='cora',
                           attack_method='meta',
                           ptb_rate=0.05)
       perturbed_adj = perturbed_data.adj

#. Train a victim model (GCN) on clearn/poinsed graph

    .. code-block:: python
       
       from deeprobust.graph.defense import GCN
       gcn = GCN(nfeat=features.shape[1],
           nhid=16,
           nclass=labels.max().item() + 1,
           dropout=0.5, device='cpu')
       gcn = gcn.to('cpu')
       gcn.fit(features, adj, labels, idx_train, idx_val) # train on clean graph with earlystopping
       gcn.test(idx_test)
         
       gcn.fit(features, perturbed_adj, labels, idx_train, idx_val) # train on poisoned graph
       gcn.test(idx_test)

#. Train defense models (GCN-Jaccard, RGCN, ProGNN) poinsed graph

    .. code-block:: python
       
       from deeprobust.graph.defense import GCNJaccard
       model = GCNJaccard(nfeat=features.shape[1],
                 nhid=16,
                 nclass=labels.max().item() + 1,
                 dropout=0.5, device='cpu').to('cpu')
       model.fit(features, perturbed_adj, labels, idx_train, idx_val, threshold=0.03)         
       model.test(idx_test)

    .. code-block:: python
       
       from deeprobust.graph.defense import GCNJaccard
       model = RGCN(nnodes=perturbed_adj.shape[0], nfeat=features.shape[1],
                    nclass=labels.max()+1, nhid=32, device='cpu')
       model.fit(features, perturbed_adj, labels, idx_train, idx_val,
                 train_iters=200, verbose=True)
       model.test(idx_test)

      
For details in training ProGNN, please refer to `this page <https://github.com/ChandlerBang/Pro-GNN/train.py>`_. 


More Examples 
-----------------------
More examples can be found in :class:`deeprobust.graph.defense`. You can also find examples in 
`github code examples <https://github.com/DSE-MSU/DeepRobust/tree/master/examples/graph>`_ 
and more details in `defense table <https://github.com/DSE-MSU/DeepRobust/tree/master/deeprobust/graph#defense-methods>`_.
