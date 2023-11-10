# Unzips Soramame data files, inserts the data into a PostgreSQL database, and stores information about unsuccessful insertions in a CSV file.
#
#
# **Importing this soramame data files in a Python program**
# -------------------------------------------------------------
#
#
#           import insertDataFromZipFolderToDatabase as db
#
#           data_importer = db(zip_folder, temp_folder, table_name)
#
#           data_importer.insertData()
#
#           unsuccessful_files = data_importer.unsuccessfulInsertionFiles
#
#           print("Total number of unsuccessful insertions:", len(unsuccessful_files))
#
#           data_importer.saveUnsuccessfulInsertions('unsuccessful_insertions.csv')


import csv
import sys
from os import listdir
from os.path import isfile, join
import psycopg2

from config import config

from alive_progress import alive_bar

class newHourlyDataFormat:
    """
    :Description: This script unzips Soramame data files, inserts the data into a PostgresSQL database, and stores information about unsuccessful insertions in a CSV file.

    :param inputZipFile: str
                The path to the zip folder containing Soramame data.

    :param tempFolder: str
                The path to store unzipped files temporarily.

    :param tableName: str
                The name of the database table.


    :Attributes:

        unsuccessfulInsertionFiles : list
                 A list to store information about unsuccessful insertions.

    :Methods:

        insertData(): This method unzips Soramame data files, reads and inserts the data into a PostgreSQL database, and handles unsuccessful insertions.



    **Methods to execute soramame on terminal**
    --------------------------------------------

                Format:
                      >>>   python newHourlyDataFormat.py <inputZipFile> <tempFolder> <tableName>
                Example:
                     >>>    python newHourlyDataFormat.py data.zip temp_data data_table


                     .. note:: Specify the name of the database in database.ini file


    **Importing this soramame data files into a python program**
    ----------------------------------------------------
    .. code-block:: python

                import insertDataFromZipFolderToDatabase as db

                data_importer = db(zip_folder, temp_folder, table_name)

                data_importer.insertData()

                unsuccessful_files = data_importer.unsuccessfulInsertionFiles

                print("Total number of unsuccessful insertions:", len(unsuccessful_files))

                data_importer.saveUnsuccessfulInsertions('unsuccessful_insertions.csv')

    """



    def insert(inputDataFolder):

        """
                Unzip Soramame data, insert it into a PostgreSQL database, and store unsuccessful insertions information.

        """
        files = [f for f in listdir(inputDataFolder) if isfile(join(inputDataFolder, f))]
        with alive_bar(len(files)) as bar:
            for file in files:
                bar()

                # Connect to the PostgreSQL database server
                conn = None
                try:
                    # read connection parameters
                    params = config()

                    # connect to the PostgreSQL server
                    # print('Connecting to the PostgreSQL database...')
                    conn = psycopg2.connect(**params)

                    # create a cursor
                    cur = conn.cursor()

                    # reading csv file
                    csv_file = open(inputDataFolder + '/' + file, encoding="cp932", errors="", newline="")

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
                    # print('Success')

                    # close the communication with the PostgreSQL
                    cur.close()

                except (Exception, psycopg2.DatabaseError) as error:
                    print(error, inputDataFolder + '/' + file)

                finally:
                    if conn is not None:
                        conn.close()
                        # print('Database connection closed.')


if __name__ == '__main__':
    """
        Start main() Method
    """
    # if len(sys.argv) == 4:
    #     soramameDataInsertion = insertDataFromZipFolderToDatabase(sys.argv[1], sys.argv[2], sys.argv[3])
    #     soramameDataInsertion.store()
    # elif len(sys.argv) == 3:
    #     soramameDataInsertion = insertDataFromZipFolderToDatabase(sys.argv[1], sys.argv[2], tableName='data')
    #     soramameDataInsertion.store()
    # else:
    #     print("Error : Incorrect number of input parameters given : " + str(len(sys.argv) - 1))
    #     print("Input Parameters-> Zip Folder path, temporary folder path, table name (default = data) ")
    #
    # newHourlyDataFormat.store('/Users/udaykiranrage/Library/CloudStorage/Dropbox/Github/soramame_ultimate/data/newFormatHourlyData')
    #
    if len(sys.argv) < 2:
        print("Error : Incorrect number of input parameters")
        print("Format: python3  stationInfo.py  fileName")
    else:
        newHourlyDataFormat.insert(sys.argv[1])