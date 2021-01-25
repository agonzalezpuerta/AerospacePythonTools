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
from tqdm import tqdm

from lib.isSatelliteInView import isSatelliteInView

def findContactGaps(listSatelliteAccesses,headerStartTime,headerEndTime):

    # Determine first satellite contact time
    listOfFirstContacts = []
    for satelliteAccess in listSatelliteAccesses:
        listOfFirstContacts.append(min(satelliteAccess[headerStartTime]).to_pydatetime())

    # Start analysis a few seconds after the first contact
    startTime = min(listOfFirstContacts) + datetime.timedelta(seconds=5.0)

    print(" ")
    print("Analysis Start Time: " + str(startTime))
    print("-------------------------------------------------------")
    
    # Initialize loop variables
    revisitTime = 0.0
    revisitTimeList = []
    stepSize = 10
    numberOfDays = 30
    endTime = 86400*numberOfDays
    atLeastOneSatelliteInView = False

    

    # Iterate through the STK scenario time.
    for dt in tqdm(range(0,endTime,stepSize)):

        storeRevisitTime = revisitTime

        # Check if there is at least one satellite in view
        for satelliteAccess in listSatelliteAccesses:
            if isSatelliteInView(startTime,satelliteAccess,headerStartTime,headerEndTime):
                atLeastOneSatelliteInView = True
                break
            else:
                atLeastOneSatelliteInView = False

        if atLeastOneSatelliteInView:
            revisitTime = 0.0
        else:
            revisitTime = revisitTime + stepSize

        # Check if the revisit time has set to zero but on the previous instant it was non-zero
        if storeRevisitTime > revisitTime:
            revisitTimeList.append(storeRevisitTime)

        startTime = startTime + datetime.timedelta(seconds=stepSize)

    return revisitTimeList