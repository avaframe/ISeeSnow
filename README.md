# ISeeSnow - model intercomparison pilot-study

The ISeeSnow project aims to initiate an intercomparison project for avalanche
simulation tools. We want to start a conversation among the modelling community
with a pilot study comparing results from mainly thickness-(depth-) integrated models
based on a Voellmy friction relation. 

To keep it simple, we exclude any model verification tests that might require a
more complex model setup. We also exclude model validation tests that
potentially include model optimization.

So the focus is on standard simulations with prescribed friction parameters for
two different topographies: an idealized topography and a real-world example. 

We ask the participating groups to employ their default configuration with a
Voellmy friction relation for these simulations. The values of the friction parameters 
mu, xi and the release thickness are provided alongside the topography and 
release area input data. As a third test case, a simulation run with purely 
Coulomb friction should be performed for the idealized topography. If the 
respective model configuration is not designed to use a friction relation 
with only Coulomb friction, we ask the participants to set the xi value in the 
Voellmy friction relation to an extremely high value, 
forcing the effect of the turbulent friction term to be negligible. 

The AvaFrame-team will provide input data and parameter values for the three test
cases and compare the gathered simulation results. The analysis is performed
using the functionalities of the [ana3AIMEC](https://docs.avaframe.org/en/latest/moduleAna3AIMEC.html) and
[ana4Stats](https://docs.avaframe.org/en/latest/moduleAna4Stats.html) modules of
[AvaFrame](https://docs.avaframe.org/en/latest/index.html). 



## How to participate in ISeeSnow?

The requirement is to perform one simulation per test case (three in total)
and provide the result datasets as described in the Section *Result datasets*.

The **runISeeSnowAnalysis.py** script provides the option to test the postprocessing analysis based on
[ana3AIMEC](https://docs.avaframe.org/en/latest/moduleAna3AIMEC.html) on your simulation results. In order to run
this script, ensure that your simulation results (in the required format and following the prescribed naming convention
described in the Section *Result datasets*) are located in the **data/testCase/Outputs** directories of
the respective test case (i.e. IdealizedTopo, RealTopo, CoulombOnly). 
 
The analysis results will be saved to **data/testCase/Outputs/ana3AIMEC**
for each of the three test cases. There is also the option to provide *outputDirectoryPath* and
*testCase* as command line arguments. If provided, the simulation result files will be fetched from the
*outputDirectoryPath* directory (one per test case) and the required topography information from the *data/testCase/Inputs* directory,
analysis results will also be saved to **data/testCase/Outputs/ana3AIMEC**. The aimec analysis further requires e.g. a
[thalweg](https://docs.avaframe.org/en/latest/glossary.html#term-thalweg) (shapefile), this data
is also provided alongside the model input data. 

Note that running the **runISeeSnowAnalysis.py** script requires an [*AvaFrame* advanced installation](https://docs.avaframe.org/en/latest/advancedUsage.html#advanced-script-installation).

Additionally, the directory **exampleWorkflowCom1DFA** provides an example workflow to run the test
cases - it is exemplary set up for [com1DFA](https://docs.avaframe.org/en/latest/moduleCom1DFA.html)-
but you are invited to include a call to your model in there.

In the following, information on provided model input data and required format
of result datasets is given:

### Model input data:

The input data comprises a digital elevation model (DEM) (regularly spaced points with a spatial resolution of 5 meters)
and a release area scenario per test case. The release area is provided as shapefile OR alternatively as release
thickness field .asc file. The .asc file has the same extent and spatial resolution as the DEM and provides the actual
values of release thickness at each cell (values different from zero give the release thickness, whereas areas outside
of the prescribed release polygon are represented by values of 0). Note on release thickness .asc file: The .asc files
in the **Inputs** directories are created based on the DEM and the release polygon read from the corresponding shapefile.
In the resulting raster, cells are set to belong to the release area as soon as there is an intersection with
the release polygon. For this reason, the area of the release thickness field exceeds the area of the release polygon.

* digital elevation model as .asc file (format:
  https://desktop.arcgis.com/en/arcmap/10.3/manage-data/raster-and-images/esri-ascii-raster-format.htm)
  with a spatial resolution of 5 meters
	* testCase IdealizedTopo: **DEM_IdealizedTopo.asc**
	* testCase RealTopo: **DEM_RealTopo.asc**
 	* testCase CoulombOnly: **DEM_CoulombOnly.asc**
* release area scenario as shapefile with release area feature (polygon), homogeneous release thickness throughout release area
	* testCase IdealizedTopo: **REL/release1HS.shp**
	* testCase RealTopo: **REL/realWog.shp**
 	* testCase CoulombOnly: **REL/release1HS.shp**
* release area scenario as asc file with release area feature thickness, homogeneous release
  thickness throughout release area, covering the DEM extent and a spatial resolution of 5 meters
	* testCase IdealizedTopo: **RELTH/release1HSField5m.asc**
	* testCase RealTopo: **RELTH/realWogField5m.asc**
 	* testCase CoulombOnly: **RELTH/release1HSField5m.asc**	
* simulation parameter text file with values for mu and xi, as well as release
  thickness value (see description of Voellmy-type friction relation for
  example here:
  https://docs.avaframe.org/en/latest/theoryCom1DFA.html#voellmy-friction-model)

#### IdealizedTopo
![test case IdealizedTopo](/images/releaseScenario_release1HS_01com1DFA_C_null_dfa.png)


#### RealTopo
![test case RealTopo](/images/releaseScenario_relWog_02com1DFA_C_null_dfa.png)


#### CoulombOnly
![test case CoulombOnly](/images/releaseScenario_release1HS_03com1DFA_C_null_dfa.png)

The corresponding files can be found in the directory **data**, where **IdealizedTopo** refers to the
idealized test case, **RealTopo** represents the real-world topography and **CoulombOnly** provides the same
topography and release area scenario as in the case of the idealizedTopo test case, but should be run with
purely Coulomb friction. For all three test cases, the DEM (*DEM_IdealizedTopo.asc*, *DEM_RealTopo.asc* and
*DEM_CoulombOnly*, respectively), the release area shapefile and the release area thickness field are located
in the directory **Inputs**. The friction parameter values and the release thickness value, can be found
in the corresponding *simulationParameterValues_testCase.csv* files. Data source info for the RealTopo test
case can be found [here](https://docs.avaframe.org/en/latest/dataSources.html#data-sources). The idealized
topographies have been generated using the [in3Utils](https://docs.avaframe.org/en/latest/moduleIn3Utils.html)
module. This topography generation is also included in the *exampleWorkflowCom1DFA/runISeeSnowTest.py* script.

### Result datasets: 

We ask all the participating groups to perform a simulation for the two test
cases, and to provide the following result datasets: 

* fields of peak flow velocity and peak flow thickness as .asc file covering the
  entire computational domain (DEM extent). *Peak* refers to the maximum
  flow variable value over the entire duration of the simulation. The peak
  fields should have a spatial resolution of 5 meters and the same extent of
  the DEM - hence the .asc files should have the same header as the provided
  dem file (if there is an issue to provide the results in this format, contact us).
  We require a specific naming of the peak field .asc files:
  *releaseName_simulationID_simType_modelType_resultType.asc*, from now on
  referred to *A_B_C_D_E.asc*, where:
  	- A - *releaseName*: refers to the name of the release shapefile
	- B - *simulationID*: needs to be unique for each simulation - use: 01IdealizedTopo, 02RealTopo and 03CoulombOnly
  	- C - *simType*: use *null*
	- D - *modelType*: name of your model - NOT allowed to include underscores
	- E - *result type*: is pft (peak flow thickness) and pfv (peak flow velocity)

  Note: underscores are not allowed except to separate the
  five elements of the file name and no data values should be provided as nans.
* a csv file with information on computation duration (CPU), avalanche flow time, total
  volume at initial time step and also final time step, spatial resolution
  (example: *simulationResultTable.csv*) - one file listing the values of all simulations
* a text file with information on model configuration, i.e. parameter values,
  numerical configuration, model version etc., the naming should be consistent with
  the peak field files: *releaseName_simulationID_simType_modelType.txt*.
  These configuration files can optionally be also provided as [.ini files](https://docs.python.org/3/library/configparser.html#supported-ini-file-structure),
  to be interpreted by [configparser](https://docs.python.org/3/library/configparser.html#module-configparser). 

**Note:** the spatial resolution of the model input data is 5 meters (regular
grid) and the result fields are required to also have a spatial resolution of 5
meters. However, this applies to the submitted result fields, the simulations
can be performed using your default numerical setup (also if using a different
spatial resolution), but they need to be submitted as rasters with a cell size
of 5 meters.

All the listed result files should be provided as archive file (zip, tar.gz, etc.) containing
the simulationResultTable with one line per simulation, and 
one subdirectory per avalanche test case: **IdealizedTopo**,
**RealTopo** and **CoulombOnly** each of them providing the respective peak fields of flow
velocity and flow thickness and the model configuration file. 

In addition, we ask the participating groups to provide a paragraph
describing their simulation tool, e.g. mathematical model, numerical methods,
configuration, code availability and a reference. This should be added as a
simple .txt file in the archive file together with the result datasets. 

Once you have prepared the required result datasets, you can send the archive file
to us via email. In case the file size is too big, contact us and we will 
inform you on how to submit the data. With the submission you agree to the publication
of the results in full. The deadline for submission is on November 30th. 

## Provide your own test case

We invite you to provide further even test cases that can be used in a potential
continuation or future intercomparison projects. We will collect these and publish
them as an open dataset (properly attributed, citable), hopefully building a test
dataset that benefits the whole community. 
The minimum requirements for an event test case are: 

* release area scenario
* release thickness 
* documented runout line

  
