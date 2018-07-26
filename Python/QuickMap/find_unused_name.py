import os

def find_unused_name(folder, prefix, search_adjacent_folders = False):
    """ Finds config and exp file names that don't already exist """
    # Check folder existance
    if not os.path.isdir(folder):
        return 0, [], []

    # Build subfolders list to search into
    parent = os.path.dirname(folder)
    if search_adjacent_folders:
        subfolders = [subfolder for subfolder in os.listdir(parent) if os.path.isdir(os.path.join(parent,subfolder))]
    else:
        subfolders = [os.path.basename(folder)]

    # Check existance one by one
    findex = 0
    exists = True
    while exists:
        findex += 1
        config_paths = [os.path.join(parent,subfolder,prefix+'_config_'+str(findex)+'.h5') for subfolder in subfolders]
        exp_paths = [os.path.join(parent,subfolder,prefix+'_exp_'+str(findex)+'.h5') for subfolder in subfolders]
        exists = any([os.path.isfile(path) for path in config_paths+exp_paths])

    # Build and return result paths
    config_path = os.path.join(folder,prefix+'_config_'+str(findex)+'.h5')
    exp_path = os.path.join(folder,prefix+'_exp_'+str(findex)+'.h5')
    
    return findex, config_path, exp_path