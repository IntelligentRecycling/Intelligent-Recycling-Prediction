from thermo_fun import *
import streamlit as st
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from xgboost import XGBRegressor
import numpy as np
import xgboost as xgb
from joblib import dump, load

st.set_page_config(page_title="Intelligent Recycling Strategy", layout="wide")

# Define the layout of the periodic table
elements = [
    ["H", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "He"],
    ["Li", "Be", "", "", "", "", "", "", "", "", "", "", "B", "C", "N", "O", "F", "Ne"],
    ["Na", "Mg", "", "", "", "", "", "", "", "", "", "", "Al", "Si", "P", "S", "Cl", "Ar"],
    ["K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr"],
    ["Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe"],
    ["Cs", "Ba", "La", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn"],
    ["Fr", "Ra", "Ac", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"],
    ["","","", "La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu"],
    ["","","", "Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr"],
]

condition = [["T","Pre","Time","", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",""]]

# Add custom CSS styles
st.markdown("""
    <style>
    .main .block-container {
        max-width: 100%;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .stTextInput {
        width: 80px;
        height: 60px;
    }
    </style>
    """, unsafe_allow_html=True)

# Create input and output components
input_values = {}
condition_values ={}
output_values = {}
phase_results = {}
background_colors ={}

# Create header for periodic table input
st.header("Intelligent Recycling Strategy Table-Inputs")

for row_idx, row in enumerate(elements):
    cols = st.columns(len(elements[0]))
    for col_idx, (col, element) in enumerate(zip(cols, row)):
        if element:
            input_values[element] = col.text_input(element, "0", key=f"input_{element}_{row_idx}_{col_idx}")
        else:
            col.markdown(" ")

# Create header for condition table
st.header("Conditions")

for row_idx, row in enumerate(condition):
    cols = st.columns(len(condition[0]))
    for col_idx, (col, element) in enumerate(zip(cols, row)):

        if element:
            element_name = element
            if element =="T":
                element_name =  element + "(K)"
            if element =="Pre":
                element_name =  element + "(atm)"
            if element =="Time":
                element_name =  element + "(s)"
            
            condition_values[element] = col.text_input(element_name, "0", key=f"condtion_{element}_{row_idx}_{col_idx}")
        else:
            col.markdown(" ")


# Define processing function
def process_elements():
    #### Model prediction
    metal_list = {}
    input_values_float ={}

    for element, value in input_values.items():
        try:
        # Try to convert input values to float
            input_values_float[element] = float(value)
        except ValueError:
            # If conversion fails, record error information
            input_values_float[element] = 0
    
    
    for metal1 in ['Fe', 'Cu', 'Ni', 'Pb']:
        metal_list[metal1] =  input_values_float[metal1]
    elements_list = input_values_float


    T = float(condition_values["T"])
    P = float(condition_values["Pre"])
    Time = float(condition_values["Time"])

    print(metal_list,elements_list,T,P,Time)
    
    results_H, results_R,split_phase_results = thermodynamic_model(metal_list, elements_list, T,P,data,transition_metals,non_transition_metals)

    R_merge,phase_merge = merge(results_H, results_R,split_phase_results,P,T)


    #### Predict debromination rate using machine learning model
    model_xgb_path ='XGBoost_Debromination_rate_Random.json'
    model_RF_path = 'RF_Debromination_rate_Grid.joblib'
    models_xgb = xgb.XGBRegressor() 
    models_RF = RandomForestRegressor()
    
    models  = models_RF
    model_path = model_RF_path
    if model_path == model_xgb_path:
        models.load_model(model_path)
    elif model_path == model_RF_path:
        models = load(model_path)


    model_input =[]

    for tmp in ['Na','Ba','Ca','Fe','Mg','Ti','Si','Al']:
        model_input.append(input_values_float[tmp])
    for con_elements in ["Time","T"]:
        if con_elements =="T" and  float(condition_values[con_elements]) > 873:
            model_input.append(min(float(condition_values[con_elements])-273,600))
        else:
            model_input.append(float(condition_values[con_elements])-273)
    
    prediction = models.predict(np.array(model_input).reshape(1, -1))[0]

    #### Calculate output
    for element_tmp in input_values.keys() :
        
        if element_tmp in data['Element'].unique():
            output_values[element_tmp] = str(R_merge[element_tmp])
            phase = phase_merge[element_tmp]
        else:
            output_values[element_tmp] = ""
            phase = "Others"

        # Update Br debromination rate
        if element_tmp == "Br":
            if input_values_float["Br"] == 0.0:
                output_values[element_tmp] = str(0)
            else:
                output_values[element_tmp] = str(prediction*0.01) # Convert to 0.0X format

        print(element_tmp, phase)

        color_capture = {"Cu": "#E6AF00", "Fe": "#FFD85B", "Ni": "#FFC305",  "Pb": "#FAE6A1" }
        # Assume metal names are consistent with the order in H value list
        capture = ['Cu', 'Fe', 'Ni', 'Pb']

        # Color based on phase separation results
        if phase == "Slag":
            color = "#A3C6D8"
        elif phase == "Alloy" :
            if  element_tmp  in capture:
                color = color_capture[element_tmp]
            else:      
                H_capture = [results_H['Cu'].get((element_tmp, P, T), None), 
                            results_H['Fe'].get((element_tmp, P, T), None),
                            results_H['Ni'].get((element_tmp, P, T), None),
                            results_H['Pb'].get((element_tmp, P, T), None)]
                
                #### Phase diagrams of four metals, filter out those in Alloy phase
                tmp_phase_list = [split_phase_results['Cu'].get(('Cu', P, T), None) ,
                                    split_phase_results['Fe'].get(('Fe', P, T), None),
                                    split_phase_results['Ni'].get(('Ni', P, T), None),
                                    split_phase_results['Pb'].get(('Pb', P, T), None)]
                
                indices = [i for i, value in enumerate(tmp_phase_list) if value == "Alloy"]

                # Extract elements from H_capture corresponding to indices
                H_values_for_alloys = [H_capture[i] for i in indices]

                # Find the minimum value among these values
                min_H_value = min(H_values_for_alloys)

                if min_H_value >= 0:
                    color = "#EADE3E"
                else:
                    # Get the metal name corresponding to the minimum value
                    min_index = H_capture.index(min_H_value)

                    min_H_metal = capture[min_index]
                    color = color_capture[min_H_metal]  
        elif phase == "Gas":
            color = "#F8CBAD"
        else:
            color = "#E7E6E6"
        
        
        # Update element background color
        background_colors[element_tmp] = color
        phase_results[element_tmp] = phase
            
    return output_values, background_colors, phase_results


# Update output table
st.empty()  # Add blank line
st.empty()  # Add another blank line

if st.button("Submit"):
    process_elements()

    # Update output table
    # Create header for condition table
    st.header("Intelligent Recycling Strategy Table-Outputs")
    for row_idx, row in enumerate(elements):
        cols = st.columns(len(row))
        for col_idx, (col, element) in enumerate(zip(cols, row)):
            if element:

                value = output_values.get(element, "")
                color = background_colors.get(element, "white")

                #### First check if phase is Alloy, then display
                if phase_results.get(element) !="Alloy" and element !="Br":
                    value = ""
                if element == "Br" and value !=str(0):
                    color = "#77ACC5"
                col.markdown(f"""
                        <div style="padding: 1px; text-align: center;">
                            <div style="font-weight: bold; text-align: left;">{element}</div>
                            <div style="background-color: {color}; padding: 1px; border-radius: 1px; margin-top: 1px;">
                                <input type="text" value="{value}" disabled style="width: 100%; border: none; background-color: {color}; text-align: center;">
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                col.markdown(" ")



