from modules.py_server_functions import DataLoading

def data_loading(logger, paths: dict, filenames: dict, labels: dict, column_names: dict, dtypes: dict, product_digits: int):
    data_loader = DataLoading(logger=logger, paths=paths, labels=labels, column_names=column_names, dtypes=dtypes)
    
    dfs, info = {}, {}
    for filename in filenames.values():
        df = data_loader.load_data(filename=filename, product_digits=product_digits)
        dfs[filename], info[filename] = df
    
    return dfs, info