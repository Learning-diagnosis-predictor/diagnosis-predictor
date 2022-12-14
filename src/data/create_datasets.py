from sklearn.model_selection import train_test_split

def get_cons_diag_col_name_from_new_diag(new_diag):
    return new_diag.replace("New Diag: ", "Diag: ")

def customize_input_cols_per_diag(input_cols, diag):
    # Remove "Diag: Intellectual Disability-Mild" when predicting "Diag: Borderline Intellectual Functioning"
    #   and vice versa because they are highly correlated, same for other diagnoses
    
    if diag == "New Diag: Intellectual Disability-Mild":
        input_cols = [x for x in input_cols if x not in ["New Diag: Borderline Intellectual Functioning", get_cons_diag_col_name_from_new_diag("New Diag: Borderline Intellectual Functioning")]]
    if diag == "New Diag: Borderline Intellectual Functioning":
        input_cols = [x for x in input_cols if x not in ["New Diag: Intellectual Disability-Mild", get_cons_diag_col_name_from_new_diag("New Diag: Intellectual Disability-Mild")]]
    
    return input_cols

def get_cons_diag_col_name_from_new_diag(new_diag):
    return new_diag.replace("New Diag: ", "Diag: ")

def get_input_and_output_cols_for_diag(full_dataset, diag, use_other_diags_as_input):
    
    if use_other_diags_as_input == 1:
        input_cols = [x for x in full_dataset.columns if 
                        not x in ["WHODAS_P,WHODAS_P_Total", "CIS_P,CIS_P_Score", "WHODAS_SR,WHODAS_SR_Score", "CIS_SR,CIS_SR_Total"]
                        and not x.startswith("WIAT")
                        and not x.startswith("WISC")
                        and not x == "Diag: No Diagnosis Given"
                        and not x.startswith("New Diag: ")
                        and not x == get_cons_diag_col_name_from_new_diag(diag)
                        and not x == diag]
    else:
        input_cols = [x for x in full_dataset.columns if 
                        not x in ["WHODAS_P,WHODAS_P_Total", "CIS_P,CIS_P_Score", "WHODAS_SR,WHODAS_SR_Score", "CIS_SR,CIS_SR_Total"]
                        and not x.startswith("WIAT")
                        and not x.startswith("WISC")
                        and not x == "Diag: No Diagnosis Given"
                        and not x.startswith("New Diag: ")
                        and not x == get_cons_diag_col_name_from_new_diag(diag)
                        and not x.startswith("Diag: ")]

    input_cols = customize_input_cols_per_diag(input_cols, diag)
    
    output_col = diag
    
    return input_cols, output_col

def create_datasets(full_dataset, diag_cols, split_percentage, use_other_diags_as_input):
    datasets = {}
    for diag in diag_cols:
        
        input_cols, output_col = get_input_and_output_cols_for_diag(full_dataset, diag, use_other_diags_as_input)
        
        # Split train, validation, and test sets
        X_train, X_test, y_train, y_test = train_test_split(full_dataset[input_cols], full_dataset[output_col], test_size=split_percentage, stratify=full_dataset[output_col], random_state=1)
        X_train_train, X_val, y_train_train, y_val = train_test_split(X_train, y_train, test_size=split_percentage, stratify=y_train, random_state=1)
    
        datasets[diag] = { "X_train": X_train,
                        "X_test": X_test,
                        "y_train": y_train,
                        "y_test": y_test,
                        "X_train_train": X_train_train,
                        "X_val": X_val,
                        "y_train_train": y_train_train,
                        "y_val": y_val}
    return datasets