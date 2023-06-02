# learning-diagnosis-predictor

Use-case of https://github.com/charlie42/diagnosis-predictor.
Predicting learning diagnoses from HBN:
- Specific Learning Disorder with Impairment in Reading
- Specific Learning Disorder with Impairment in Mathematics
- Specific Learning Disorder with Impairment in Written Expression
- Intellectual Disability-Mild
- Borderline Intellectual Functioning
- Processing Speed Deficit 
- NVLD

## 1 step:

`python -W ignore src/data/create_datasets.py 0 CCSC 0 0`

Arguments: only_assessment_distribution, first_assessment_to_drop, use_other_diags_as_input = 0, only_free_assessments = 0

## 2 step:

`python -W ignore src/models/train_models.py 0.02 0`

Arguments: performance_margin = 0.02, models_from_file = 1

## 3 step:

`python -W ignore src/models/evaluate_original_models.py 1`

Arguments: use_test_set=1

## 4 step:

`python -W ignore src/models/identify_feature_subsets.py 126 0`

Arguments: number_of_features_to_check = 126, importances_from_file = 0

## 5 step

`python -W ignore src/models/evaluate_models_on_feature_subsets.py 0`

Arguments: models_from_file = 1

