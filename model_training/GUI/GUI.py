import gradio as gr
import xgboost as xgb
import numpy as np
import joblib
import os  # Add file existence check

# Precious metal list and corresponding optimization methods
model_list = ['Au', 'Ag', 'Pd', 'Pt', 'Rh']
op_list = ['baye', 'Grid', 'baye', 'baye', 'Random']
model_save_name = 'XGBoost'

# Initialize model list (fix _estimator_type core issue)
models = []
for i in range(5):
    # 1. Build model file name with correct path
    model_load_name = f'XGBoost_R-{model_list[i]}_{op_list[i]}.json'
    print(f"Attempting to load model file: {model_load_name}")
    
    # 2. Check if file exists
    if not os.path.exists(model_load_name):
        raise FileNotFoundError(f"Model file does not exist: {model_load_name}")
    
    # 3. Correctly load XGBoost model (preserve scikit-learn interface attributes)
    # Step 1: Create XGBRegressor instance
    model = xgb.XGBRegressor()
    # Step 2: Load Booster model first (underlying model)
    booster = xgb.Booster()
    booster.load_model(model_load_name)
    # Step 3: Associate booster with XGBRegressor instance (key: preserve _estimator_type attribute)
    model._Booster = booster
    # Step 4: Explicitly set _estimator_type (double guarantee)
    model._estimator_type = "regressor"
    
    models.append(model)

def predict(*inputs):
    try:
        # 1. Convert input to numpy array, ensure correct dimensions
        inputs_tmp = np.array(inputs, dtype=np.float32).reshape(1, -1)
        # 2. Initialize prediction results
        predictions = [model.predict(inputs_tmp)[0] for model in models]
        
        # 3. Set corresponding prediction values to zero based on precious metal content in input (correct index correspondence)
        # Last 5 elements in input list are: Au, Ag, Pd, Pt, Rh
        au_idx = -5  # Position of Au in input
        ag_idx = -4  # Position of Ag in input
        pd_idx = -3  # Position of Pd in input
        pt_idx = -2  # Position of Pt in input
        rh_idx = -1  # Position of Rh in input
        
        if inputs[au_idx] == 0:
            predictions[0] = 0.0
        if inputs[ag_idx] == 0:
            predictions[1] = 0.0
        if inputs[pd_idx] == 0:
            predictions[2] = 0.0
        if inputs[pt_idx] == 0:
            predictions[3] = 0.0
        if inputs[rh_idx] == 0:
            predictions[4] = 0.0
        
        # 4. Format output (keep 4 decimal places, improve readability)
        return [f"{pred:.4f}" for pred in predictions]
    
    except Exception as e:
        # Exception handling: return error message for debugging
        return [f"Prediction error: {str(e)}"] * 5

# Create Gradio interface (fixed Na2B4O7 variable name error)
with gr.Blocks(css="""
    .header {
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
        height: 100px;
    }
    .logo {
        position: absolute;
        top: 50%;
        right: 10px;
        transform: translateY(-50%);
        max-width: 80px;
        max-height: 150px;
    }
    .content {
        margin-top: 40px;
    }
    .section-title {
        text-align: center;
        font-size: 1.2em;
        font-weight: bold;
    }
    .dataframe th, .dataframe td {
        text-align: center;
    }
    .custom-slider label {
        font-weight: bold;
    }
""") as demo:
    # Title and Logo
    with gr.Row(elem_classes="header"):
        gr.Markdown("<h1 style='font-size: 2.0em; text-align: center; margin: 0;'>Intelligent Prediction System for Precious Metals Smelting in Urban Mines</h1>")
        gr.Image("GUI/LOGO.png", elem_id="logo", show_label=False, elem_classes="logo")

    # Main content area
    with gr.Row(elem_classes="content"):
        with gr.Column(scale=3):
            gr.Markdown("<h1 style='text-align: center; background-color: #F5DEB3;'>Feed Composition</h1>")
            with gr.Row():
                # Metal parameters
                with gr.Column(scale=1.0):
                    gr.Markdown("<h2 style='text-align: center;'>Metals</h2>")
                    Ag = gr.Slider(label="Ag (ppm)", minimum=0, maximum=50100, step=1)
                    Au = gr.Slider(label="Au (ppm)", minimum=0, maximum=1667, step=1)
                    Bi = gr.Slider(label="Bi (%)", minimum=0, maximum=14, step=0.01)
                    Co = gr.Slider(label="Co (%)", minimum=0, maximum=1, step=0.01)
                    Cu = gr.Slider(label="Cu (%)", minimum=0, maximum=175, step=0.01)
                    Fe = gr.Slider(label="Fe (%)", minimum=0, maximum=129, step=0.01)
                    Ni = gr.Slider(label="Ni (%)", minimum=0, maximum=13, step=0.01)
                    Pb = gr.Slider(label="Pb (%)", minimum=0, maximum=34, step=0.01)
                    Pd = gr.Slider(label="Pd (ppm)", minimum=0, maximum=9500, step=1)
                    Pt = gr.Slider(label="Pt (ppm)", minimum=0, maximum=1780, step=1)
                    Rh = gr.Slider(label="Rh (ppm)", minimum=0, maximum=285, step=1)
                    Sb = gr.Slider(label="Sb (%)", minimum=0, maximum=5, step=0.01)
                    Sn = gr.Slider(label="Sn (%)", minimum=0, maximum=9, step=0.01)

                # Non-metal parameters (fixed Na2B4O7 variable name error)
                with gr.Column(scale=1.0):
                    gr.Markdown("<h2 style='text-align: center;'>Non-Metals</h2>")
                    with gr.Row():
                        with gr.Column(scale=1.0):
                            Al2O3 = gr.Slider(label="Al2O3 (%)", minimum=0, maximum=100, step=0.01)
                            BaO = gr.Slider(label="BaO (%)", minimum=0, maximum=40, step=0.01)
                            C = gr.Slider(label="C (%)", minimum=0, maximum=20, step=0.01)
                            CaBr2 = gr.Slider(label="CaBr2 (%)", minimum=0, maximum=3, step=0.01)
                            CaCl2 = gr.Slider(label="CaCl2 (%)", minimum=0, maximum=3, step=0.01)
                            CaF2 = gr.Slider(label="CaF2 (%)", minimum=0, maximum=30, step=0.01)
                            CaO = gr.Slider(label="CaO (%)", minimum=0, maximum=116, step=0.01)
                            CuO = gr.Slider(label="CuO (%)", minimum=0, maximum=45, step=0.01)
                            FeO = gr.Slider(label="FeO (%)", minimum=0, maximum=46, step=0.01)
                            Fe2O3 = gr.Slider(label="Fe2O3 (%)", minimum=0, maximum=40, step=0.01)
                            Fe3O4 = gr.Slider(label="Fe3O4 (%)", minimum=0, maximum=34, step=0.01)
                            FeS2 = gr.Slider(label="FeS2 (%)", minimum=0, maximum=60, step=0.01) 
                            K2O = gr.Slider(label="K2O (%)", minimum=0, maximum=1, step=0.01)
                        with gr.Column(scale=1.0):
                            La2O3 = gr.Slider(label="La2O3 (%)", minimum=0, maximum=2, step=0.01)
                            MgO = gr.Slider(label="MgO (%)", minimum=0, maximum=14, step=0.01)
                            MnO = gr.Slider(label="MnO (%)", minimum=0, maximum=2, step=0.01)
                            Na2B4O7 = gr.Slider(label="Na2B4O7 (%)", minimum=0, maximum=23, step=0.01)  # Fixed variable name
                            Na2O = gr.Slider(label="Na2O (%)", minimum=0, maximum=27, step=0.01)
                            SiO2 = gr.Slider(label="SiO2 (%)", minimum=0, maximum=232, step=0.01)
                            SnO2 = gr.Slider(label="SnO2 (%)", minimum=0, maximum=4, step=0.01)
                            TiO2 = gr.Slider(label="TiO2 (%)", minimum=0, maximum=20, step=0.01)
                            ZrO2 = gr.Slider(label="ZrO2 (%)", minimum=0, maximum=17, step=0.01)
        
        # Smelting conditions and prediction area
        with gr.Column(scale=1.0):
            gr.Markdown("<h1 style='text-align: center; background-color: #F5DEB3;'>Smelting Condition</h1>")
            gr.Markdown("<h2 style='text-align: center;'>Smelting</h2>")
            temperature = gr.Slider(label="Temperature (℃)", minimum=0, maximum=2000, step=1)
            duration = gr.Slider(label="Duration (h)", minimum=0, maximum=24, step=1)
            
            gr.Markdown("<h1 style='text-align: center; background-color: #ADD8E6;'>Prediction</h1>")
            prediction_button = gr.Button("Predict")
            prediction_outputs = [gr.Textbox(label=metal) for metal in ["Au (%)", "Ag (%)", "Pd (%)", "Pt (%)", "Rh (%)"]]
    
    # Input parameter list (synchronized fix for Na2B4O7 variable name)
    inputs = [
        CaO, Al2O3, SiO2, MgO, BaO, FeO, Fe2O3, Fe3O4, FeS2, K2O,
        Na2O, ZrO2, MnO, TiO2, La2O3, SnO2, Na2B4O7, CaF2, CaCl2, CaBr2,
        Bi, Sn, Pb, Sb, Co, Cu, CuO, Ni, Fe, C, temperature, duration,
        Au, Ag, Pd, Pt, Rh
    ]
    
    # Bind prediction button event
    prediction_button.click(predict, inputs, prediction_outputs)

# Launch Gradio application (add share=False to avoid public link, debug=True for debugging)
demo.launch(debug=True, share=False)