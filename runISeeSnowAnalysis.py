"""
    Run script for performing postprocessing analysis of ISeeSnow test cases results
"""

# Load modules
import pathlib
import argparse

# Local imports
from avaframe.in3Utils import cfgUtils, cfgHandling
from avaframe.in3Utils import logUtils
from avaframe.runScripts.runAna3AIMEC import runAna3AIMEC
from avaframe.ana3AIMEC import ana3AIMEC


def runISeeSnowAnalysis(outputDirectoryPath, testCaseName):
    """ perform analysis on result datasets
        if outputDirectoryPath not provided - check for result datasets in data/testCase/Outputs - default option
        if outputDirectoryPath provided, respective testCaseName required to check for thalweg info in inputdata
    """

    # Load avalanche directory from general configuration file
    dirPath = pathlib.Path(__file__).parents[0]
    cfgMain = cfgUtils.getGeneralConfig(dirPath / 'ISeeSnowCfg.ini')
    # create the directory info where to find result datasets for analysis
    aimecDirDict = createAimecDir(outputDirectoryPath, testCaseName, cfgMain, dirPath)

    # loop over all directories
    for ind, aimecDir in enumerate(aimecDirDict['directory']):

        # setup avalancheDir
        testCase = aimecDirDict['testCase'][ind]
        avalancheDir = pathlib.Path(dirPath, 'data', testCase)

        # Start logging
        logName = 'runISeeSnowAnalysis_%s' % testCase
        log = logUtils.initiateLogger(avalancheDir, logName)
        log.info('MAIN SCRIPT')
        log.info('Current avalanche: %s', avalancheDir)

        #++++++++++ Perform result analysis (based on aimec)+++++++++++++++++++++++
        # OUTPUTS need to be located at data/testCase/Outputs
        # get the configuration of aimec using overrides
        cfgAimec = cfgUtils.getModuleConfig(ana3AIMEC, fileOverride='', modInfo=False, toPrint=False, onlyDefault=True)
        cfgAimec, cfgMain = cfgHandling.applyCfgOverride(cfgAimec, cfgMain, ana3AIMEC, addModValues=False)
        runAna3AIMEC(avalancheDir, cfgAimec, inputDir=aimecDir, demFileName=('DEM_%s.asc' % testCase))
        log.info('Result analysis using ana3AIMEC performed for test case: %s' % testCase)


def createAimecDir(outputDirectoryPath, testCaseName, cfgMain, dirPath):
    """ check where to find result datasets for analysis - default in data/testCase/Outputs
        if different outputDirectoryPath provided, create info on input data directory for testCase
    """

    if outputDirectoryPath == '' and testCaseName == '':
        # Load avalanche directory from general configuration file
        aimecDirDict = {'directory': [], 'testCase': []}
        for testCase in ['IdealizedTopo', 'RealTopo', 'CoulombOnly']:
            avalancheDir = pathlib.Path(dirPath, 'data', testCase)
            aimecDirDict['directory'].append((avalancheDir / 'Outputs'))
            aimecDirDict['testCase'].append(testCase)
    elif outputDirectoryPath != '' and testCaseName in ['IdealizedTopo', 'RealTopo', 'CoulombOnly']:
        aimecDir = pathlib.Path(outputDirectoryPath)
        if aimecDir.is_dir() == False:
            message = 'Provided directory %s does not exist' % str(aimecDir)
            raise FileNotFoundError(message)
        else:
            aimecDirDict = {'directory': [aimecDir], 'testCase': [testCaseName]}

    return aimecDirDict


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run ISeeSnow analysis')
    parser.add_argument('outputDir', metavar='outputDirectoryPath', type=str, nargs='?', default='',
                        help=('path to the directory where the result files are stored to perform the analysis ' +
                              'default is data/testCase/Outputs'))
    parser.add_argument('testCase', metavar='testCase', type=str, nargs='?', default='',
                        choices=['', 'IdealizedTopo', 'RealTopo', 'CoulombOnly'],
                        help=('name of the ISeeSnow test case, default the analysis will be performed for all three ' +
                              'test cases: IdealizedTopo, RealTopo, CoulombOnly'))

    args = parser.parse_args()
    runISeeSnowAnalysis(str(args.outputDir), str(args.testCase))
