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

# --- STK CONSTELLATION ANALYSIS --------------------------------------------------------------------------------------------
# Authors: Alejandro Gonzalez Puerta (ALGP)
# Goal: To post-process the results of STK Basic and yield constellation performance metrics
# ---------------------------------------------------------------------------------------------------------------------------

# IMPORT CUSTOM FUNCTIONS
from lib.getPowerAnalysis import getPowerAnalysis
from lib.findAccessesPerDay import findAccessesPerDay
from lib.concatenateSatelliteAccesses import concatenateSatelliteAccesses
from lib.findContactGaps import findContactGaps
from lib.readAccessFrames import readAccessFrames

# IMPORT LIBRARIES
import pandas as pd
import datetime
import os, glob

# ---------------------------------------------------------------------------------------------------------------------------

# FILE OPERATIONS
scriptName = "stk-constellation-analysis.py"
currentPath = __file__.replace(scriptName,'')

satelliteID = 'BELEM'
selectedUserTerminal = 'Brasilia'
folderToSearch = '/input/user-terminals/' + selectedUserTerminal

startDate = datetime.datetime(year= 2022, month= 1,day=1,hour=0,minute=0,second=0)
endDate = datetime.datetime(year= 2022, month= 2,day=1,hour=0,minute=0,second=0)

# COLUMN HEADERS
headerAccess = "Access"
headerStartTime  = "Start Time (UTCG)"
headerEndTime  = "Stop Time (UTCG)"
headerDuration = "Duration (sec)"

# FUNCTION HANDLING
enableRevisitTime = False
enableAccessDuration = False
enableDailyAccess = False
enablePowerAnalysis = True


# ---------------------------------------------------------------------------------------------------------------------------

# ITERATE THROUGH FOLDER
# listSatelliteAccesses = []

os.chdir(currentPath+folderToSearch)

listSatelliteAccesses = readAccessFrames()

# ---------------------------------------------------------------------------------------------------------------------------
# PERFORM ANALYSIS

if enableAccessDuration:
    concatenatedSatelliteAccesses = concatenateSatelliteAccesses(listSatelliteAccesses)

    print(" ")
    print("Access duration statistics for " + selectedUserTerminal + ", total of " + str((endDate-startDate).days) + " days:")
    print("-------------------------------------------------------")
    print(" ")
    print("MIN: " + str(min(concatenatedSatelliteAccesses[headerDuration])))
    print("AVG: " + str(round(sum(concatenatedSatelliteAccesses[headerDuration])/len(concatenatedSatelliteAccesses[headerDuration]),2)))
    print("MAX: " + str(max(concatenatedSatelliteAccesses[headerDuration])))
    print("-------------------------------------------------------")
    print(" ")

# ---------------------------------------------------------------------------------------------------------------------------

if enableDailyAccess:

    accessesPerDay = findAccessesPerDay(listSatelliteAccesses,startDate,endDate,headerStartTime)

    print(" ")
    print("Daily access statistics for " + selectedUserTerminal + ", total of " + str((endDate-startDate).days) + " days:")
    print("-------------------------------------------------------")
    print(accessesPerDay)
    print(" ")
    print("MIN: " + str(min(accessesPerDay)))
    print("AVG: " + str(round(sum(accessesPerDay)/len(accessesPerDay),2)))
    print("MAX: " + str(max(accessesPerDay)))
    print("-------------------------------------------------------")
    print(" ")

# ---------------------------------------------------------------------------------------------------------------------------

if enableRevisitTime:

    revisitTimeList = findContactGaps(listSatelliteAccesses,headerStartTime,headerEndTime)

    print(" ")
    print("Revisit time statistics for " + selectedUserTerminal + ":")
    print("-------------------------------------------------------")
    print(revisitTimeList)
    print(" ")
    print("MIN: " + str(min(revisitTimeList)))
    print("AVG: " + str(round(sum(revisitTimeList)/len(revisitTimeList),2)))
    print("MAX: " + str(max(revisitTimeList)))
    print("-------------------------------------------------------")
    print(" ")

# ---------------------------------------------------------------------------------------------------------------------------

if enablePowerAnalysis:

    df = getPowerAnalysis(listSatelliteAccesses[0],startDate,endDate,satelliteID)

    print(df)