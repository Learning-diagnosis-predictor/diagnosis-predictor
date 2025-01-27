def build_nvld(data):

    vci = "WISC,WISC_VCI"
    vsi = "WISC,WISC_VSI"
    assq = "ASSQ,ASSQ_Total"
    word = "WIAT,WIAT_Word_P"
    cbcl = "CBCL,CBCL_SP_T"
    num = "WIAT,WIAT_Num_P"
    flanker = "NIH_Scores,NIH7_Flanker_P"
    card = "NIH_Scores,NIH7_Card_P"
        
    # Step 1
    spacial_condition = (data[vci] - data[vsi]) > 15 
    reading_condition = data[word] >= 16
    step_1_condition = spacial_condition & reading_condition
    
    # Step 2
    EF_condition = (data[flanker] < 16) | (data[card] < 16)
    social_condition = (data[cbcl] >= 70)
    math_condition = (data[num] <= 16)
    step2_condition = (social_condition.astype(int) + math_condition.astype(int) + EF_condition.astype(int)) >= 2

    # Step 3
    asd_condition = data[assq] < 19
    step_3_condition = asd_condition
    
    return step_1_condition & step2_condition & step_3_condition

def make_new_diag_cols(data):

    # Create new diganosis columns: positive if consensus diagnosis is positive OR if WIAT or WISC score is within range
    data["New Diag.Specific Learning Disorder with Impairment in Reading"] = (data["WIAT,WIAT_Word_Stnd"] < 85) & (data["WISC,WISC_FSIQ"] > 70)
    data["New Diag.Specific Learning Disorder with Impairment in Mathematics"] = (data["WIAT,WIAT_Num_Stnd"] < 85) & (data["WISC,WISC_FSIQ"] > 70)
    data["New Diag.Specific Learning Disorder with Impairment in Written Expression"] = (data["WIAT,WIAT_Spell_Stnd"] < 85)  & (data["WISC,WISC_FSIQ"] > 70)
    data["New Diag.Intellectual Disability-Mild"] = (data["WISC,WISC_FSIQ"] < 70) 
    data["New Diag.Borderline Intellectual Functioning"] = ((data["WISC,WISC_FSIQ"] < 85) & (data["WISC,WISC_FSIQ"] > 70))
    data["New Diag.Processing Speed Deficit"] = (data["WISC,WISC_PSI"] < 85) 
    data["New Diag.NVLD"] = build_nvld(data)
    
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
    print(data["New Diag.NVLD"].value_counts())
    print(data["New Diag.Specific Learning Disorder with Impairment in Reading - Consensus"].value_counts())
    print(data["New Diag.Specific Learning Disorder with Impairment in Mathematics - Consensus"].value_counts())
    print(data["New Diag.Intellectual Disability-Mild - Consensus"].value_counts())
    print(data["New Diag.Borderline Intellectual Functioning - Consensus"].value_counts())
    print(data["New Diag.Specific Learning Disorder with Impairment in Written Expression - Consensus"].value_counts())

    return data