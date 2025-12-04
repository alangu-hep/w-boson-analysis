#!/usr/bin/env python3

import sys
import os
import json

import numpy as np
import awkward as ak
import uproot
import time
import requests

import atlasopenmagic as atom

workdir = os.getenv('WORKDIR')
sys.path.append(workdir)
from utils import config as cfg
from utils.calculations import calc_mt, calc_weight
from utils import selection

atom.set_release(cfg.release)

data_samples = atom.build_dataset(cfg.dataset_ids, skim = cfg.skim, protocol = 'https', cache = True)

all_data = {}

for sample in data_samples:

    print(f'Currently working on: {sample}')

    frames = []

    for url in data_samples[sample]['list']:
        if sample == 'Data':
            prefix = "Data/" 
        else: 
            prefix = "MC/mc_"
        string = url

        start = time.time()
        print("\t"+url+":")

        tree = uproot.open(string + ":analysis")

        sample_data = []

        for data in tree.iterate(cfg.physical_variables + cfg.cut_variables + cfg.weight_variables,
                                 entry_stop=tree.num_entries):

            pre_selection = len(data)

            data = data[selection.trig_cuts(data.trigE, data.trigM)]
                                 
            data['leading_lep_pt'] = data['lep_pt'][:,0]
            data = data[data['leading_lep_pt'] > 7]
                        
            data = data[selection.detector_cuts(data.lep_isTrigMatched, data.lep_isTightIso, data.lep_isTightID)]

            lep_type = data['lep_type']
            lep_eta = data['lep_eta']
            data = data[selection.type_cut(lep_type, lep_eta)]
                        
            data['transverse_mass'] = calc_mt(data['lep_e'], data['met'], data['lep_phi'], data['met_phi'])

            if 'Data' not in sample:
                data['totalWeight'] = calc_weight(cfg.weight_variables, data)

            sample_data.append(data)
                                 
            elapsed = time.time() - start

            if not 'Data' in sample:
                post_selection = sum(data['totalWeight'])
                print("\t\t Sum of Weights: \t"+str(post_selection)+"\t in "+str(round(elapsed,1))+"s")
            else:
                post_selection = len(data)
                print("\t\t Pre-Selection: "+str(pre_selection)+",\t Post-Selection: \t"+str(post_selection)+"\t in "+str(round(elapsed,1))+"s")
                        
        frames.append(ak.concatenate(sample_data))

    all_data[sample] = ak.concatenate(frames)
                      
# Adopted from Weaver

with uproot.recreate(os.path.join(workdir, 'outputs/processed_data.root'), compression=uproot.LZ4(4)) as fout:
    for field in all_data.fields:
        total_data = all_data[field]
        tree = fout.mktree('Data', {f: total_data[f].type for f in total_data.fields})
        start = 0
        while start < len(total_data[total_data.fields[0]]) - 1:
            tree.extend({k: total_data[k][start:start + 1048576] for k in total_data.fields})
            start += 1048576