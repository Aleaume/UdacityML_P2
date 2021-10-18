from azureml.core import Workspace
from azureml.core.webservice import Webservice

# Requires the config to be downloaded first to the current working directory
ws = Workspace.from_config()

# Set with the deployment name
name = "myservice"

# load existing web service
service = AciWebservice(name=name, workspace=ws)
logs = service.get_logs()

for line in logs.split('\n'):
    print(line)

#SOURCE / HELP: https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.core.webservice.aci.aciwebservice?view=azure-ml-py
#Resubmission: I udpated the service object to get the right constructor of AciWebservice and not previously Webservice