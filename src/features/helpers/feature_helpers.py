import pandas as pd

def get_possibly_numeric_cols(df):  
    # Return a list of columns that can be sucfessfully converted to numeric

    valid_numeric_columns = []
    for column in df.columns:
        try:
            pd.to_numeric(df[column])
            valid_numeric_columns.append(column)
        except ValueError:
            pass

    return valid_numeric_columns
