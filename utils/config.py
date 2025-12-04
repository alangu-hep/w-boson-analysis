# Data Configuration for primary analysis

'''
Domain Properties
'''

luminosity = 36.6
GeV = 1.0 # Standard unit
MeV = 0.001

'''
Dataset Config
'''

skim = '1LMET30'
release = '2025e-13tev-beta'

dataset_ids = {
    r'Data': {'dids': ['data']},
    r'Signal $W \rightarrow e \nu$': {'dids': [700338, 700340]},
    r'Signal $W \rightarrow \mu \nu$': {'dids': [700341, 700342, 700343]},
    r'QCD Background': {'dids': [364700]},
    r'Background $Z \rightarrow \nu \nu, Z \rightarrow ll': {'dids': [364243]},
    r'WZ Background': {'dids': [700489]}
}

'''
Selection Variables
'''

physical_variables = ['lep_e', 'lep_pt', 'lep_phi', 'lep_eta', 'met', 'met_phi']
cut_variables = ['lep_type', 'lep_isTightID', 'lep_isTightIso', 'trigE', 'trigM', 'trigMET', 'lep_isTrigMatched']
weight_variables = ['mcWeight', 'kfac', 'xsec', 'ScaleFactor_PILEUP', 'ScaleFactor_ELE', 'ScaleFactor_MUON', 'ScaleFactor_LepTRIGGER', 'ScaleFactor_ElTRIGGER', 'ScaleFactor_MuTRIGGER']
