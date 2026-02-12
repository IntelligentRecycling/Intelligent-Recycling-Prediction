import pandas as pd
import numpy as np


# Read Excel file
import os
file_path = os.path.join(os.path.dirname(__file__), 'data-thermodynamic.xlsx')
data = pd.read_excel(file_path, engine="openpyxl")

# Define metal classification
transition_metals = ['Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'La', 'Ce', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg']
non_transition_metals = ['Li', 'Be', 'Na', 'Mg', 'Al', 'Si', 'K', 'Ca', 'Ga', 'Ge', 'As', 'Se', 'Rb', 'In', 'Sn', 'Sb', 'Te', 'Cs', 'Ba', 'Tl', 'Pb', 'Bi']


def get_phase(phases,tmp_phase_list):

    if tmp_phase_list[-1] =="Gas" and phases[-1]=="Alloy":
        phases[-1] = "Gas"
    
    if 'Alloy' in phases:
        tmp = 'Alloy'
    elif 'Slag' in phases:
        tmp = 'Slag'
    elif all(phase == "Others" for phase in phases):
        tmp = "Others"
    else:
        tmp = 'Gas'

    return tmp

#### Calculate H and R for one collector and one other element
def thermodynamic_model(metal_list, elements_list, T,P,data,transition_metals,non_transition_metals):
    # Initialize result dictionaries
    results_H = {}
    results_R = {}
    split_phase_results = {}

    # Iterate through each metal combination and each oxygen partial pressure and temperature
    for metal1 in ['Fe', 'Cu', 'Ni', 'Pb']:

        results_H[metal1] = {}
        results_R[metal1] = {}
        split_phase_results[metal1] = {}

        f1 = metal_list[metal1]
        for element2 in data['Element'].unique():

            if f1 == 0 or elements_list[element2] ==0:
                # Save H and R results
                results_H[metal1][(element2, P, T)] = 0
                results_R[metal1][(element2, P, T)] = 0
                split_phase_results[metal1][(element2, P, T)] = "Others"

            else:
                f2 = elements_list[element2] 
                # Assign parameters based on metal properties
                if (metal1 in transition_metals and element2 in transition_metals) or (metal1 in non_transition_metals and element2 in non_transition_metals):
                    alpha = 0
                    if metal1 in transition_metals and element2 in transition_metals:
                        p = 14.1
                    else:
                        p = 10.6
                else:
                    alpha = 0.73
                    p = 12.3

                q = 9.4  
                eta1 = data.loc[data['Element'] == metal1, 'η'].iloc[0]
                eta2 = data.loc[data['Element'] == element2, 'η'].iloc[0]
                phi1 = data.loc[data['Element'] == metal1, 'φ'].iloc[0]
                phi2 = data.loc[data['Element'] == element2, 'φ'].iloc[0]
                r1 = data.loc[data['Element'] == metal1, 'r'].iloc[0]
                r2 = data.loc[data['Element'] == element2, 'r'].iloc[0]
                V1 = data.loc[data['Element'] == metal1, 'V'].iloc[0]
                V2 = data.loc[data['Element'] == element2, 'V'].iloc[0]
                a1 = data.loc[data['Element'] == metal1, 'a'].iloc[0]
                b1 = data.loc[data['Element'] == metal1, 'b'].iloc[0]
                a2 = data.loc[data['Element'] == element2, 'a'].iloc[0]
                b2 = data.loc[data['Element'] == element2, 'b'].iloc[0]
                c2 = data.loc[data['Element'] == element2, 'c'].iloc[0]
                d2 = data.loc[data['Element'] == element2, 'd'].iloc[0]
                n = data.loc[data['Element'] == element2, 'n'].iloc[0]

                # Calculate I1 and I2
                Z1 = a1 + b1 / T
                Z2 = a2 + b2 / T
                I1 = 10 ** Z1
                I2 = 10 ** Z2

                # Calculate x1 and x2
                x1 = f1 / (f1 + f2)
                x2 = f2 / (f1 + f2)

                # Calculate A, B, C, D
                A = (eta1 - eta2) ** 2
                B = (phi1 - phi2) ** 2
                C = r1 * r2
                D = 1 / eta1 + 1 / eta2

                # Calculate U, W, E
                U = x2 * V2 * x1 * V1
                W = x2 * V2 + x1 * V1
                E = U / W

                # Calculate H
                H = (2 * E * p * (q * A - B - alpha * C)) / D *1000

                # Calculate J and K
                J = (1 - x2) * H / x2
                K = (H + J) / (8.314 * T)
                
                # Calculate γ2
                gamma2 = np.exp(K)

                # Calculate Ω
                Omega = np.log10(gamma2 * I2 / I1)

                # Calculate G2, O, Π
                G2 = c2 + d2 * T
                O = G2 / (19.14714 * T) + 0.0345
                Pi = n / 2 * np.log10(P) + np.log10(gamma2) - O

                # Calculate L and R
                L = 10 ** Pi
                R = f1 / (L * (1 - f1) + f1)
                        
                
                if element2 == "Cu" and P == 10**-10 and T==1673 :
                    print("X1: {}, X2: {}, A: {}, B: {}, C: {}, D: {}, U: {}, W: {}, E: {}, H: {}, J: {}, K: {}".format(x1,x2,A,B,C,D,U,W,E,H,J,K))
                    print("gamma2: {}, Omega: {}, G2: {}, O: {}, Pi: {}, L: {}, R: {}".format(gamma2, Omega, G2, O, Pi, L, R))
                
                # Save H and R results
                results_H[metal1][(element2, P, T)] = H
                results_R[metal1][(element2, P, T)] = R
                

                
                # Calculate theta
                theta = max(0, 4.01 - np.log10(I1))

                # Determine which phase the metal enters
                if Pi < 0 and Omega < theta:
                    phase = 'Alloy'
                elif Pi >= 0 and Omega < Pi + theta:
                    phase = 'Slag'
                else:
                    phase = 'Gas'
                split_phase_results[metal1][(element2, P, T)] = phase

    return results_H, results_R,split_phase_results
    
def merge(results_H, results_R,split_phase_results,P,T):
    print("===> :", results_R)
    
    R_merge = {}
    phase_merge = {}
    for element in data['Element'].unique():
        print("#####",element)
        R_data_merge =  1- ( (1-results_R['Cu'].get((element, P, T), None))*(1-results_R['Fe'].get((element, P, T), None))*(1-results_R['Ni'].get((element, P, T), None))*(1-results_R['Pb'].get((element, P, T), None)))
                    
        R_merge[element] = R_data_merge
        
        #### Phase diagrams of four metals, filter out those in Alloy phase
        tmp_phase_list = [split_phase_results['Cu'].get(('Cu', P, T), None) ,
                                split_phase_results['Fe'].get(('Fe', P, T), None),
                                split_phase_results['Ni'].get(('Ni', P, T), None),
                                split_phase_results['Pb'].get(('Pb', P, T), None)]
        
        element_phase_list = [split_phase_results['Cu'].get((element, P, T), None) ,
                                split_phase_results['Fe'].get((element, P, T), None),
                                split_phase_results['Ni'].get((element, P, T), None),
                                split_phase_results['Pb'].get((element, P, T), None)]


        print("collect_phase: ",tmp_phase_list )
        print("element_phase: ",element_phase_list)
        print("final_phase: ", element_phase_list)

        SP_data = get_phase(element_phase_list, tmp_phase_list)

        phase_merge[element] = SP_data
        # if element =="Pb":
        #     print("RRRRRR==>: ", results_R['Cu'].get((element, P, T), None),results_R['Fe'].get((element, P, T), None),results_R['Ni'].get((element, P, T), None),results_R['Pb'].get((element, P, T), None)    ,R_data_merge)
        #     print("PPPPPP==>: ", split_phase_results['Cu'].get((element, P, T), None),split_phase_results['Fe'].get((element, P, T), None),split_phase_results['Ni'].get((element, P, T), None),split_phase_results['Pb'].get((element, P, T), None),SP_data)
    return  R_merge,phase_merge