*NOTE:* This file is a template that you can use to create the README for your project. The *TODO* comments below will highlight the information you should be sure to include.


# Your Project Title Here

*TODO:* Write an overview to your project.

## Architectural Diagram
*TODO*: Provide an architectual diagram of the project and give an introduction of each step. An architectural diagram is an image that helps visualize the flow of operations from start to finish. In this case, it has to be related to the completed project, with its various stages that are critical to the overall flow. For example, one stage for managing models could be "using Automated ML to determine the best model". 

## Key Steps
*TODO*: Write a short discription of the key steps. Remeber to include all the screenshots required to demonstrate key steps. 
- Step #1: Environment set up => not necessary as I made use of the Udacity Lab with pre-installed tools
  - The only set-up / preparation activity was to create a compute instance (in order to run the Notebook See step #2)
  
- Step #2 : Create and run Auto ML Experiment => achieved using azure SDK for Python, see Notebook xxx

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
  - We then update the URI and key in the endpoint.py and run the script
  - Last we run the benchmark.sh and check the results


- Step #7: Create, Publish and Consume a Pipeline
  - Changes made to original file:
    - folder name & experiment name
    - compute cluster name to match the existing one
    - update the automl settings & config to match previous experiment
    



## Screen Recording
*TODO* Provide a link to a screen recording of the project in action. Remember that the screencast should demonstrate:

## Standout Suggestions
*TODO (Optional):* This is where you can provide information about any standout suggestions that you have attempted.
