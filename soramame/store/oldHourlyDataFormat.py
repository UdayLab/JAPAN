import os
import csv
import sys
import psycopg2
from config import config
from alive_progress import alive_bar
from os import listdir
from os.path import isfile, join
from config import config
from alive_progress import alive_bar

class oldHourlyDataFormat:

    def insert(inputDataFolder):
        subFolders = [ f.path for f in os.scandir(inputDataFolder) if f.is_dir() ]
        conn = None
        inputFileName = ""
        for folder in subFolders:
            try:
                params = config()
                conn = psycopg2.connect(**params)

                cur = conn.cursor()


                print('Reading the folder: ' + str(folder))
                files = [f for f in listdir(folder) if isfile(join(folder, f))]

                with alive_bar(len(files)) as bar:
                    for file in files:
                        bar()

                        inputFileName = folder + '/' + file

                        csv_file = open(inputFileName, encoding="cp932", errors="", newline="")
                        f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"',
                                       skipinitialspace=True)
                        header = next(f)

                        for row in f:
                            for i in range(len(row)):
                                # filling missing values
                                # print(row[i])
                                if row[i] == '' or row[i] == '-' or '#' in row[i]:
                                    row[i] = '9999'

                                # writing query
                            query = 'insert into hourly_observations values(' + row[0] + ',\'' + row[1] + ' ' + row[
                                2] + ':00:00\'' + ',' + \
                                    row[3] + ',' + row[4] + ',' + row[5] + ',' \
                                    + row[6] + ',' + row[7] + ',' + row[8] + ',' + row[9] + ',' + row[10] + ',' + row[
                                        11] + ',' + \
                                    row[12] + ',' + row[13] + ',' + row[14] + ',-1' + ',' + row[16] + ',' + row[17] + ',' + row[
                                        18] + ")"

                            # executing the query
                            cur.execute(query)
                    conn.commit()
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error,  inputFileName)
            finally:
                if conn is not None:
                    conn.close()


if __name__ == '__main__':
    """
        Start the main() Method
    """

    if len(sys.argv) < 2:
        print("Error : Incorrect number of input parameters")
        print("Format: python3  stationInfo.py  inputFolderContainingData")
    else:
        oldHourlyDataFormat.insert(sys.argv[1])