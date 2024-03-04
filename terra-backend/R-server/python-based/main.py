import numpy as np
import pandas as pd
import datetime

from flask import Flask,request,jsonify
from flask_cors import CORS

import_file_path = "/data/comext_imp.csv"
export_file_path =  "/data/comext_exp.csv"
c_data = pd.DataFrame()

def load_comext(file_path):
    db = pd.read_csv(file_path, dtype={"cpa": str})
    print(f"Loaded file {file_path}")
    return db

def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

def data_function(import_data, export_data, flow, var_cpa, country_code, partner_code, dataType, tipo_var):
    global c_data
    if flow == "1":
        c_data = import_data
    elif flow == "2":
        c_data = export_data    
    # User selects a UE country, global partner, cpa
    c_data = c_data[(c_data['DECLARANT_ISO'] == country_code) &
                (c_data['PARTNER_ISO'] == partner_code) &
                (c_data['cpa'] == var_cpa)]
    
    # User selects whether data is in value or quantity
    if tipo_var == "1":
        c_data = c_data[['PERIOD', 'val_cpa']]
    elif tipo_var == "2":
        c_data = c_data[['PERIOD', 'q_kg']]

    c_data.columns = ['PERIOD', 'series']

    if len(c_data['series']) > 0:
        # Format dates for sorting
        c_data['year'] = c_data['PERIOD'].astype(str).str[:4].astype(int)
        c_data['month'] = c_data['PERIOD'].astype(str).str[-2:].astype(int)

        # Sort the dataset
        c_data.sort_values(['year', 'month'], inplace=True)
        # Create date column
        c_data['date'] = pd.to_datetime(c_data['year'].astype(str) + '-' + c_data['month'].astype(str) + '-01')

        # Create date range for comparison
        start_date = datetime.datetime(c_data['year'].iloc[0], c_data['month'].iloc[0], 1)
        end_date = datetime.datetime(c_data['year'].iloc[-1], c_data['month'].iloc[-1], 1)
        date_full = pd.date_range(start=start_date, end=end_date, freq='MS')
        
        # Select necessary columns
        c_data = c_data[['date', 'series']]

        # Compare for missing months
        if len(c_data['date']) < len(date_full):
            db_full = pd.DataFrame({'date': date_full})
            c_data = pd.merge(c_data, db_full, how='outer')

        # Sort the dataset
        c_data.sort_values('date', inplace=True)

        # Calculate Yearly Variation Series if dataType is 1
        if dataType == "1":
            c_data['series_prev'] = c_data['series'].shift(12)
            c_data['series'] = c_data['series'] - c_data['series_prev']
            c_data = c_data.dropna(subset=['series'])
            c_data = c_data[['date','series']]
    
    dict_c_data = { "date": list(c_data["date"].dt.strftime("%Y-%m-%d")), "series": list(c_data["series"].astype(float))}
    return dict_c_data


def itsa(import_data, export_data, flow, var_cpa, country_code, partner_code, dataType, tipo_var):
    try:
        # Create a dictionary to store the results for return
        res_dict = {}

        # Load the dataset
        data_result = data_function(import_data, export_data, flow, var_cpa, country_code, partner_code, dataType, tipo_var)
        series_data = data_result['series']

        # Check if the dataset is empty, generate error code 00 if true
        status_main = "01" if len(series_data) > 0 and ~any(np.isnan(val) for val in series_data) else "00"
        res_dict["statusMain"] = status_main
        res_dict["diagMain"] = data_result

        # Check for missing values
        #len_diff = 1 if sum(pd.isna(series_data)) >= 1 else 0
#
        #if len_diff == 0 and status_main == "01":
        #    ############################ ACF Plot
        #    acf_list = {}
        #    acf_result = plt.acorr(series_data, maxlags=len(series_data)-1, detrend=lambda x: x.mean(), usevlines=False)
        #    acf_list["lne_y"] = acf_result[1]
        #    acf_list["lne_x"] = np.arange(0, len(series_data))
        #    conf_int_pos = 1.96 / np.sqrt(len(series_data) - 12)
        #    acf_list["dsh_y_pos"] = [conf_int_pos] * len(acf_list["lne_x"])
        #    acf_list["dsh_x_pos"] = acf_list["lne_x"]
        #    acf_list["dsh_y_neg"] = [-conf_int_pos] * len(acf_list["lne_x"])
        #    acf_list["dsh_x_neg"] = acf_list["lne_x"]
#
        #    res_dict["diagACF"] = acf_list
        #    res_dict["statusACF"] = ["01"]
#
        #    ############################ QQ-plot
        #    qq_result = probplot(series_data, plot=None)
        #    pnt_x = qq_result[0][0]
        #    pnt_y = qq_result[0][1]
#
        #    # Find 1st and 3rd quartile of data
        #    y = np.percentile(series_data, [25, 75])
        #    # Find the 1st and 3rd quartile of the normal distribution
        #    x = np.percentile(np.random.normal(size=len(series_data)), [25, 75])
        #    # Compute the intercept and slope of the line that passes through these points
        #    slope = np.diff(y) / np.diff(x)
        #    intercept = y[0] - slope * x[0]
#
        #    lne_y = intercept + slope * pnt_x
        #    lne_x = pnt_x
        #    normal = pd.DataFrame({"pnt_x": pnt_x, "pnt_y": pnt_y, "lne_x": lne_x, "lne_y": lne_y})
#
        #    res_dict["diagNorm"] = normal
        #    res_dict["statusNorm"] = ["01"]
#
        #else:
        #    res_dict["statusACF"] = ["00"]
        #    res_dict["statusNorm"] = ["00"]

        return res_dict

    except Exception as e:
        res_dict = {
            "statusMain": ["00"],
            #"statusACF": ["00"],
            #"statusNorm": ["00"],
            "error": str(e)
        }
        return res_dict


COMEXT_IMP = load_comext(import_file_path)
COMEXT_EXP = load_comext(export_file_path)

app = Flask(__name__)
CORS(app, resources=r'/*')

@app.route('/ts', methods=['GET'])
def itsa_route():
    flow = request.args.get('flow')
    var = request.args.get('var')
    country = request.args.get('country')
    partner = request.args.get('partner')
    dataType = request.args.get('dataType')
    tipovar = request.args.get('tipovar') # cambiare da tipovar a vartype

    resp = itsa(COMEXT_IMP, COMEXT_EXP, flow, var, country, partner, dataType, tipovar)
    response = jsonify(resp)
    response.content_type = "application/json"
    return add_cors(response)

if __name__ == '__main__':
    IP='0.0.0.0'
    port=5500
    app.run(host=IP, port=port)
