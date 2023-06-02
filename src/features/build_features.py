def make_new_diag_cols(data):

    # Create new diganosis columns: positive if consensus diagnosis is positive OR if WIAT or WISC score is within range
    data["New Diag.Specific Learning Disorder with Impairment in Reading"] = (data["WIAT,WIAT_Word_Stnd"] < 85) & (data["WISC,WISC_FSIQ"] > 70)
    data["New Diag.Specific Learning Disorder with Impairment in Mathematics"] = (data["WIAT,WIAT_Num_Stnd"] < 85) & (data["WISC,WISC_FSIQ"] > 70)
    data["New Diag.Specific Learning Disorder with Impairment in Written Expression"] = (data["WIAT,WIAT_Spell_Stnd"] < 85) & (data["WISC,WISC_FSIQ"] > 70)
    data["New Diag.Intellectual Disability-Mild"] = data["WISC,WISC_FSIQ"] < 70
    data["New Diag.Borderline Intellectual Functioning"] = (data["WISC,WISC_FSIQ"] < 85) & (data["WISC,WISC_FSIQ"] > 70) 
    data["New Diag.Processing Speed Deficit"] = (data["WISC,WISC_PSI"] < 85) 

    # data["New Diag.Specific Learning Disorder with Impairment in Reading"] = data["Diag.Specific Learning Disorder with Impairment in Reading"]
    # data["New Diag.Specific Learning Disorder with Impairment in Mathematics"] = data["Diag.Specific Learning Disorder with Impairment in Mathematics"]
    # data["New Diag.Intellectual Disability-Mild"] = data["Diag.Intellectual Disability-Mild"]
    # data["New Diag.Borderline Intellectual Functioning"] = data["Diag.Borderline Intellectual Functioning"]
    # data["New Diag.Specific Learning Disorder with Impairment in Written Expression"] = data["Diag.Specific Learning Disorder with Impairment in Written Expression"] == 1 
    # data["New Diag.Processing Speed Deficit"] = (data["WISC,WISC_PSI"] < 85) 

    print("New diagnosis columns positive value counts:")
    print(data["New Diag.Specific Learning Disorder with Impairment in Reading"].value_counts())
    print(data["New Diag.Specific Learning Disorder with Impairment in Written Expression"].value_counts())
    print(data["New Diag.Specific Learning Disorder with Impairment in Mathematics"].value_counts())
    print(data["New Diag.Intellectual Disability-Mild"].value_counts())
    print(data["New Diag.Borderline Intellectual Functioning"].value_counts())
    print(data["New Diag.Processing Speed Deficit"].value_counts())

    return data