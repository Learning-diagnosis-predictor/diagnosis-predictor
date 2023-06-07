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

def transform_pre_int_cols(data):
    
    data = data.drop(["PreInt_EduHx,NeuroPsych", "PreInt_EduHx,IEP", "PreInt_EduHx,learning_disability"], axis=1)
    # Previous diagnoses and meds: drop DX cols in PreInt_TxHx, drop _dose cols
    data = data.drop([x for x in data.columns if "PreInt_TxHx,Past_DX" in x], axis=1)
    data = data.drop([x for x in data.columns if "_dose" in x], axis=1)
    # Drop everything from PreInt_Lang except Child_Lang1_Age, Child_Lang2_Age, Child_Lang3_Age
    data = data.drop([x for x in data.columns if "PreInt_Lang" in x and x not in ["Child_Lang1_Age", "Child_Lang2_Age", "Child_Lang3_Age"]], axis=1)
    data = data.drop("PreInt_FamHx_RDC,caregiver_relation", axis=1) 


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
    data['PreInt_DevHx,birthweight_ozs'] = data['PreInt_DevHx,birthweight_lbs'] * 16 + data['PreInt_DevHx,birthweight_ozs']
    data = data.drop(["PreInt_DevHx,birthweight_lbs"], axis=1)

    
    # Replce weird no-response flags with nans in PreInt_FamHx_RDC
    cols = [x for x in data.columns if "PreInt_FamHx_RDC" in x]
    for col in cols:
        # Replace 99 and 999 with NaN
        data.loc[data[col].astype(str).isin(["99", "999", "9999"]), col] = np.nan # Replace 99 and 999 with NaN


    # Aggregate PreInt_FamHx_RDC between relatives
    # Aggregate between parents
    prefixes = ["PreInt_FamHx_RDC,"+x for x in["f", "m", "sib1", "sib2", "sib3", "sib4", "sib5"]]
    num_cols_with_prefixes = [x for x in features.get_possibly_numeric_cols(data) if x.startswith(tuple(prefixes)) and 
                                                                                 not x.endswith(tuple(["info", "age", "height", "weight"]))]
    postfixes = []
    for prefix in prefixes:
        postfixes += [x.replace(prefix, "") for x in num_cols_with_prefixes if x.startswith(prefix)]
    print("Postfixes to aggregate: ", postfixes)
    # Take average of columns with the same postfix over all relatives (prefixes)
    
    for postfix in postfixes:
        # Aggregate between grand-grand-parents
        cols_to_aggregate_ggp = [x for x in num_cols_with_prefixes if 
                                                              x.endswith(postfix) and
                                                              x.startswith(tuple(["PreInt_FamHx_RDC,mmm",     
                                                                            "PreInt_FamHx_RDC,mmf",
                                                                            "PreInt_FamHx_RDC,mfm",
                                                                            "PreInt_FamHx_RDC,mff",
                                                                            "PreInt_FamHx_RDC,fmm",
                                                                            "PreInt_FamHx_RDC,fmf",
                                                                            "PreInt_FamHx_RDC,ffm",
                                                                            "PreInt_FamHx_RDC,fff"])) and 
                                                                            x in data.columns]
        data["PreInt_FamHx_RDC," + postfix + "_MEAN_grandgrandparents"] = data[cols_to_aggregate_ggp].mean(axis=1)
        data = data.drop([x for x in cols_to_aggregate_ggp], axis=1)
        # Aggregate between grand-parents
        cols_to_aggregate_gp = [x for x in num_cols_with_prefixes if
                                                                x.endswith(postfix) and 
                                                                x.startswith(tuple(["PreInt_FamHx_RDC,mm",
                                                                            "PreInt_FamHx_RDC,mf",
                                                                            "PreInt_FamHx_RDC,fm",
                                                                            "PreInt_FamHx_RDC,ff"])) and 
                                                                            x in data.columns] # didn't drop yet
        data["PreInt_FamHx_RDC," + postfix + "_MEAN_grandparents"] = data[cols_to_aggregate_gp].mean(axis=1)
        data = data.drop([x for x in cols_to_aggregate_gp], axis=1)
        # Aggregate between parents and sibling (all that are rest)
        cols_to_aggregate_p = [x for x in num_cols_with_prefixes if 
                                                                x.endswith(postfix) and
                                                                x in data.columns] # didn't drop yet
        data["PreInt_FamHx_RDC," + postfix + "_MEAN_parents"] = data[cols_to_aggregate_p].mean(axis=1)
        data = data.drop([x for x in cols_to_aggregate_p], axis=1)
    # Aggregate between siblings
                                                        
    
    # Remove all columns containing age over 125
    cols = [x for x in data.columns if "Age" in x or "age" in x and not "language" in x and not "skill_age" in x] #Skill ages are in months
    for col in cols:
        data[col] = pd.to_numeric(data[col], errors='coerce') 
        data.loc[data[col] > 125, col] = np.nan


    # Remove outliers from columns that look numerical in PreInt
    from scipy import stats
    cols = [x for x in data.columns if "PreInt" in x]
    cols = features.get_possibly_numeric_cols(data[cols])
    data[cols] = data[cols].apply(pd.to_numeric)

    print(cols)
    
    # Print the valid columns
    print(stats.zscore(data[['PreInt_DevHx,skill_age_01', 'PreInt_DevHx,skill_age_02']], axis=1, nan_policy='omit'))
    #print((np.abs(stats.zscore(data[cols], nan_policy='omit')) < 3).all(axis=1))
    #data[cols][(np.abs(stats.zscore(data[cols], nan_policy='omit')) < 3).all(axis=1)]
    # Print outliers to check
    #data[cols][~(np.abs(stats.zscore(data[cols], nan_policy='omit')) < 3).all(axis=1)]

    return data