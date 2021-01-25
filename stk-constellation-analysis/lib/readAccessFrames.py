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


import os, glob
import pandas as pd
import datetime

from lib.constants import headerStartTime
from lib.constants import headerEndTime

def readAccessFrames():

    listSatelliteAccesses = []

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

    return listSatelliteAccesses