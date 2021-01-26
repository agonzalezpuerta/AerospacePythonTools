#      Copyright (c) 2021, Alejandro Gonzalez Puerta
#      All rights reserved.
#  
#      Redistribution and use in source and binary forms, with or without modification, are
#      permitted provided that the following conditions are met:
#        - Redistributions of source code must retain the above copyright notice, this list of
#          conditions and the following disclaimer.
#        - Redistributions in binary form must reproduce the above copyright notice, this list of
#          conditions and the following disclaimer in the documentation and/or other materials
#          provided with the distribution.
#        - The name of the contributors to this software may not be used to endorse or promote
#          promote products derived from this software without specific prior written permission.
#  
#      THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS
#      OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#      MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#      COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#      EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
#      GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
#      AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#      NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
#      OF THE POSSIBILITY OF SUCH DAMAGE.

import datetime
import os
from tqdm import tqdm
import pandas as pd
import numpy as np

from lib.readAccessFrames import readAccessFrames
from lib.isSatelliteInView import isSatelliteInView

from lib.constants import headerStartTime
from lib.constants import headerEndTime

# FILE OPERATIONS
scriptName = "lib\getPowerAnalysis.py"
currentPath = __file__.replace(scriptName,'')

powerSolarArray = 33.6
powerPlatform = 7.0
powerPayload = 5.0
powerTtcON = 10.0
powerTtcOFF = 1.0

folderToSearch = "input/satellites/"

def getLightingPeriod(satelliteID):
    
    os.chdir(currentPath+folderToSearch+satelliteID+"/lighting-periods/")

    lightingPeriod = readAccessFrames()

    return lightingPeriod

def getServiceRegion(satelliteID):
    
    os.chdir(currentPath+folderToSearch+satelliteID+"/service-region/")

    serviceRegion = readAccessFrames()

    return serviceRegion

def getGroundStation(satelliteID):
    
    os.chdir(currentPath+folderToSearch+satelliteID+"/ground-station/")

    groundStation = readAccessFrames()

    return groundStation


def getPowerAnalysis(satelliteAccess,startDate,endDate,satelliteID):


    # Start analysis a few seconds after the first contact
    # startTime = min(satelliteAccess[headerStartTime]).to_pydatetime() + datetime.timedelta(seconds=5.0)


    print(" ")
    print("Analysis Start Date: " + str(startDate))
    print("-------------------------------------------------------")
    
    # Initialize loop variables
    stepSize = 10
    numberOfDays = 1 #(endDate-startDate).days
    endTime = 5400#86400*numberOfDays

    print(currentPath)

    lightingPeriod = getLightingPeriod(satelliteID)
    serviceRegion = getServiceRegion(satelliteID)
    groundStation = getGroundStation(satelliteID)


    powerBalance = 0.0
    powerConsumption = 0.0
    powerGeneration = 0.0

    accumulatedConsumption = 0.0
    accumulatedGeneration = 0.0

    columns = ['Time (UTCG)','Power Consumption [W]','Power Generation [W]','Power Balance [W]']

    df = pd.DataFrame(columns=columns)

    listPowerBalance = []
    listPowerGeneration = []
    listPowerConsumption = []
    listTime = []

    # Iterate through the STK scenario time.
    for dt in tqdm(range(0,endTime,stepSize)):
        
        powerGeneration = 0.0
        powerConsumption = powerPlatform + powerTtcOFF

        # Check if satellite is within lighting period
        if isSatelliteInView(startDate,lightingPeriod[0],headerStartTime,headerEndTime):
            powerGeneration = powerSolarArray

        # Check if satellite is within service region
        if isSatelliteInView(startDate,serviceRegion[0],headerStartTime,headerEndTime):
            powerConsumption = powerConsumption + powerPayload

        # Check if satellite is in visibility of the GS
        if isSatelliteInView(startDate,groundStation[0],headerStartTime,headerEndTime):
            powerConsumption = powerConsumption - powerTtcOFF + powerTtcON

        powerBalance = powerGeneration - powerConsumption

        accumulatedGeneration = accumulatedGeneration + powerGeneration*stepSize        # Energy in [Ws]
        accumulatedConsumption = accumulatedConsumption + powerConsumption*stepSize     # Energy in [Ws]

        listTime.append(startDate)
        listPowerBalance.append(powerBalance)
        listPowerConsumption.append(powerConsumption)
        listPowerGeneration.append(powerGeneration)

        startDate = startDate + datetime.timedelta(seconds=stepSize)

    energyBalance = accumulatedGeneration - accumulatedConsumption

    print(" ")
    print("Accumulated GENERATED power over " + str(numberOfDays) + ": " + str(round(accumulatedGeneration/3600)) + " Wh")
    print(" ")
    print("Accumulated CONSUMED power over " + str(numberOfDays) + ": " + str(round(accumulatedConsumption/3600)) + " Wh")
    print(" ")
    print("Energy BALANCE over " + str(numberOfDays) + ": " + str(energyBalance/3600))
    print(" ")

    df['Time (UTCG)'] = listTime
    df['Power Consumption [W]'] = listPowerConsumption
    df['Power Generation [W]'] = listPowerGeneration
    df['Power Balance [W]'] = listPowerBalance

    df.to_csv(currentPath+folderToSearch+satelliteID+"/power-balance/powerBalance"+satelliteID+".csv")

    return df