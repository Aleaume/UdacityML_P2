
# Udacity AZ ML Enginner Project #2 - Deploying Models & Pipelines - Q4 2021

## Requirements

  - Open Azure ML Studio & login.
  - Create a compute instance on which you will run your notebooks and scripts.
  - In order for the project & scripts to run, please make sure the Folder "Project-Solution-Cousseau" is uploaded.
  
## Overview

- Model deployment (details in Figure 1)
  - First, it picks up a public csv file with Bankmarketing data and creates a dataset in Azure.
  - Then an experiment is created to find the best model.
  - After registering this model, it is deployed and can be consumed via a test python script
  - In parallel, it uses the swagger.json file generated at deploy to visualize in a swagger page. The instance being set on a docker.
  - Also, a benchmark scripts calls on an apache instance to test the response time and performance of the deployed model.
  
- Pipeline publishing (Figure 2)
  - In the second part, we make use of the same computing cluster, to run again a similar experiment, and capture the best model.
  - We then create a pipeline from this model and publish it.
  - Via the jupyter notebook, we test and consume the endpoint for this pipeline.


## Architectural Diagram


![image](https://user-images.githubusercontent.com/32632731/137295084-66a93581-c82c-48d2-8124-01e174666a42.png)
Figure 1

![image](https://user-images.githubusercontent.com/32632731/137294914-430b8fe0-0bf2-4140-bfe7-0b28a65dd8e4.png)
Figure 2

## Key Steps

- Step #1: Environment set up => not necessary as I made use of the Udacity Lab with pre-installed tools
  - The only set-up / preparation activity was to create a compute instance (in order to run the Notebook See step #2)
  
- Step #2 : Create and run Auto ML Experiment => achieved using azure SDK for Python, see Notebook *project_2_udacity_Cousseau.ipynb*

  - First step up is to retrieve the current workspace
  ```python
      from azureml.core import Workspace, Experiment, Dataset
      #ws = Workspace.get(name="udacity-project")
      ws = Workspace.from_config()  
      # using the current workspace (Lab)  SOURCE: https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.core.workspace.workspace?view=azure-ml-py
      exp = Experiment(workspace=ws, name="udacity-project_2_Cousseau")
      print('Workspace name: ' + ws.name, 
            'Azure region: ' + ws.location, 
            'Subscription id: ' + ws.subscription_id, 
            'Resource group: ' + ws.resource_group, sep = '\n')
      run = exp.start_logging()
  ```
  
  - Then I created a compute cluster with the instructions given (Standard_DS12_V2, minimum 1 node)
  
  ```python
              cluster_name = "myCluster"
        try:
            cluster = ComputeTarget(workspace=ws, name=cluster_name)
            print("Cluster already created")
        except ComputeTargetException:
            compute_config = AmlCompute.provisioning_configuration(vm_size="STANDARD_DS12_V2",min_nodes=1, max_nodes=6)
            cluster = ComputeTarget.create(ws,cluster_name, compute_config) #creates the actual cluster
  ```
  
  ![image](https://user-images.githubusercontent.com/32632731/136262638-67d22fe3-864b-4136-b286-4de90d62e528.png)

  
  - Once done and running, we then load the Dataset from the url provided
  
  ![image](https://user-images.githubusercontent.com/32632731/136263292-3d06ebfe-ae89-415e-95a2-d5fce5ba9f43.png)

 - From there on, we setup a new AutoML experiment with the required constraint (Classification, Explain best Model, Exit after 1h, max concurrency to 5)
 ![image](https://user-images.githubusercontent.com/32632731/136699813-e0e10bab-b930-496a-869e-6e118f565244.png)

 
 - Once ran, we have a look at the results and display the best run for checking
  
  
 - Before we then jump to Step #3 we need to register the run as a Model.

 ![image](https://user-images.githubusercontent.com/32632731/136701920-e8fc31f0-126d-4f6f-9141-540078b465fe.png)
  ![image](https://user-images.githubusercontent.com/32632731/136269749-6aba90e5-f5d3-4fe2-9fe9-b54e0eedc777.png)

- Step #3: Deploy the Best Model => achieved using azure SDK for Python, see Notebook xxx
  - First we need to define the inference configuration
    ```python
                #Define inference configuration

                #score.py needs to be located in the same directory as this notebook. Otherwise update the source_directory variable

                from azureml.core import Environment
                from azureml.core.model import InferenceConfig

                env = Environment(name="Project 2 Udacity")
                my_inference_config = InferenceConfig(
                    environment=env,
                    source_directory="./",
                    entry_script="./score.py",
                )
    ```
   - And then we can deploy it to ACI
    
    ```python
    
                 #Deploy to ACI

              from azureml.core.webservice import AciWebservice

              deployment_config = AciWebservice.deploy_configuration(
                  cpu_cores=0.5, memory_gb=1, auth_enabled=True
              )

              service = model.deploy(
                  ws,
                  "myservice",
                  [model],
                  my_inference_config,
                  deployment_config,
                  overwrite=True,
              )
              service.wait_for_deployment(show_output=True)

              print(service.get_logs())
    
    ```
    
    ![image](https://user-images.githubusercontent.com/32632731/136702629-69a56ebd-a3ae-4b8e-a4e6-720fae86aea3.png)

    
- Step #4: Enable Logging

![image](https://user-images.githubusercontent.com/32632731/136274509-baedc330-1abd-4ed6-aa69-f3e769564cf3.png)

![image](https://user-images.githubusercontent.com/32632731/136275072-0086011c-ec4f-4f3c-bafd-df26560c7b90.png)


- Step #5: Swagger Documentation
  - Download swagger.json from Model just deployed and save it in the local swagger folder
  - Start git bash from this folder, and run swagger.sh
  ![image](https://user-images.githubusercontent.com/32632731/136704369-b2f8d709-9d79-4e0b-a025-2edfe11bdbde.png)
  - Once done, run serve.py
  
  ![image](https://user-images.githubusercontent.com/32632731/136705317-b98dcbeb-b943-4bf6-9868-97889e5a243a.png)

  - Finally we can display swagger documentation about the deployed model:
  
  ![image](https://user-images.githubusercontent.com/32632731/136705220-0e46204e-77f9-4b79-bdbc-9da58d0f9cba.png)
  ![image](https://user-images.githubusercontent.com/32632731/136705245-548c1be6-96b3-4b02-8a51-1cbe2fb8912a.png)


- Step #6: Consume Model Endpoints
  - From the consume tab of the deployed model we retrieve both the score ui & the key
  ![image](https://user-images.githubusercontent.com/32632731/136705380-e3b8e043-7ab3-4498-a925-ef54cdff75b6.png)

  - Then we make sure to add those in the endpoint.py script before running it
  
  ![image](https://user-images.githubusercontent.com/32632731/136706007-e8c8a3f5-93f9-4dac-ab61-621465595a1a.png)
  
- Optional - Benchmark the endpoint -
  - First we check that the Apache CLI tool is installed
  ![image](https://user-images.githubusercontent.com/32632731/137581361-3a4a34d8-42d7-479f-9ccb-d223f172f089.png)

  - We then update the URI and key in the endpoint.py and run the script
  - Last we run the benchmark.sh and check the results
  ![image](https://user-images.githubusercontent.com/32632731/137581917-28fbb43a-e781-4316-b655-7439042afe27.png)
  ![image](https://user-images.githubusercontent.com/32632731/137581932-4a4b1138-476f-4795-89e4-fd1bcb20a388.png)



- Step #7: Create, Publish and Consume a Pipeline

From this step, the project switches to a second notebook, provided by udacity, named: "aml-pipelines-with-automated-machine-learning-step.ipynb"

  - Changes made to original file:
    - folder name & experiment name
    - compute cluster name to match the existing one
    - dataset name
    - update the automl settings & config to match previous experiment
    
   -Once the workspace, cluster, dataset and model have been either retrieved or created, we start by creating a pipeline & running it:
   ![image](https://user-images.githubusercontent.com/32632731/137583065-ff86b57e-4f0f-4016-b8d9-d3b3f2ef1041.png)
    ![image](https://user-images.githubusercontent.com/32632731/137583127-5b5ee481-bc58-4c96-a161-624c1cf6c515.png)

   ![image](https://user-images.githubusercontent.com/32632731/137582814-aad62a24-f620-438c-b7ee-cb08edfad61a.png)
   ![image](https://user-images.githubusercontent.com/32632731/137582826-d43be04c-8f63-458b-978c-aa76516ac2e6.png)
   ![image](https://user-images.githubusercontent.com/32632731/137582842-14f109a6-9660-40cb-929d-ead75ca3c4f3.png)
   ![image](https://user-images.githubusercontent.com/32632731/137582872-b909cc59-31fc-4fa3-915c-f049c0734674.png)
   
   - After downloading the results outputs, and exmining it, we retrieve the best Model, and test it:
   ![image](https://user-images.githubusercontent.com/32632731/137582954-56babd53-0c8b-498e-a6b1-ed504d301585.png)

   
   - Last, we then publish the Pipeline and test it:
   ![image](https://user-images.githubusercontent.com/32632731/137582967-4b6c0339-295e-4a3d-9c6c-1573bd3237cf.png)
    ![image](https://user-images.githubusercontent.com/32632731/137583043-8ca1fa68-ba72-477c-bcb3-ff47a0a1ab65.png)
    - We can here see the Published Pipeline Overview showing the REST endpoint and status is ACTIVE.
    ![image](https://user-images.githubusercontent.com/32632731/137854884-d7e2a423-08e2-423c-919a-3f8877203cba.png)






## Screen Recording
- The 5 min Pipeline screencast can be accessed here:
https://youtu.be/JBdv4biEUS8
- A full version of the 1st part of the project regarding the Model can be viewed here:
https://youtu.be/2ScCChpkOxg

## Standout Suggestions
-Quickly after understanding what was asked for this Project, I decided to try to deliver it using mostly Azure Python SDK rather that the GUI of Azure ML Studio.

This has proven more challenging but more rewarding and helped me understand better some topics.

Also, as I want this project to be a go-back-to resource whenever I need, I tried do have an extensive documentation of my work and each steps.

This can also be seen in the extensive "bonus" video I recorded to track back every single steps.

-In terms of improvement, I believe there is first an investigation to be made into the struggle to register a model and then deploy it with a ready-generated swagger info.
Also, I believe the entry script and environment settings of some sorts are holding me from being able to have it properly running when trying to deploy with the score.py script. For the purpose of this project a simple dummy script is working. This issue lies in the ability to reference a model (in order to call the predict function) from the score.py script.
-Sources tried:
https://knowledge.udacity.com/questions/414299
https://knowledge.udacity.com/questions/419852
https://docs.microsoft.com/en-us/azure/machine-learning/how-to-deploy-and-where?tabs=python#registermodel
https://docs.microsoft.com/en-us/azure/machine-learning/how-to-deploy-advanced-entry-script#load-registered-models

 
 The model itself could be also improved, we do have an acceptable first results with an accuracy ~0.918 but with fine tuning the algorithm used we could maybe reach an even better result. Also some additional preparation step could help (i.e. Normaization).
 
 SOURCES: https://docs.microsoft.com/en-us/azure/architecture/data-science-process/prepare-data
 
 
 
