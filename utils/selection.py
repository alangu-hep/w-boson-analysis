import numpy as np
import awkward as ak

def type_cut(lep_type, lep_eta):
    is_electron = (lep_type[:, 0] == 11) & (np.abs(lep_eta[:, 0]) <2.47)
    is_muon = (lep_type[:, 0]==13) & (lep_eta[:, 0]<2.47)
    return is_electron | is_muon
                     
def detector_cuts(trig_match, iso_match, id_match):
    mask = (trig_match[:, 0]) & (id_match[:, 0]) & (iso_match[:, 0])
    return mask
                     
def trig_cuts(trigE, trigM):
    mask = (trigE) | (trigM)
    return mask