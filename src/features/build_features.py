def make_new_diag_cols(data, diag_cols):

    # Create new diganosis columns: positive if consensus diagnosis is positive OR if WIAT or WISC score is within range
    data["New Diag.Specific Learning Disorder with Impairment in Reading"] = (data["WIAT,WIAT_Word_Stnd"] < 85) | (data["Diag.Specific Learning Disorder with Impairment in Reading"] == 1)
    data["New Diag.Specific Learning Disorder with Impairment in Mathematics"] = (data["WIAT,WIAT_Num_Stnd"] < 85) | (data["Diag.Specific Learning Disorder with Impairment in Mathematics"] == 1)
    data["New Diag.Intellectual Disability-Mild"] = (data["WISC,WISC_FSIQ"] < 70) | (data["Diag.Borderline Intellectual Functioning"] == 1)
    data["New Diag.Borderline Intellectual Functioning"] = ((data["WISC,WISC_FSIQ"] < 85) & (data["WISC,WISC_FSIQ"] > 70)) | (data["Diag.Intellectual Disability-Mild"] == 1)
    data["New Diag.Specific Learning Disorder with Impairment in Written Expression"] = (data["Diag.Specific Learning Disorder with Impairment in Written Expression"] == 1) # No task for written expression

    print("New diagnosis columns positive value counts:")
    print(data["New Diag.Specific Learning Disorder with Impairment in Reading"].value_counts())
    print(data["New Diag.Specific Learning Disorder with Impairment in Written Expression"].value_counts())
    print(data["New Diag.Specific Learning Disorder with Impairment in Mathematics"].value_counts())
    print(data["New Diag.Intellectual Disability-Mild"].value_counts())
    print(data["New Diag.Borderline Intellectual Functioning"].value_counts())

    return data