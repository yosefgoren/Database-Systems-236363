from typing import List
import Utility.DBConnector as Connector
from Utility.ReturnValue import ReturnValue
from Utility.Exceptions import DatabaseException
from Business.Photo import Photo
from Business.RAM import RAM
from Business.Disk import Disk
from psycopg2 import sql

#GLOBAL SETTINGS:

print_logs = True


#GLBOAL VARIABLES:
ptable_name = "ptable"
dtable_name = "dtable"
rtable_name = "rtable"


#AUX FUNCTIONS:
def strsum(strings: list, delim = ", ", delim_last = False)->str:
    res = ""
    for s in strings:
        res += s + delim
    if not delim_last and len(strings) > 0:
        res = res[:-len(delim)]
    return res

def log_query(*pargs):
    if print_logs:
        print("Final SQL query made:")
        print(*pargs)

def sql_exe(query: str):
    """
        returns 'False' when running successful,
        and 'True' if a DB exception was raised.
    """
    log_query(query)
    result = None
    try:
        conn = Connector.DBConnector()
        result = conn.execute(query)
        conn.commit()
    except DatabaseException.UNIQUE_VIOLATION:
        return ReturnValue.ALREADY_EXISTS, result
    except DatabaseException.ConnectionInvalid:
        return ReturnValue.ERROR, result
    except DatabaseException.FOREIGN_KEY_VIOLATION:#when this happends?
        return ReturnValue.ERROR, result #TODO: check what should be here.
    except DatabaseException.database_ini_ERROR:
        return ReturnValue.ERROR, result
    except DatabaseException.UNKNOWN_ERROR:
        return ReturnValue.ERROR, result
    except DatabaseException.NOT_NULL_VIOLATION:
        return ReturnValue.BAD_PARAMS, result
    except DatabaseException.CHECK_VIOLATION:
        return ReturnValue.BAD_PARAMS, result
    return ReturnValue.OK, result

#CURD API:
def createTables():
    def create_table_format(tname: str, scheme_attributes: list)->str:
        if len(scheme_attributes) < 1:
            raise "got empty list of attributes"
        scheme = strsum(scheme_attributes)
        return f"CREATE TABLE {tname}({scheme});"
    table_specifications = {
        ptable_name: [
            "photoID INT NOT NULL",
            "description TEXT NOT NULL",
            "size INT NOT NULL",
            "PRIMARY KEY(photoID)",
            "CHECK (photoID > 0)",
            "CHECK (size >= 0)"
        ],
        dtable_name: [
            "diskID INT NOT NULL",
            "company TEXT NOT NULL",
            "speed INT NOT NULL",
            "free_space INT NOT NULL",
            "cost INT NOT NULL",
            "PRIMARY KEY(diskID)",
            "CHECK (diskID > 0)",
            "CHECK (speed > 0)",
            "CHECK (cost > 0)",
            "CHECK (free_space >= 0)"
        ],
        rtable_name: [
            "ramID INT NOT NULL",
            "company TEXT NOT NULL",
            "size INT NOT NULL",
            "PRIMARY KEY (ramID)",
            "CHECK (ramID > 0)",
            "CHECK (size > 0)"
        ]
    }
    create_table_queries = [create_table_format(tname, scheme) for tname, scheme in table_specifications.items()]
    create_all_query = "BEGIN;\n"+strsum(create_table_queries, "\n", True)+"COMMIT;"
    sql_exe(create_all_query)

def clearTables():
    pass

def dropTables():
    pass


def addPhoto(photo: Photo) -> ReturnValue:
    """
        photoID INT NOT NULL
        description TEXT NOT NULL
        size INT NOT NULL
    """
    ret, res = sql_exe(f"INSERT INTO {ptable_name} VALUES({photo.getPhotoID()}, '{photo.getDescription()}', {photo.getSize()});")
    return ret

def getPhotoByID(photoID: int) -> Photo:
    ret, (num_results, results) = sql_exe(f"SELECT * FROM {ptable_name} WHERE photoID = {photoID};")
    if len(results) < 1:
        return Photo.badPhoto()
    return Photo(*(results[0].values()))

def deletePhoto(photo: Photo) -> ReturnValue:
    #TODO: add cascade properties to DB to cause automatic deletion of other items...
    ret, res = sql_exe(f"DELETE FROM {ptable_name} WHERE photoID = {photo.getPhotoID()};")
    return ret


def addDisk(disk: Disk) -> ReturnValue:
    """
        diskID INT NOT NULL
        company TEXT NOT NULL
        speed INT NOT NULL
        free_space INT NOT NULL
        cost INT NOT NULL
    """
    ret, res = sql_exe(f"INSERT INTO {dtable_name} VALUES({disk.getDiskID()}, {disk.getCompany()}, {disk.getSpeed()}, {disk.getFreeSpace()}, {disk.getCost()});")
    return ret

def getDiskByID(diskID: int) -> Disk:
    ret, (num_results, results) = sql_exe(f"SELECT * FROM {dtable_name} WHERE diskID = {diskID};")
    if len(results) < 1:
        return Disk.badDisk()
    return Disk(*(results[0].values()))


def deleteDisk(diskID: int) -> ReturnValue:
    ret, res = sql_exe(f"DELETE FROM {dtable_name} WHERE diskID = {diskID};")
    return ret

def addRAM(ram: RAM) -> ReturnValue:
    """
        ramID INT NOT NULL
        company TEXT NOT NULL
        size INT NOT NULL
    """
    ret, res = sql_exe(f"INSERT INTO {rtable_name} VALUES({ram.getRamID()}, {ram.getCompany()}, {ram.getSize()});")
    return ret

def getRAMByID(ramID: int) -> RAM:
    ret, (num_results, results) = sql_exe(f"SELECT * FROM {rtable_name} WHERE ramID = {ramID};")
    if len(results) < 1:
        return RAM.badRAM()
    return RAM(*(results[0].values()))

def deleteRAM(ramID: int) -> ReturnValue:
    ret, res = sql_exe(f"DELETE FROM {rtable_name} WHERE ramID = {ramID};")
    return ret

def addDiskAndPhoto(disk: Disk, photo: Photo) -> ReturnValue:
    return ReturnValue.OK


def addPhotoToDisk(photo: Photo, diskID: int) -> ReturnValue:
    return ReturnValue.OK


def removePhotoFromDisk(photo: Photo, diskID: int) -> ReturnValue:
    return ReturnValue.OK


def addRAMToDisk(ramID: int, diskID: int) -> ReturnValue:
    return ReturnValue.OK


def removeRAMFromDisk(ramID: int, diskID: int) -> ReturnValue:
    return ReturnValue.OK


def averagePhotosSizeOnDisk(diskID: int) -> float:
    return 0


def getTotalRamOnDisk(diskID: int) -> int:
    return 0


def getCostForDescription(description: str) -> int:
    return 0


def getPhotosCanBeAddedToDisk(diskID: int) -> List[int]:
    return []


def getPhotosCanBeAddedToDiskAndRAM(diskID: int) -> List[int]:
    return []


def isCompanyExclusive(diskID: int) -> bool:
    return True


def isDiskContainingAtLeastNumExists(description : str, num : int) -> bool:
    return True


def getDisksContainingTheMostData() -> List[int]:
    return []


def getConflictingDisks() -> List[int]:
    return []


def mostAvailableDisks() -> List[int]:
    return []


def getClosePhotos(photoID: int) -> List[int]:
    return []
