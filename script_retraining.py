from catboost import CatBoostRegressor, Pool
import pandas as pd
import numpy as np
import os
import argparse
from logger import logger
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

parser = argparse.ArgumentParser()
parser.add_argument("--iterations", type=int, help="an integer number")
parser.add_argument("--max_depth", type=int, help="an integer number")
parser.add_argument("--learning_rate", type=int, help="an integer number")
parser.add_argument("--model", type=str, help="location of previous model")
parser.add_argument("--data", type=str, help="location of new data")
parser.add_argument("--output_location", type=str, help="location of output model")
args = parser.parse_args()

params = {"iterations":1000, "max_depth":6} ## init some parameters in case they are not provided

if args.iterations is not None:
    params["iterations"] = args.iterations

if args.max_depth is not None:
    params["max_depth"] = args.max_depth

if args.learning_rate is not None:
    params["learning_rate"] = args.learning_rate


current_model: str = args.model
old_model = None
new_model = CatBoostRegressor(**params)
logger.info(f" New model initialized with trianing parameters {params}")

#CHECK THE EXISTENCE OF A PRETRAINED MODEL
if current_model is not None and os.path.exists(current_model):
    old_model = CatBoostRegressor()
    old_model.load_model(current_model)
    logger.info(f" Loaded previous model from {current_model}")
else:
    logger.warning(" No model found to continue training from")

## LOADING NEW DATA
data_path: str = args.data
data: None | pd.DataFrame = None
if data_path is None:
    raise Exception(f"No data location provided")
else:
    if data_path[-4:] != ".csv":
        raise Exception(f"The location {data_path} is not correct file, please provide a csv extensions")
    else:
        data = pd.read_csv(data_path)


## TRAINING PHASE
columns = ['carat', 'cut', 'color', 'clarity', 'depth', 'table', 'price', 'x', 'y',
       'z']

if data is not None:
    _common_columns: set = set(data.columns).intersection(set(columns))

    if len(_common_columns) < len(columns):
        raise ValueError(f"Missing columns in the provided data: {set(columns) - _common_columns}")
    
    logger.info("Initialize preprocessing")
    data = data[~(data["price"] < 1)]
    data = data[~((data["x"] == 0) | (data["y"] == 0) | (data["z"] == 0))]

    data["z-depth"] = data["depth"]*data["z"]/100
    data["table_width"] = data["table"]*data["x"] / 100
    
    for col in ["carat","x","y","z", "z-depth","table_width","price"]:
        data.loc[:, f"log_{col}"] = np.log(data[col])
    logger.info("Done preprocessing")

    x = data[['log_carat', 'cut', 'color', 'clarity', 'log_x', 'log_y', 'log_z',
       'log_z-depth', 'log_table_width']]
    y = data["log_price"]

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=.2)

    cat_features=[col for col in x.columns if x[col].dtype == "O"]

    test_pool = Pool(X_test, y_test, cat_features)

    logger.info("Start training")

    new_model.fit(
        x,
        y,
        eval_set=test_pool,
        cat_features=cat_features,
        use_best_model=True,
        early_stopping_rounds=20,
        verbose=False,
        init_model=old_model)
    
    y_hat = new_model.predict(X_test)
    mse = mean_squared_error(np.exp(y_test), np.exp(y_hat))
    mae = mean_absolute_error(np.exp(y_test), np.exp(y_hat))
    logger.info(f"Trained model results: mse {mse:.4f}, rmse {np.sqrt(mse):.4f}, mae {mae:.4f}")

    if (_location := args.output_location) is not None:
        new_model.save_model(fname=_location, format="cbm")
        logger.info(f"Model saved in {_location}")
    else:
        base_path = "./model"
        model_num = 1
        while True:
            model_path: str = f"{base_path}_{model_num}"
            if not os.path.exists(model_path):
                break
            else:
                model_num += 1
        new_model.save_model(fname=model_path, format="cbm")
        logger.info(f"No provided location, model saved in {model_path}")
    
    



