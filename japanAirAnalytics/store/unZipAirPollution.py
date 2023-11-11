# Unzips the given input folder.
import os
import sys
import zipfile


def getFolder(zip_folder, output_location):
    """
    :Description: Unzips the given input folder.

    :param zip_folder: str
        Input zip file containing Soramame data.

    :param output_location: str
        Directory to store the unzipped files.

    **Methods to execute the csv file**
    --------------------------------------------------

                Format:
                      >>>   unzippedLocation = get_folder("zip_folder", "output_location")
                Example:
                      >>>     unzippedLocation = get_folder("data.zip", "temp_data")

    """

    with zipfile.ZipFile(zip_folder, 'r') as zip_ref:
        zip_ref.extractall(output_location + str(zip_folder.split('.')[0]))
    return os.path.join(output_location, zip_folder.split('.')[0])


if __name__ == '__main__':
    """
    Start the main() Method
    """
    if len(sys.argv) < 3:
        print("Error : Incorrect number of input parameters given : " + str(len(sys.argv) - 1))
        print("Input Parameters-> zip folder Path, output Folder Path")
    else:
        unzippedLocation = get_folder(sys.argv[1], sys.argv[2])
