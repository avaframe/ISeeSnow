"""
    Run script for performing ISeeSnow test cases
    the test case configuration is read from the respective test case's configuration file: 'ISeeSnowCfg%s.ini' % testCase
    command line options are to choose the comMod (computational module) and runComputationalModule - if the comMod shall be called
    or just the input data fetched as inputDict
"""

# Load modules
import pathlib
import pandas as pd
import shutil
import argparse

# Local imports
import avaframe.in3Utils.initializeProject as initProj
from avaframe.com1DFA import com1DFA
from avaframe.in3Utils import cfgUtils, cfgHandling
from avaframe.in3Utils import logUtils
from avaframe.in3Utils import generateTopo
from avaframe.in3Utils import getReleaseArea
from avaframe.in1Data import getInput


def runISeeSnowTest(comMod, noCallToComputationalModule):
    """ create a folder structure for each test case and create generic topography and release areas for
        IdealizedTopo and CoulombOnly test, fetch input data as infoDict and call comMod to perform simulations

        Parameters
        ------------
        comMod: str
            name of computation module used to perform simulations,
            available options: com1DFA
            consider implementing a call to you comMod
        runComputationalModule: str
            if True call comMod if False only input data is fetched and returned as dict inputDict
    """
 
    # loop over all three ISeeSnow test cases
    for testCase in ['IdealizedTopo', 'RealTopo', 'CoulombOnly']:

        # Load avalanche directory from general configuration file
        dirPath = pathlib.Path(__file__).parents[0]
        cfgMain = cfgUtils.getGeneralConfig(dirPath / ('ISeeSnowCfg%s.ini' % testCase))
        avalancheDir = cfgMain['MAIN']['avalancheDir']

        #+++++++++++++++ Initialize project with directory structure
        initProj.initializeFolderStruct(avalancheDir)
        # Start logging
        logName = 'runISeeSnow_%s' % testCase
        log = logUtils.initiateLogger(avalancheDir, logName)
        log.info('MAIN SCRIPT')
        log.info('Current avalanche: %s', avalancheDir)


        if testCase in ['IdealizedTopo', 'CoulombOnly']:
            #+++++++++ Geometry generation +++++++++++++++++
            # get the configuration of generateTopo and getReleaseArea using overrides
            cfgGeo = cfgUtils.getModuleConfig(generateTopo, toPrint=False, onlyDefault=True)
            cfgGeo, cfgMain = cfgHandling.applyCfgOverride(cfgGeo, cfgMain, generateTopo)
            cfgRel = cfgUtils.getModuleConfig(getReleaseArea, toPrint=False, onlyDefault=True)
            cfgRel, cfgMain = cfgHandling.applyCfgOverride(cfgRel, cfgMain, getReleaseArea)

            # Call main function to generate DEM
            [z, name_ext, outDir] = generateTopo.generateTopo(cfgGeo, avalancheDir)
            # Call main function to generate release area
            [xv, yv, xyPoints] = getReleaseArea.getReleaseArea(cfgGeo, cfgRel, avalancheDir)

            # copy release thickness field file
            shutil.copy(pathlib.Path('data', testCase, 'Inputs', 'release1HSField5m.asc'), (pathlib.Path(avalancheDir, 'Inputs', 'RELTH')))
        elif testCase == 'RealTopo':
            copyInputData(avalancheDir, testCase, log)

        #++++++++++FETCH INPUT DATA++++++++++++++++++++++++++
        # paths to: DEM, release shp file, release field asc file, friction parameter values (mu, xi) and release thickness,
        # provided as dictionary with keys: DEM, releaseSHP, releaseASC, mu, xi, releaseThickness
        inputDict = fetchInputDataAsDict(avalancheDir, testCase, log)

        # ++++++++++CALL TO COMPUTATIONAL MODULE++++++++++++++
        # HERE YOU COULD CALL YOUR MODULE
        if noCallToComputationalModule is False:
            if comMod == 'com1DFA':
                #++++++++++ Perform simulation with com1DFA module
                # get the configuration of com1DFA using overrides
                cfgCom1DFA = cfgUtils.getModuleConfig(com1DFA, fileOverride='', modInfo=False, toPrint=False, onlyDefault=True)
                cfgCom1DFA, cfgMain = cfgHandling.applyCfgOverride(cfgCom1DFA, cfgMain, com1DFA, addModValues=False)
                # call com1DFA and perform simulations
                dem, plotDict, reportDictList, simDF = com1DFA.com1DFAMain(cfgMain, cfgInfo=cfgCom1DFA)
                #+++++++++++++++++++++++++++++++++++++++++++++++
            else:
                log.error('ComMod: %s not available - consider implementing it :)' % comMod)


def fetchInputDataAsDict(avalancheDir, testCase, log):
    """ fetch input data (paths to: DEM, release shp file, release field asc file, friction parameter values (mu, xi), release thickness
        provided as dictionary with keys: DEM, releaseSHP, releaseASC, mu, xi, releaseThickness
    """

    # fetch file paths to input data: dem, release area
    demFile, releaseFiles, releaseFields = getInput.getInputPaths(avalancheDir)
    # only use first item of releaseFiles/releaseFields list - as we only have one release area shp/asc file in the input data
    releaseFile = releaseFiles[0]
    releaseField = releaseFields[0]
    # get pandas dataFrame of friction model parameters and release thickness info
    simFile = pathlib.Path('data', testCase, 'Inputs', ('simulationParameterValues_%s.csv' % testCase))
    simulationParameters = pd.read_csv(simFile, header=0)
    mu = simulationParameters[simulationParameters['test case'] == testCase]['mu'].values[0]
    xi = simulationParameters[simulationParameters['test case'] == testCase]['xi'].values[0]
    releaseThickness = simulationParameters[simulationParameters['test case'] == testCase]['releaseThickness'].values[0]
    inputDict = {'DEM': demFile, 'releaseSHP': releaseFile, 'releaseASC': releaseField, 'mu': mu, 'xi': xi,
                 'releaseThickness': releaseThickness}
    log.info(
        'Fetched input data for test case %s, dem: %s, release area shp file: %s and raster file %s, mu: %.2f, xi: %2f and release thickness %.2f' %
        (testCase, demFile.stem, releaseFile.stem, releaseField.stem, mu, xi, releaseThickness))

    return inputDict


def copyInputData(avalancheDir, testCase, log):
    """ copy relevant input data from main data directory to project directory structure"""

    # create path
    avaDir = pathlib.Path(avalancheDir)
    for shpEnd in ['shp', 'shx', 'qix', 'prj', 'dbf', 'cpg']:
        releaseFileshp = pathlib.Path('data', testCase, 'Inputs', ('relWog.%s' % shpEnd))
        shutil.copy(releaseFileshp, (avaDir / 'Inputs' /'REL'))
    demFile = pathlib.Path('data', testCase, 'Inputs', 'DEM_RealTopo.asc')
    shutil.copy(demFile, (avaDir / 'Inputs'))
    relThField = pathlib.Path('data', testCase, 'Inputs', 'relWogField5m.asc')
    shutil.copy(demFile, (avaDir / 'Inputs' / 'RELTH'))
    log.info("Copied input data for %s test case" % testCase)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run ISeeSnow test case simulations')
    parser.add_argument('comMod', metavar='computational module', type=str, nargs='?', default='com1DFA',
                        help=('the name of the computational module that is called to perform the simulations,' +
                              ' available option: com1DFA, however' +
                             'consider implementing a call to your own module'))
    parser.add_argument('-nCM', '--noCallToComputationalModule',
                        action='store_true',
                        help='if False, call to computational module to run test case simulations will be made' +
                             'if True, only folder structure will be initialized and input data fetched and' +
                             'provided it as inputDict')

    args = parser.parse_args()
    runISeeSnowTest(str(args.comMod), args.noCallToComputationalModule)
