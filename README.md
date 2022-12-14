# learning-diagnosis-predictor

Use-case of https://github.com/charlie42/diagnosis-predictor.
Predicting learning diagnoses from HBN that have both consensus diagnosis and corresponding WISC and WAIS scores:
- Specific Learning Disorder with Impairment in Reading
- Specific Learning Disorder with Impairment in Mathematics
- Intellectual Disability-Mild
- Borderline Intellectual Functioning

## 1 step:

`python -W ignore src/data/make_dataset.py SCARED_SR`

Arguments: first_assessment_to_drop

## 2 step:

`python -W ignore src/models/train_models.py 0.02 1 0`

Arguments: performance_margin = 0.02, use_other_diags_as_input = 1, models_from_file = 1

## 3 step:

`python -W ignore src/models/evaluate_original_models.py 0.8 1`

Arguments: auc_threshold = 0.8, use_test_set=1

## 4 step:

`python -W ignore src/models/identify_feature_subsets.py 50`

Arguments: number_of_features_to_check = 50

## 5 step

`python -W ignore src/models/evaluate_models_on_feature_subsets.py 1`

Arguments: models_from_file = 1

