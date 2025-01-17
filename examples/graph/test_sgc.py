import torch
import argparse
from deeprobust.graph.data import Dataset, Dpr2Pyg
from deeprobust.graph.defense import SGC
from deeprobust.graph.data import Dataset
from deeprobust.graph.data import PrePtbDataset

parser = argparse.ArgumentParser()
parser.add_argument('--seed', type=int, default=15, help='Random seed.')
parser.add_argument('--dataset', type=str, default='cora', choices=['cora', 'cora_ml', 'citeseer', 'polblogs', 'pubmed'], help='dataset')
parser.add_argument('--ptb_rate', type=float, default=0.05,  help='perturbation rate')

args = parser.parse_args()
args.cuda = torch.cuda.is_available()
print('cuda: %s' % args.cuda)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

data = Dataset(root='/tmp/', name=args.dataset, setting='nettack', seed=15)
adj, features, labels = data.adj, data.features, data.labels
idx_train, idx_val, idx_test = data.idx_train, data.idx_val, data.idx_test

sgc = SGC(nfeat=features.shape[1],
      nclass=labels.max().item() + 1,
      lr=0.1, device=device)
sgc = sgc.to(device)


# test on clean graph
print('==================')
print('=== train on clean graph ===')

pyg_data = Dpr2Pyg(data)
sgc.fit(pyg_data, verbose=True) # train with earlystopping
sgc.test()

# load pre-attacked graph by Zugner: https://github.com/danielzuegner/gnn-meta-attack
print('==================')
print('=== load graph perturbed by Zugner metattack (under seed 15) ===')
perturbed_data = PrePtbDataset(root='/tmp/',
        name=args.dataset,
        attack_method='meta',
        ptb_rate=args.ptb_rate)
perturbed_adj = perturbed_data.adj
pyg_data.update_edge_index(perturbed_adj) # inplace operation
sgc.fit(pyg_data, verbose=True) # train with earlystopping
sgc.test()




