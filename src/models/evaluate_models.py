import os
os.environ["PYTHONWARNINGS"] = "ignore::UserWarning" # Seems to be the only way to suppress multi-thread sklearn warnings

import math
import pandas as pd
import numpy as np
import sys

from sklearn.metrics import confusion_matrix, roc_auc_score, roc_curve
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score

# Calculate probability threshold
def calculate_threshold(classifier, X_train_train, y_train_train, X_val, y_val, b):
    from numpy import nanargmax

    # Fit model on train set
    classifier.fit(X_train_train, y_train_train)
    
    # Get predicted probabilities values
    y_val_pred_prob = classifier.predict_proba(X_val)

    # calculate roc curve
    fpr, tpr, thresholds = roc_curve(y_val, y_val_pred_prob[:,1])

    # calculate the g-mean for each threshold
    gmeans = np.sqrt(tpr * (1-fpr))
    
    # locate the index of the largest g-mean
    ix = nanargmax(gmeans)
    
    threshold = thresholds[ix]
    
    return threshold

# Find best thresholds
def find_best_thresholds(beta, best_classifiers, datasets):
    best_thresholds = {}
    for diag in datasets.keys():
        print("Finding best threshold for", diag)
        best_classifier_for_diag = best_classifiers[diag]
        X_train_train, y_train_train, X_val, y_val = \
            datasets[diag]["X_train_train"], \
            datasets[diag]["y_train_train"], \
            datasets[diag]["X_val"], \
            datasets[diag]["y_val"]
        threshold = calculate_threshold(
            best_classifier_for_diag, 
            X_train_train, y_train_train, X_val, y_val, 
            beta
        )
        best_thresholds[diag] = threshold
    print(best_thresholds)
    return best_thresholds

def get_matrix_metrics(real_values,pred_values,beta):
    CM = confusion_matrix(real_values,pred_values)
    TN = CM[0][0]+0.01 # +0.01 To avoid division by 0 errors
    FN = CM[1][0]+0.01
    TP = CM[1][1]+0.01
    FP = CM[0][1]+0.01
    Population = TN+FN+TP+FP
    Prevalence = round( (TP+FN) / Population,2)
    Accuracy   = round( (TP+TN) / Population,4)
    Precision  = round( TP / (TP+FP),4 )
    NPV        = round( TN / (TN+FN),4 )
    FDR        = round( FP / (TP+FP),4 )
    FOR        = round( FN / (TN+FN),4 ) 
    check_Pos  = Precision + FDR
    check_Neg  = NPV + FOR
    Recall     = round( TP / (TP+FN),4 )
    FPR        = round( FP / (TN+FP),4 )
    FNR        = round( FN / (TP+FN),4 )
    TNR        = round( TN / (TN+FP),4 ) 
    check_Pos2 = Recall + FNR
    check_Neg2 = FPR + TNR
    LRPos      = round( Recall/FPR,4 ) 
    LRNeg      = round( FNR / TNR ,4 )
    #DOR        = round( LRPos/LRNeg)
    DOR        = 1 # FIX, LINE ABOVE
    F1         = round ( 2 * ((Precision*Recall)/(Precision+Recall)),4)
    FBeta      = round ( (1+beta**2)*((Precision*Recall)/((beta**2 * Precision)+ Recall)) ,4)
    MCC        = round ( ((TP*TN)-(FP*FN))/math.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))  ,4)
    BM         = Recall+TNR-1
    MK         = Precision+NPV-1   
    Predicted_Positive_Ratio = round( (TP+FP) / Population,2)
    
    mat_met = [TP,TN,FP,FN,Prevalence,Accuracy,Precision,NPV,FDR,FOR,check_Pos,check_Neg,Recall,FPR,FNR,TNR,check_Pos2,check_Neg2,LRPos,LRNeg,DOR,F1,FBeta,MCC,BM,MK,Predicted_Positive_Ratio]
    metric_names = ['TP','TN','FP','FN','Prevalence','Accuracy','Precision','NPV','FDR','FOR','check_Pos','check_Neg','Recall (Sensitivity)','FPR','FNR','TNR (Specificity)','check_Pos2','check_Neg2','LR+','LR-','DOR','F1','FBeta','MCC','BM','MK','Predicted Positive Ratio','ROC AUC']   

    return (mat_met, metric_names)

def get_metrics(classifier, threshold, X, y, beta):
       
    y_pred_prob = classifier.predict_proba(X)
    y_pred = (y_pred_prob[:,1] >= threshold).astype(bool) 

    metrics, metric_names = get_matrix_metrics(y, y_pred, beta=beta)

    roc_auc = roc_auc_score(y, y_pred_prob[:,1])
    metrics.append(roc_auc)
    
    return metrics, metric_names

def add_number_of_positive_examples(results, datasets):
    for diag in datasets:
        full_dataset_y = datasets[diag]["y_train"].append(datasets[diag]["y_test"]) # Reconstruct full dataset from train and test
        results.loc[results["Diag"] == diag, "# of Positive Examples"] = full_dataset_y.sum()
    return results

def check_performance(best_classifiers, datasets, best_thresholds, scores_of_best_classifiers, beta, use_test_set=False):
    results = []
    for diag in datasets.keys():
        print(diag)
        classifier = best_classifiers[diag]
        threshold = best_thresholds[diag]
        if use_test_set:
            X, y = datasets[diag]["X_test"], datasets[diag]["y_test"]
        else:
            X, y = datasets[diag]["X_val"], datasets[diag]["y_val"]

        metrics, metric_names = get_metrics(classifier, threshold, X, y, beta)
        
        results.append([
            diag, 
            *metrics])

    results = pd.DataFrame(results, columns=["Diag"]+metric_names)
    results = add_number_of_positive_examples(results, datasets)

    return results.sort_values(by="ROC AUC", ascending=False)

def get_auc_cv_from_grid_search(reports_dir):
    auc_cv_from_grid_search = pd.read_csv(reports_dir + "df_of_best_classifiers_and_their_scores.csv")
    auc_cv_from_grid_search = auc_cv_from_grid_search[["Diag", "Best score", "SD of best score", "Score - SD"]]
    auc_cv_from_grid_search.columns = ["Diag", "ROC AUC Mean CV", "ROC AUC SD CV", "ROC AUC Mean CV - SD"]
    return auc_cv_from_grid_search

# Get diagnoses with good performance
def find_well_performing_diags(results, min_roc_auc_cv):
    well_performing_diags = results[
        (results["ROC AUC Mean CV"] >= min_roc_auc_cv)
    ]["Diag"].values
    return well_performing_diags

def main(beta = 3, performance_margin = 0.02, auc_threshold = 0.8):

    # Need this to be able to import local packages
    import sys, os, inspect
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)
    import models, data

    beta = float(beta)
    performance_margin = float(performance_margin)
    auc_threshold = float(auc_threshold)

    models_dir = "models/"
    data_processed_dir = "data/processed/"
    reports_dir = "reports/"

    full_dataset = pd.read_csv(data_processed_dir + "item_lvl_w_impairment.csv")

    from joblib import load
    best_classifiers = load(models_dir+'best-classifiers.joblib')
    scores_of_best_classifiers = load(models_dir+'scores-of-best-classifiers.joblib')
    sds_of_scores_of_best_classifiers = load(models_dir+'sds-of-scores-of-best-classifiers.joblib')

    # Get list of column names with "Diag: " prefix, where ROC AUC is over threshold and variance under threshold
    # ROC AUC reference: https://gpsych.bmj.com/content/gpsych/30/3/207.full.pd
    diag_cols = [x for x in sds_of_scores_of_best_classifiers.keys() if  
                sds_of_scores_of_best_classifiers[x] <= performance_margin and 
                scores_of_best_classifiers[x] >= auc_threshold]
    print("Diagnoses that passed the threshold: ")
    print(diag_cols)

    datasets = data.create_datasets(full_dataset, diag_cols)

    # Find best probability thresholds for each diagnosis
    best_thresholds = find_best_thresholds(
            beta=beta, 
            best_classifiers=best_classifiers, 
            datasets=datasets
    )
    from joblib import dump
    dump(best_thresholds, models_dir+'best-thresholds.joblib', compress=1)

    # Print performances of models on validation set
    roc_auc_cv_from_grid_search = get_auc_cv_from_grid_search(reports_dir)
    performance_table = check_performance(best_classifiers, datasets, best_thresholds, scores_of_best_classifiers, beta=beta, use_test_set=False)
    performance_table = performance_table.merge(roc_auc_cv_from_grid_search, on="Diag")
    print(performance_table[['Diag','Recall (Sensitivity)','TNR (Specificity)','ROC AUC Mean CV']].sort_values("ROC AUC Mean CV"))
    performance_table.to_csv(reports_dir+"performance_table_all_features.csv", index=False)    

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])