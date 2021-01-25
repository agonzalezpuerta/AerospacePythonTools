# --- STK CONSTELLATION ANALYSIS --------------------------------------------------------------------------------------------
# Authors: Alejandro Gonzalez Puerta (ALGP)
# Goal: To post-process the results of STK Basic and yield constellation performance metrics
# ---------------------------------------------------------------------------------------------------------------------------

# IMPORT CUSTOM FUNCTIONS
from lib.isSatelliteInView import isSatelliteInView
from lib.findAccessesPerDay import findAccessesPerDay
from lib.findAccessDurationStatistics import findAccessDurationStatistics
from lib.findContactGaps import findContactGaps

# IMPORT LIBRARIES
import pandas as pd
import datetime
import os, glob

# ---------------------------------------------------------------------------------------------------------------------------

# FILE OPERATIONS
scriptName = "stk-constellation-analysis.py"
currentPath = __file__.replace(scriptName,'')
folderToSearch = 'Brasilia'

startDate = datetime.datetime(year= 2022, month= 1,day=1,hour=0,minute=0,second=0)
endDate = datetime.datetime(year= 2022, month= 2,day=1,hour=0,minute=0,second=0)

# COLUMN HEADERS
headerAccess = "Access"
headerStartTime  = "Start Time (UTCG)"
headerEndTime  = "Stop Time (UTCG)"
headerDuration = "Duration (sec)"

# FUNCTION HANDLING
enableRevisitTime = False
enableAccessDuration = True
enableDailyAccess = False

# ---------------------------------------------------------------------------------------------------------------------------

# ITERATE THROUGH FOLDER
listSatelliteAccesses = []

os.chdir(currentPath+folderToSearch)

for fileToSearch in glob.glob("*.csv"):

    # Get current dataframe
    df = pd.read_csv(fileToSearch , delimiter=',')

    # Remove miliseconds from datetime string
    df[headerStartTime] = df[headerStartTime].str[:-4]
    df[headerEndTime] = df[headerEndTime].str[:-4]

    # Convert time strings into datetime format
    df[headerStartTime] = df.apply(lambda x: datetime.datetime.strptime(x[headerStartTime], '%d %b %Y %H:%M:%S'),axis=1)
    df[headerEndTime] = df.apply(lambda x: datetime.datetime.strptime(x[headerEndTime], '%d %b %Y %H:%M:%S'),axis=1)

    # Append dataframe to search list
    listSatelliteAccesses.append(df)

# ---------------------------------------------------------------------------------------------------------------------------
# PERFORM ANALYSIS

if enableAccessDuration:
    findAccessDurationStatistics(listSatelliteAccesses)

# ---------------------------------------------------------------------------------------------------------------------------

if enableDailyAccess:

    accessesPerDay = findAccessesPerDay(listSatelliteAccesses,startDate,endDate,headerStartTime)

    print(" ")
    print("Daily access statistics for " + folderToSearch + ", total of " + str((endDate-startDate).days) + " days:")
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
    print("Revisit time statistics for " + folderToSearch + ":")
    print("-------------------------------------------------------")
    print(revisitTimeList)
    print(" ")
    print("MIN: " + str(min(revisitTimeList)))
    print("AVG: " + str(round(sum(revisitTimeList)/len(revisitTimeList),2)))
    print("MAX: " + str(max(revisitTimeList)))
    print("-------------------------------------------------------")
    print(" ")

# ---------------------------------------------------------------------------------------------------------------------------