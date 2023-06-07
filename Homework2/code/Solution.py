from typing import List
import Utility.DBConnector as Connector
from Utility.ReturnValue import ReturnValue
from Utility.Exceptions import DatabaseException
from Business.Photo import Photo
from Business.RAM import RAM
from Business.Disk import Disk
from psycopg2 import sql

#GLOBAL SETTINGS:

print_logs = False
print_exceptions = False

#GLBOAL VARIABLES:
ptable = "ptable"
dtable = "dtable"
rtable = "rtable"
podtable = "podtable"
rodtable = "rodtable"

table_specifications = {
    ptable: [
        "photoID INT NOT NULL",
        "description TEXT NOT NULL",
        "size INT NOT NULL",
        "PRIMARY KEY(photoID)",
        "CHECK (photoID > 0)",
        "CHECK (size >= 0)"
    ],
    dtable: [
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
    rtable: [
        "ramID INT NOT NULL",
        "company TEXT NOT NULL",
        "size INT NOT NULL",
        "PRIMARY KEY (ramID)",
        "CHECK (ramID > 0)",
        "CHECK (size > 0)"
    ],
    podtable: [
        "photoID INT NOT NULL",
        "diskID INT NOT NULL",
        f"FOREIGN KEY (photoID) REFERENCES {ptable}(photoID) ON DELETE CASCADE",
        f"FOREIGN KEY (diskID) REFERENCES {dtable}(diskID) ON DELETE CASCADE",
        "PRIMARY KEY(photoID, diskID)"
    ],
    rodtable : [
        "ramID INT NOT NULL",
        "diskID INT NOT NULL",
        f"FOREIGN KEY (ramID) REFERENCES {rtable}(ramID) ON DELETE CASCADE",
        f"FOREIGN KEY (diskID) REFERENCES {dtable}(diskID) ON DELETE CASCADE",
        "PRIMARY KEY(ramID, diskID)"
    ]
}

def log_exception(*s):
    if print_exceptions:
        print(*s)

def create_values_exp(*fields: list)->str:
    new_fields = [str(fld) if type(fld) != str else "'"+fld+"'" for fld in fields]
    return f"VALUES({strsum(new_fields)})"

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
    if len(query)>0 and query[-1] != ";":
        query += ";"
    log_query(query)
    result = None
    try:
        conn = Connector.DBConnector()
        result = conn.execute(query)
        conn.commit()
    except DatabaseException.FOREIGN_KEY_VIOLATION:
        log_exception("seen FOREIGN_KEY_VIOLATION")
        return ReturnValue.NOT_EXISTS, result #TODO: check what should be here.
    except DatabaseException.UNIQUE_VIOLATION:
        log_exception("seen UNIQUE_VIOLATION")
        return ReturnValue.ALREADY_EXISTS, result
    except DatabaseException.ConnectionInvalid:
        log_exception("seen ConnectionInvalid")
        return ReturnValue.ERROR, result
    except DatabaseException.database_ini_ERROR:
        log_exception("seen database_ini_ERROR")
        return ReturnValue.ERROR, result
    except DatabaseException.UNKNOWN_ERROR:
        log_exception("seen UNKNOWN_ERROR")
        return ReturnValue.ERROR, result
    except DatabaseException.NOT_NULL_VIOLATION:
        log_exception("seen NOT_NULL_VIOLATION")
        return ReturnValue.BAD_PARAMS, result
    except DatabaseException.CHECK_VIOLATION:
        log_exception("seen CHECK_VIOLATION")
        return ReturnValue.BAD_PARAMS, result
    return ReturnValue.OK, result

def sql_exe_transcation(*queries: list):
    """
        assumes the queries provided do not include ';'.
    """
    assert(all([(len(q) > 0) and (q[-1] != ";") for q in queries]))
    query = strsum(["BEGIN"]+[q for q in queries]+["END"], ";\n", True)
    return sql_exe(query)

#CURD API:
def createTables():
    #TODO: check that if we need to handle table-already exists error or should ignore.
    def create_table_format(tname: str, scheme_attributes: list)->str:
        if len(scheme_attributes) < 1:
            raise "got empty list of attributes"
        scheme = strsum(scheme_attributes)
        return f"CREATE TABLE {tname}({scheme})"
    
    create_table_queries = [create_table_format(tname, scheme) for tname, scheme in table_specifications.items()]
    sql_exe_transcation(*create_table_queries)

def clearTables():
    sql_exe_transcation(*[f"DELETE FROM {tname}" for tname in table_specifications.keys().__reversed__()])

def dropTables():
    sql_exe_transcation(*[f"DROP TABLE {tname}" for tname in table_specifications.keys().__reversed__()])

def addPhoto_query(photo: Photo)->str:
    return f"INSERT INTO {ptable} {create_values_exp(photo.getPhotoID(), photo.getDescription(), photo.getSize())}"

def addPhoto(photo: Photo) -> ReturnValue:
    """
        photoID INT NOT NULL
        description TEXT NOT NULL
        size INT NOT NULL
    """
    ret, res = sql_exe(addPhoto_query(photo))
    return ret

def getPhotoByID(photoID: int) -> Photo:
    ret, (num_results, results) = sql_exe(f"SELECT * FROM {ptable} WHERE photoID = {photoID};")
    if len(results) < 1:
        return Photo.badPhoto()
    return Photo(*(results[0].values()))

def deletePhoto(photo: Photo) -> ReturnValue:
    #TODO: add cascade properties to DB to cause automatic deletion of other items...
    ret, res = sql_exe(f"DELETE FROM {ptable} WHERE photoID = {photo.getPhotoID()};")
    return ret

def addDisk_query(disk: Disk)->str:
    return f"INSERT INTO {dtable} {create_values_exp(disk.getDiskID(), disk.getCompany(), disk.getSpeed(), disk.getFreeSpace(), disk.getCost())}"

def addDisk(disk: Disk) -> ReturnValue:
    """
        diskID INT NOT NULL
        company TEXT NOT NULL
        speed INT NOT NULL
        free_space INT NOT NULL
        cost INT NOT NULL
    """
    ret, res = sql_exe(addDisk_query(disk))
    return ret

def getDiskByID(diskID: int) -> Disk:
    ret, (num_results, results) = sql_exe(f"SELECT * FROM {dtable} WHERE diskID = {diskID};")
    if len(results) < 1:
        return Disk.badDisk()
    return Disk(*(results[0].values()))


def deleteDisk(diskID: int) -> ReturnValue:
    ret, res = sql_exe(f"DELETE FROM {dtable} WHERE diskID = {diskID};")
    return ret

def addRAM(ram: RAM) -> ReturnValue:
    """
        ramID INT NOT NULL
        company TEXT NOT NULL
        size INT NOT NULL
    """
    ret, res = sql_exe(f"INSERT INTO {rtable} {create_values_exp(ram.getRamID(), ram.getCompany(), ram.getSize())}")
    return ret

def getRAMByID(ramID: int) -> RAM:
    ret, (num_results, results) = sql_exe(f"SELECT * FROM {rtable} WHERE ramID = {ramID};")
    if len(results) < 1:
        return RAM.badRAM()
    return RAM(*(results[0].values()))

def deleteRAM(ramID: int) -> ReturnValue:
    ret, res = sql_exe(f"DELETE FROM {rtable} WHERE ramID = {ramID};")
    return ret

def addDiskAndPhoto(disk: Disk, photo: Photo) -> ReturnValue:
    ret, res = sql_exe_transcation(addDisk_query(disk), addPhoto_query(photo))
    return ret

# Basic API:
def addPhotoToDisk(photo: Photo, diskID: int) -> ReturnValue:
    ret, res = sql_exe_transcation(#TODO: verify exceptions are handled correctly.
        f"UPDATE {dtable} SET free_space=free_space-{photo.getSize()}",
        f"INSERT INTO {podtable} {create_values_exp(photo.getPhotoID(), diskID)}"
    )
    return ret

def removePhotoFromDisk(photo: Photo, diskID: int) -> ReturnValue:
    ret, res = sql_exe_transcation(
        f"UPDATE {dtable} SET free_space=free_space+{photo.getSize()}",
        f"DELETE FROM {podtable} WHERE photoID={photo.getPhotoID()} AND diskID={diskID}"
    )
    return ret


def addRAMToDisk(ramID: int, diskID: int) -> ReturnValue:
    ret, res = sql_exe(f"INSERT INTO {rodtable} {create_values_exp(ramID, diskID)}")
    return ret

def removeRAMFromDisk(ramID: int, diskID: int) -> ReturnValue:
    ret, res = sql_exe(f"DELETE FROM {rodtable} WHERE ramID={ramID} AND diskID={diskID}")
    return ret

def averagePhotosSizeOnDisk(diskID: int) -> float:
    ret, res = sql_exe(f"SELECT AVG(size) FROM {ptable}, {podtable} WHERE {podtable}.photoID={ptable}.photoID AND {podtable}.diskID={diskID}")
    if ret != ReturnValue.OK:
        return -1
    avg = res[1][0]['avg']
    return 0 if avg == None else avg

def getTotalRamOnDisk(diskID: int) -> int:
    ret, res = sql_exe(f"SELECT SUM(size) FROM {rtable}, {rodtable} WHERE {rtable}.ramID={rodtable}.ramID AND {rodtable}.diskID={diskID}")
    if ret != ReturnValue.OK:
        return -1
    sum = res[1][0]['sum']
    return 0 if sum == None else sum

def getCostForDescription(description: str) -> int:#TODO: basic test
    ret, res = sql_exe(f"SELECT SUM({dtable}.cost*{ptable}.size)\
        FROM {ptable}, {podtable}, {dtable}\
        WHERE {ptable}.description={description} AND {ptable}.photoID={podtable}.photoID AND {dtable}.diskID={podtable}.diskID"
    )
    if ret != ReturnValue.Ok:
        return -1
    sum = res[1][0]['sum']
    return 0 if sum == None else sum

def getPhotosCanBeAddedToDisk(diskID: int) -> List[int]:
    ret, res = sql_exe(f"SELECT {ptable}.photoID FROM {ptable}\
        WHERE {ptable}.size <= (SELECT free_space FROM\
            {dtable} WHERE {dtable}.diskID={diskID}\
        )\
        ORDER BY {ptable}.photoID DESC\
        LIMIT 5"
    )
    if ret != ReturnValue.OK or res[1] == None:
        return []
    photo_ids = []
    for i in range(res[0]):
        d = res[1][i]
        photo_ids.append(*d.values())
    return photo_ids
    

def getPhotosCanBeAddedToDiskAndRAM(diskID: int) -> List[int]:
    ret, res = sql_exe(f"\
        (\
            SELECT {ptable}.photoID FROM {ptable}\
            WHERE {ptable}.size <= (SELECT free_space FROM {dtable} WHERE {dtable}.diskID={diskID})\
        )\
            INTRERSECT\
        (\
            SELECT {ptable}.photoID FROM {ptable}\
            WHERE {ptable}.size <=\
            (\
                SELECT SUM({rtable}.size) FROM {rtable}, {rodtable}\
                WHERE {rtable}.ramID={rodtable}.ramID AND {rodtable}.diskID={diskID}\
            )\
        )\
        ORDER BY {ptable}.photoID DESC\
        LIMIT 5"
    )
    if ret != ReturnValue.OK or res[1] == None:
        return []
    photo_ids = []
    for i in range(res[0]):
        d = res[1][i]
        photo_ids.append(*d.values())
    return photo_ids

def isCompanyExclusive(diskID: int) -> bool:
    ret, res = sql_exe(f"SELECT diskID FROM {dtable} WHERE\
            (SELECT company FROM {dtable} WHERE {dtable}.diskID={diskID})\
            =\
            ALL(SELECT company FROM {rodtable}, {rtable} WHERE {rodtable}.ramID={rtable}.ramID) AND {rodtable}.diskID={diskID})\
        AND\
            {dtable}.diskID={diskID}\
    ")
    if ret != ReturnValue.OK or res[1] == None:
        return False
    return (res[0] != 0)

def isDiskContainingAtLeastNumExists(description : str, num : int) -> bool:
    return True


def getDisksContainingTheMostData() -> List[int]:
    return []

# Advanced API:
def getConflictingDisks() -> List[int]:
return []


def mostAvailableDisks() -> List[int]:
return []


def getClosePhotos(photoID: int) -> List[int]:
return []
