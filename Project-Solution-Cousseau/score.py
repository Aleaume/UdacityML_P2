#ENTRY SCRIPT
#The entry script receives data submitted to a deployed web service and passes it to the model. 
# It then returns the model's response to the client. The script is specific to your model. 
# The entry script must understand the data that the model expects and returns.

#make sure file "score.py" is placed in the directory : "./source_dir"

import json


def init():
    print("This is init")


def run(data):
    test = json.loads(data)
    print(f"received data {test}")
    return f"test is {test}"

#SOURCE / HELP :https://docs.microsoft.com/en-us/azure/machine-learning/how-to-deploy-and-where?tabs=python