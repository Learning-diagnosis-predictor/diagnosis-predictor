import os, datetime

def get_params_from_current_data_dir_name(current_data_dir_name):

    # Get paramers from the dir name created by train_models.py. Format: "[DATETIME]__first_param_1__second_param_TRUE"

    # Remove the last underscore
    current_data_dir_name = current_data_dir_name[:-1]
    
    # Split the string on the triple underscores
    parts = current_data_dir_name.split("___")
    
    # The first element is the datetime, so we can ignore it
    # The remaining elements are the parameters, so we can assign them to a list
    params = parts[1:]
    
    # Initialize an empty dictionary to store the param names and values
    param_dict = {}
    
    # Iterate through the list of params
    for param in params:
        # Split the param on the underscore to separate the name from the value
        print(param.rsplit("__", 1))
        name, value = param.rsplit("__", 1)
        
        # Add the name and value to the dictionary
        param_dict[name] = value
    
    # Return the dictionary
    return param_dict

<<<<<<< HEAD
<<<<<<< HEAD
=======
def get_newest_dir_in_dir(path):
    dir_names = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    # Find dir with the latest timestamp, dir name format: 2023-01-05 11.03.00___first_dropped_assessment__ICU_P___other_diag_as_input__0___debug_mode__True
    print(dir_names[0].split("___")[0])
    timestamps = [d.split("___")[0] for d in dir_names]
    timestamps = [datetime.datetime.strptime(t, "%Y-%m-%d %H.%M.%S") for t in timestamps]
    newest_dir_name = dir_names[timestamps.index(max(timestamps))]
    return path + newest_dir_name + "/"

>>>>>>> 94f6b6d (dir with latest timestamp instead of latest dir (to take into account git pulls))
=======
>>>>>>> 2129726 (fix special characters in diag file names)
def get_newest_non_empty_dir_in_dir(path):
    dir_names = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    non_empty_dir_names = [d for d in dir_names if len(os.listdir(path+d)) > 0]
    # Find non-empty dir with the latest timestamp, dir name format: 2023-01-05 11.03.00___first_dropped_assessment__ICU_P___other_diag_as_input__0___debug_mode__True
    
    timestamps = [d.split("___")[0] for d in non_empty_dir_names]
    timestamps = [datetime.datetime.strptime(t, "%Y-%m-%d %H.%M.%S") for t in timestamps]
    newest_dir_name = non_empty_dir_names[timestamps.index(max(timestamps))]
    return path + newest_dir_name + "/"