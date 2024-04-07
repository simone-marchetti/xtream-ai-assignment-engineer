from flask import Response, request, Flask
from flask_restful import Resource, Api
from catboost import CatBoostRegressor
import json
import pandas as pd
import numpy as np

app = Flask(__name__)
api = Api(app)

#load model
model = CatBoostRegressor()
model.load_model("best_model")

training_columns = ['log_carat', 'cut', 'color', 'clarity', 'log_x', 'log_y', 'log_z',
       'log_z-depth', 'log_table_width']

class Predict(Resource):

    @staticmethod
    def post():
        try:
            query_parameters: list | dict = request.get_json()
            
            if isinstance(query_parameters, dict):
                query_parameters: dict = {k: [v] for k, v in query_parameters.items()}
                data: pd.DataFrame = pd.DataFrame.from_dict(query_parameters)
            elif isinstance(query_parameters, list):
                data: pd.DataFrame = pd.DataFrame.from_records(query_parameters)

            data["z-depth"] = data["depth"]*data["z"]/100
            data["table_width"] = data["table"]*data["x"] / 100

            for col in ["carat","x","y","z", "z-depth","table_width"]:
                 data.loc[:, f"log_{col}"] = np.log(data[col])

            predictions = np.exp(model.predict(data=data[training_columns]))
            response_data = {'prediction': predictions.tolist()}

            return Response(response=json.dumps(response_data), status=200, mimetype='application/json')
        
        except Exception as e:
            return Response(response=json.dumps({'error': str(e)}), status=400, mimetype='application/json')
        

# Add the resource to the API with the specified route
api.add_resource(Predict, '/predict')

if __name__ == '__main__':
    app.run(debug=True)