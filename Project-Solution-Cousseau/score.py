#ENTRY SCRIPT
#The entry script receives data submitted to a deployed web service and passes it to the model. 
# It then returns the model's response to the client. The script is specific to your model. 
# The entry script must understand the data that the model expects and returns.

#make sure file "score.py" is placed in the directory : "./source_dir"

import json


def init():
    print("This is init")
    model_path = Model.get_model_path("./")
    print("Model Path is:",model_path)
    model = joblib.load(model_path)

def run(data):
    data = json.loads(data)
    result = model.predict(data['data'])
    return {'data' : result.tolist() , 'message' : 'Successfully 
            predicted'}
   except Exception as e:
      error = str(e)
      return {'data' : error , 'message' : 'Failed to predict 
             '}
    print(f"received data {data}")
    return f"test is {test}"

#SOURCE / HELP :https://docs.microsoft.com/en-us/azure/machine-learning/how-to-deploy-and-where?tabs=python

#https://medium.com/daily-programming-tips/how-to-deploy-a-local-ml-model-as-a-web-service-on-azure-machine-learning-studio-5eb788a2884c
