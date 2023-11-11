import sys
import psycopg2
import pandas as pd
from config import config
import time
from datetime import timedelta, datetime
from alive_progress import alive_bar

class createDataFrame:

    def __init__(self,startDate,endDate):
        self.startDate = startDate
        self.endDate = endDate
        self.dataframe = None
        self.timeStamps = None
        self.stationIDs = None
        self.pm25Data = None
        self.param = 'pm25'
        self.time = []

    def createTimeStampColumnInDataFrame(self) -> None:
        hoursList = []
        while self.startDate <= endDate:
            for hour in range(24):
                hoursList.append(self.startDate.replace(hour=hour, minute=0, second=0).strftime('%Y-%m-%d %H:%M:%S'))
            self.startDate += timedelta(days=1)
 
            # Creating dataframe with timestamps as column
        self.dataframe = pd.DataFrame(hoursList, columns=['TimeStamp'])

    def generateDataFrameForAllStations(self,tableName='data') ->None:
        dataframe = None
        conn = None
        try:
            # read connection parameters
            params = config()

            #print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)

            # create a cursor
            cur = conn.cursor()

            # Execute sql query to find  distinct sensors in a database
            query = 'SELECT DISTINCT(sname) FROM ' + tableName
            cur.execute(query)
            stationIDs = cur.fetchall()

            with alive_bar(len(stationIDs)) as bar:
                for station in stationIDs:
                    bar()
                    query = 'select time,pm25 from ' + tableName + ' where sname= %s ORDER BY time asc'
                    #print(station[0])
                    cur.execute(query, (station[0],))
                    pm25Data = cur.fetchall()
                    #print(pm25Data)

                    temp = {}
                    for sensorValue in pm25Data:
                        if sensorValue[1] in [-1000, 9999]:
                            temp[str(sensorValue[0])] = 'NaN'
                        else:
                            temp[str(sensorValue[0])] = str(sensorValue[1])

                    #print(temp.values()) # TOBE DELETED

                    sensorSpecificDataFrame = pd.DataFrame({'TimeStamp': temp.keys(), station[0]: temp.values()})
                    #print(sensorDf)
                    self.dataframe = pd.merge(self.dataframe, sensorSpecificDataFrame, on='TimeStamp', how='left')

                #print(self.dataframe)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')

    def save(self, fileName):

        print(self.dataframe)
        self.dataframe.to_csv(fileName,index=False)

if __name__ == "__main__":
    startDate = datetime(2023, 10, 1)
    endDate = datetime(2023, 10, 31)
    obj = createDataFrame(startDate,endDate)

    obj.createTimeStampColumnInDataFrame()
    obj.generateDataFrameForAllStations()

    obj.save("sample.csv")
