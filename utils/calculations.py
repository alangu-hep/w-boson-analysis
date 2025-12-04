import numpy as np
import vector
import awkward

def delta_phi(lep_phi, met_phi):
    
    delta_phi = lep_phi - met_phi
    
    return delta_phi

def calc_mt(lep_e, met, lep_phi, met_phi):
    
    d_phi = delta_phi(lep_phi, met_phi)
    
    m_t = np.sqrt(2*(lep_e)*(met)*(1-np.cos(d_phi))) 
    
    return m_t

def calc_weight(weight_variables, events, luminosity):
    total_weight = cfg.luminosity * 1000 / events["sum_of_weights"]
    for var in weight_variables:
        total_weight = total_weight * abs(events[variable])
    return total_weight