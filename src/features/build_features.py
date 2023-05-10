def make_new_diag_cols(data, diag_cols):

    # Create new diganosis columns: positive if consensus diagnosis is positive OR if WIAT or WISC score is within range
    data["New Diag.Specific Learning Disorder with Impairment in Reading"] = (data["WIAT,WIAT_Word_Stnd"] < 85) | ((data["Diag.Specific Learning Disorder with Impairment in Reading"] == 1) & (data["WISC,WISC_FSIQ"] > 70))
    data["New Diag.Specific Learning Disorder with Impairment in Mathematics"] = (data["WIAT,WIAT_Num_Stnd"] < 85) | ((data["Diag.Specific Learning Disorder with Impairment in Mathematics"] == 1) & (data["WISC,WISC_FSIQ"] > 70)) 
    data["New Diag.Intellectual Disability-Mild"] = (data["WISC,WISC_FSIQ"] < 70) | (data["Diag.Borderline Intellectual Functioning"] == 1)
    data["New Diag.Borderline Intellectual Functioning"] = ((data["WISC,WISC_FSIQ"] < 85) & (data["WISC,WISC_FSIQ"] > 70)) | (data["Diag.Intellectual Disability-Mild"] == 1)
    data["New Diag.Specific Learning Disorder with Impairment in Written Expression"] = (data["Diag.Specific Learning Disorder with Impairment in Written Expression"] == 1) # No task for written expression
    data["New Diag.Processing Speed Deficit"] = (data["WISC,WISC_PSI"] < 85) 
    print(data["WISC,WISC_VCI"].dtype, data["WISC,WISC_VSI"].dtype, data["WIAT,WIAT_Word_P"].dtype, data["CBCL,CBCL_SP_T"].dtype, data["WIAT,WIAT_Num_P"].dtype, data["ASSQ,ASSQ_Total"].dtype)
    print(data["WISC,WISC_VCI"].describe(), data["WISC,WISC_VSI"].describe(), (data["WISC,WISC_VCI"] - data["WISC,WISC_VSI"]).describe(), data["WIAT,WIAT_Word_P"].describe(), data["CBCL,CBCL_SP_T"].describe(), data["WIAT,WIAT_Num_P"].describe(), data["ASSQ,ASSQ_Total"].describe())
    #data["New Diag.NVLD"] = ((data["WISC,WISC_VCI"] - data["WISC,WISC_VSI"]) > 15) & (data["ASSQ,ASSQ_Total"] < 19) & ((data["WIAT,WIAT_Word_P"] <= 16) | (data["CBCL,CBCL_SP_T"] >= 70) | (data["WIAT,WIAT_Num_P"] <= 16))
    #print((((data["WISC,WISC_VCI"] - data["WISC,WISC_VSI"]) > 15) & (data["ASSQ,ASSQ_Total"] < 19)).value_counts())
    data["New Diag.NVLD"] = ((data["WISC,WISC_VCI"] - data["WISC,WISC_VSI"]) > 15) & (data["ASSQ,ASSQ_Total"] < 19)

    print("New diagnosis columns positive value counts:")
    print(data["New Diag.Specific Learning Disorder with Impairment in Reading"].value_counts())
    print(data["New Diag.Specific Learning Disorder with Impairment in Written Expression"].value_counts())
    print(data["New Diag.Specific Learning Disorder with Impairment in Mathematics"].value_counts())
    print(data["New Diag.Intellectual Disability-Mild"].value_counts())
    print(data["New Diag.Borderline Intellectual Functioning"].value_counts())
    print(data["New Diag.Processing Speed Deficit"].value_counts())
    print(data["New Diag.NVLD"].value_counts())

    return data