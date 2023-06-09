import sys, os, inspect
import pandas as pd
import numpy as np

# To import from parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import features

def make_new_diag_cols(data):

    # Create new diganosis columns: positive if consensus diagnosis is positive OR if WIAT or WISC score is within range
    data["New Diag.Specific Learning Disorder with Impairment in Reading"] = (data["WIAT,WIAT_Word_Stnd"] < 85) & (data["WISC,WISC_FSIQ"] > 70)
    data["New Diag.Specific Learning Disorder with Impairment in Mathematics"] = (data["WIAT,WIAT_Num_Stnd"] < 85) & (data["WISC,WISC_FSIQ"] > 70)
    data["New Diag.Specific Learning Disorder with Impairment in Written Expression"] = (data["WIAT,WIAT_Spell_Stnd"] < 85)  & (data["WISC,WISC_FSIQ"] > 70)
    data["New Diag.Intellectual Disability-Mild"] = (data["WISC,WISC_FSIQ"] < 70) 
    data["New Diag.Borderline Intellectual Functioning"] = ((data["WISC,WISC_FSIQ"] < 85) & (data["WISC,WISC_FSIQ"] > 70))
    data["New Diag.Processing Speed Deficit"] = (data["WISC,WISC_PSI"] < 85) 
    

    data["New Diag.Specific Learning Disorder with Impairment in Reading - Consensus"] = (data["Diag.Specific Learning Disorder with Impairment in Reading"] == 1)
    data["New Diag.Specific Learning Disorder with Impairment in Mathematics - Consensus"] = (data["Diag.Specific Learning Disorder with Impairment in Mathematics"] == 1)
    data["New Diag.Intellectual Disability-Mild - Consensus"] = (data["Diag.Borderline Intellectual Functioning"] == 1)
    data["New Diag.Borderline Intellectual Functioning - Consensus"] = (data["Diag.Intellectual Disability-Mild"] == 1)
    data["New Diag.Specific Learning Disorder with Impairment in Written Expression - Consensus"] = (data["Diag.Specific Learning Disorder with Impairment in Written Expression"] == 1) # No task for written expression
    

    print("New diagnosis columns positive value counts:")
    print(data["New Diag.Specific Learning Disorder with Impairment in Reading"].value_counts())
    print(data["New Diag.Specific Learning Disorder with Impairment in Mathematics"].value_counts())
    print(data["New Diag.Specific Learning Disorder with Impairment in Written Expression"].value_counts())
    print(data["New Diag.Intellectual Disability-Mild"].value_counts())
    print(data["New Diag.Borderline Intellectual Functioning"].value_counts())
    print(data["New Diag.Processing Speed Deficit"].value_counts())
    print(data["New Diag.Specific Learning Disorder with Impairment in Reading - Consensus"].value_counts())
    print(data["New Diag.Specific Learning Disorder with Impairment in Mathematics - Consensus"].value_counts())
    print(data["New Diag.Intellectual Disability-Mild - Consensus"].value_counts())
    print(data["New Diag.Borderline Intellectual Functioning - Consensus"].value_counts())
    print(data["New Diag.Specific Learning Disorder with Impairment in Written Expression - Consensus"].value_counts())

    return data

def replace_with_dict_otherwise_nan(data, cols, dict):
    for col in cols:
        data.loc[~data[col].isin(dict.keys()), col] = np.nan # Replace any other possible values with NaN
        data[col] = data[col].astype(str).replace(dict)
    return data

def one_hot_encode_cols(data, cols):
    for col in cols:
        print("One hot encoding " + col)
        print("Number of columns before encoding: " + str(len(data.columns)))
        dummies = pd.get_dummies(data[col], prefix=col)
        data = pd.concat([data, dummies], axis=1)
        print("Number of columns after encoding: " + str(len(data.columns)))
        data = data.drop(col, axis=1)
        print("Number of columns after dropping original col: " + str(len(data.columns)))
    return data

def aggregate_pre_int_famhx_rdc(data):

    # Number of siblings - how many osib1age is not NaN
    data["PreInt_FamHx_RDC,NumSibs"] = (data["PreInt_FamHx_RDC,osib1age"].notnull().astype(int) + 
                                        data["PreInt_FamHx_RDC,osib2age"].notnull().astype(int) +   
                                        data["PreInt_FamHx_RDC,osib3age"].notnull().astype(int) +       
                                        data["PreInt_FamHx_RDC,osib4age_2"].notnull().astype(int) +       
                                        data["PreInt_FamHx_RDC,osib5age"].notnull().astype(int))          

    # Columns to aggregate

    prefixes = ["PreInt_FamHx_RDC,"+x for x in["f", "m", "sib1", "sib2", "sib3", "sib4", "sib5"]]
    postfixes = ["dxsev", "attempts", "hospit"]
    cols_to_agg = [x+y for x in prefixes for y in postfixes if x+y in data.columns]

    for postfix in postfixes:
        # Aggregate between parents and sibling 
        cols_to_agg_postfix = [x for x in cols_to_agg if postfix in x and x in data.columns]
        data["PreInt_FamHx_RDC," + postfix + "_MEAN_parents_siblings"] = data[cols_to_agg_postfix].astype(float).mean(axis=1)

        data = data.drop([x for x in cols_to_agg_postfix], axis=1)

    # Columns to keep as is
    rdc_cols_to_keep = [
        ["PreInt_FamHx_RDC,osib1sex", "PreInt_FamHx_RDC,osib1age", "PreInt_FamHx_RDC,omoves1", "PreInt_FamHx_RDC,omoves2", "PreInt_FamHx_RDC,omoves3", "PreInt_FamHx_RDC,ocare1", "PreInt_FamHx_RDC,ocare2", "PreInt_FamHx_RDC,ocare3"] + 
        [x for x in data.columns if "MEAN_parents_siblings" in x] + 
        ["PreInt_FamHx_RDC,NumSibs"]]
    cols_to_drop = [x for x in data.columns if x.startswith("PreInt_FamHx_RDC,") and x not in rdc_cols_to_keep]
    data = data.drop(cols_to_drop, axis=1)

    return data

def transform_pre_int_lang(data):

    # How many languages the child speaks since birth
    data["PreInt_Lang,NumLangs"] = data[["PreInt_Lang,Child_Lang1_Life",
                                         "PreInt_Lang,Child_Lang2_Life",
                                         "PreInt_Lang,Child_Lang3_Life"]].sum(axis=1)

    # Drop the rest of the language columns
    data = data.drop([x for x in data.columns if "PreInt_Lang," in x and not x == "PreInt_Lang,NumLangs"], axis=1)

    return data

def transform_pre_int_cols(data):

    data = data.drop(["PreInt_EduHx,NeuroPsych", "PreInt_EduHx,IEP", "PreInt_EduHx,learning_disability"] + # Self-evident
                     [x for x in data.columns if "PreInt_TxHx,Past_DX" in x] + # Could be learning disability
                     [x for x in data.columns if "_dose" in x], axis=1)
    

    # Tansform PreInt_Lang
    data = transform_pre_int_lang(data)


    # One hot encode categorical cols
    cols = ([x for x in data.columns if x.startswith("PreInt_Demos_Fam") and x.endswith("_Race")] +
            [x for x in data.columns if x.startswith("PreInt_Demos_Fam") and "_Relation" in x] + 
            ["PreInt_Demos_Fam,guardian_maritalstatus"] +
            [x for x in data.columns if "_Setting" in x and x.startswith("PreInt_Lang")]
    )
    data = one_hot_encode_cols(data, cols)

    
    # Transform PreInt_DevHx,skill_range_X cols into a number (Early or early=-1, Normal or normal=0, Late or late=1, other=NaN)
    cols = [x for x in data.columns if "PreInt_DevHx,skill_range_" in x]   
    dict = {"Early": -1, "early": -1, "Normal": 0, "normal": 0, "Late": 1, "late": 1}  
    replace_with_dict_otherwise_nan(data, cols, dict)

    # Clearn PreInt_FamHx_RDC cols: in *alive cols, replace everything that is not 1 or 2 with NaN
    cols = [x for x in data.columns if "PreInt_FamHx_RDC" in x and "alive" in x]
    dict = {"1": 1, "2": 2}
    data = replace_with_dict_otherwise_nan(data, cols, dict)

    # Transform rel quality columns
    cols = [x for x in data.columns if "_RelQuality" in x or "RelQual" in x or "_quality" in x]
    dict = {"Excellent": 4, "Good": 3, "Fair": 2, "Poor": 1, "excellent": 4, "good": 3, "fair": 2, "poor": 1}  
    data = replace_with_dict_otherwise_nan(data, cols, dict)
    
    # Exchange 2 and 3 in PreInt_EduHx,current_religious, more logical order
    cols = ["PreInt_EduHx,current_religious"]
    dict = {"1": 1, "2": 3, "3": 2}
    data = replace_with_dict_otherwise_nan(data, cols, dict)

    # PreInt_Demos_Fam,X_Ethnicity: replace 2 and 3 with NaN
    cols = [x for x in data.columns if x.startswith("PreInt_Demos_Fam,") and x.endswith("Ethnicity")]
    dict = {"0": 0, "1": 1}
    data = replace_with_dict_otherwise_nan(data, cols, dict)
    
    
    # Transform height to inches
    cols = [x for x in data.columns if "_Height_Ft" in x]
    for ft_col in cols:
        inch_col = ft_col.replace("_Ft", "_In")
        # Convert height to inches
        data[ft_col] = data[ft_col].astype('Int64')
        data[inch_col] = data[inch_col].astype('Int64')
        data[inch_col] = data[ft_col] * 12 + data[inch_col]
        data = data.drop(ft_col, axis=1)

    # Transform weight to lbs
    data['PreInt_DevHx,birthweight_ozs'] = data['PreInt_DevHx,birthweight_lbs'].astype(float) * 16 + data['PreInt_DevHx,birthweight_ozs'].astype(float)    
    data = data.drop(["PreInt_DevHx,birthweight_lbs"], axis=1)

    
    # Replce weird no-response flags with nans in PreInt_FamHx_RDC
    cols = [x for x in data.columns if "PreInt_FamHx_RDC" in x]
    for col in cols:
        # Replace 99, 999, 9999 with NaN
        data.loc[data[col].astype(str).isin(["99", "999", "9999"]), col] = np.nan # Replace with NaN


    data = aggregate_pre_int_famhx_rdc(data)
                                                        
    
    # Remove all values with age over 125
    cols = [x for x in data.columns if "Age" in x or "age" in x and not "language" in x and not "skill_age" in x] #Skill ages are in months
    for col in cols:
        data[col] = pd.to_numeric(data[col], errors='coerce') 
        data.loc[data[col] > 125, col] = np.nan

    # Set negative values in PreInt_Demos_Fam,Married_Yrs col to NaN
    data.loc[data["PreInt_Demos_Fam,Married_Yrs"].astype(float) < 0, "PreInt_Demos_Fam,Married_Yrs"] = np.nan
    

    # Take average of parent height, weight, age (PreInt_Demos_Fam,P2_Weight, PreInt_Demos_Fam,P1_Weight; PreInt_Demos_Fam,P1_Height_In, PreInt_Demos_Fam,P2_Height_In, PreInt_Demos_Fam,P1_Age, PreInt_Demos_Fam,P2_Age)
    cols = [x for x in data.columns if "PreInt_Demos_Fam,P1_" in x and "Weight" in x or "PreInt_Demos_Fam,P2_" in x and "Weight" in x]
    data["PreInt_Demos_Fam,Parent_Weight"] = data[cols].astype(float).mean(axis=1)
    
    cols = [x for x in data.columns if "PreInt_Demos_Fam,P1_" in x and "Height" in x or "PreInt_Demos_Fam,P2_" in x and "Height" in x]
    data["PreInt_Demos_Fam,Parent_Height"] = data[cols].astype(float).mean(axis=1)

    cols = [x for x in data.columns if "PreInt_Demos_Fam,P1_" in x and "Age" in x or "PreInt_Demos_Fam,P2_" in x and "Age" in x]
    data["PreInt_Demos_Fam,Parent_Age"] = data[cols].astype(float).mean(axis=1)
    
    return data