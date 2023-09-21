# example workflow


Here, we provide an example workflow to run the three test cases. The script **runISeeSnowTest.py** 1) creates a folder structure for each test case (within this directory) and generates the idealized topography and release area scenario, 2) fetches input data and provides paths to the respective files as well as release thickness and friction parameter values in a dictionary and 3) performs a call to the computational module to perform the simulations. It is exemplary set up for [com1DFA](https://docs.avaframe.org/en/latest/moduleCom1DFA.html) as computational module but you are invited to include a call to your model in there.

### To run

In the main ISeeSnow repository, call the script using: 

```
python3 exampleWorkflowCom1DFA/runISeeSnowTest.py comMod 
```
where *comMod* refers to the name of the computational model as string. Default setting is 'com1DFA' and currently also the only available option, however, we invite you to implement a call to your computational module here.
There is the option to include the flag *-nCM* as command line argument: 

```
python3 exampleWorkflowCom1DFA/runISeeSnowTest.py comMod -nCM
```

If *-nCM* is passed, no call to a computational module is performed, so only the data folder structure is created, the input data is fetched and provided as a python dictionary called *infoDict*. 


 

