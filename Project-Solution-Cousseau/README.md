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
  - Then I created a compute cluster with the instructions given (Standard_DS12_V2, minimum 1 node)
  
  ![image](https://user-images.githubusercontent.com/32632731/136262638-67d22fe3-864b-4136-b286-4de90d62e528.png)

  
  - Once done and running, we then load the Dataset from the url provided
  
  ![image](https://user-images.githubusercontent.com/32632731/136263292-3d06ebfe-ae89-415e-95a2-d5fce5ba9f43.png)

 - From there on, we setup a new AutoML experiment with the required constraint (Classification, Explain best Model, Exit after 1h, max concurrency to 5)
  ![image](https://user-images.githubusercontent.com/32632731/136269016-1d95115b-9ef5-472a-9590-7614aeee6254.png)
 
 - Once ran, we have a look at the results and disply the best run for checking
  
  
 - Before we then jump to Step #3 we need to register the run as a Model.

  ![image](https://user-images.githubusercontent.com/32632731/136269656-cc3ed73b-ce82-46c8-b83d-d7f48480a6e8.png)
  ![image](https://user-images.githubusercontent.com/32632731/136269749-6aba90e5-f5d3-4fe2-9fe9-b54e0eedc777.png)

- Step #3: Deploy the Best Model => achieved using azure SDK for Python, see Notebook xxx

- Step #4: Enable Logging

![image](https://user-images.githubusercontent.com/32632731/136274509-baedc330-1abd-4ed6-aa69-f3e769564cf3.png)

![image](https://user-images.githubusercontent.com/32632731/136275072-0086011c-ec4f-4f3c-bafd-df26560c7b90.png)


- Step #5: Swagger Documentation
- Step #6: Consume Model Endpoints
- Step #7: Create, Publish and Consume a Pipeline



## Screen Recording
*TODO* Provide a link to a screen recording of the project in action. Remember that the screencast should demonstrate:

## Standout Suggestions
*TODO (Optional):* This is where you can provide information about any standout suggestions that you have attempted.
