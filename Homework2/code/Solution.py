from typing import List
import Utility.DBConnector as Connector
from Utility.ReturnValue import ReturnValue
from Utility.Exceptions import DatabaseException
from Business.Photo import Photo
from Business.RAM import RAM
from Business.Disk import Disk
import psycopg2

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
def get_first_val(d: dict):
    return list(d.values())[0]

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

def sql_exe_list(query: str, default_res = []):
    ret, res = sql_exe(query)
    if ret != ReturnValue.OK or res[0] <= 0:
        return default_res
    return [get_first_val(res[1][i]) for i in range(res[0])]


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
        return ReturnValue.NOT_EXISTS, result
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
    except psycopg2.errors.UndefinedColumn:
        log_exception("seen psycopg2.errors.UndefinedColumn")
        return ReturnValue.BAD_PARAMS, result
    except psycopg2.errors.UndefinedTable:
        log_exception("seen psycopg2.errors.UndefinedTable")
        return ReturnValue.ERROR, result
    # except Exception:
    #     log_exception("seen Exception")
    #     return ReturnValue.ERROR, result
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
    def create_table_format(tname: str, scheme_attributes: list)->str:
        if len(scheme_attributes) < 1:
            raise "got empty list of attributes"
        scheme = strsum(scheme_attributes)
        return f"CREATE TABLE {tname}({scheme})"
    
    create_table_queries = [create_table_format(tname, scheme) for tname, scheme in table_specifications.items()]
    try:
        sql_exe_transcation(*create_table_queries)
    except psycopg2.errors.DuplicateTable:
        pass

def clearTables():
    sql_exe_transcation(*[f"DELETE FROM {tname}" for tname in table_specifications.keys().__reversed__()])

def dropTables():
    sql_exe_transcation(*[f"DROP TABLE {tname}" for tname in table_specifications.keys().__reversed__()])

def addPhoto_query(photo: Photo)->str:
    return f"INSERT INTO {ptable} {create_values_exp(photo.getPhotoID(), photo.getDescription(), photo.getSize())}"

def addPhoto(photo: Photo) -> ReturnValue:
    ret, res = sql_exe(addPhoto_query(photo))
    return ret

def getPhotoByID(photoID: int) -> Photo:
    ret, res = sql_exe(f"SELECT * FROM {ptable} WHERE photoID = {photoID};")
    if ret != ReturnValue.OK or res[0] < 1:
        return Photo.badPhoto()
    return Photo(*(res[1][0].values()))

def deletePhoto(photo: Photo) -> ReturnValue:
    ret, res = sql_exe_transcation(
        f"UPDATE {dtable} SET free_space=free_space+{photo.getSize()}\
            WHERE {dtable}.diskID IN (SELECT {podtable}.diskID FROM {podtable} WHERE {podtable}.photoID={photo.getPhotoID()})",   
        f"DELETE FROM {ptable} WHERE photoID = {photo.getPhotoID()}"
    )
    return ret

def addDisk_query(disk: Disk)->str:
    return f"INSERT INTO {dtable} {create_values_exp(disk.getDiskID(), disk.getCompany(), disk.getSpeed(), disk.getFreeSpace(), disk.getCost())}"

def addDisk(disk: Disk) -> ReturnValue:
    ret, res = sql_exe(addDisk_query(disk))
    return ret

def getDiskByID(diskID: int) -> Disk:
    ret, res = sql_exe(f"SELECT * FROM {dtable} WHERE diskID = {diskID};")
    if ret != ReturnValue.OK or res[0] < 1:
        return Disk.badDisk()
    return Disk(*(res[1][0].values()))


def deleteDisk(diskID: int) -> ReturnValue:
    ret, res = sql_exe(f"DELETE FROM {dtable} WHERE diskID = {diskID};")
    if ret == ReturnValue.OK:
        rows_effected = res[0]
        if rows_effected == 0:
            return ReturnValue.NOT_EXISTS
    return ret

def addRAM(ram: RAM) -> ReturnValue:
    ret, res = sql_exe(f"INSERT INTO {rtable} {create_values_exp(ram.getRamID(), ram.getCompany(), ram.getSize())}")
    return ret

def getRAMByID(ramID: int) -> RAM:
    ret, res = sql_exe(f"SELECT * FROM {rtable} WHERE ramID = {ramID};")
    if ret != ReturnValue.OK or res[0] < 1:
        return RAM.badRAM()
    return RAM(*(res[1][0].values()))

def deleteRAM(ramID: int) -> ReturnValue:
    ret, res = sql_exe(f"DELETE FROM {rtable} WHERE ramID = {ramID};")
    if ret == ReturnValue.OK:
        rows_effected = res[0]
        if rows_effected == 0:
            return ReturnValue.NOT_EXISTS
    return ret

def addDiskAndPhoto(disk: Disk, photo: Photo) -> ReturnValue:
    ret, res = sql_exe_transcation(addDisk_query(disk), addPhoto_query(photo))
    return ret

# Basic API:
def addPhotoToDisk(photo: Photo, diskID: int) -> ReturnValue:
    ret, res = sql_exe_transcation(
        f"INSERT INTO {podtable} {create_values_exp(photo.getPhotoID(), diskID)}",
        f"UPDATE {dtable} SET free_space=free_space-{photo.getSize()} WHERE {dtable}.diskID={diskID}",
    )
    return ret

def removePhotoFromDisk(photo: Photo, diskID: int) -> ReturnValue:
    ret, res = sql_exe_transcation(
        f"UPDATE {dtable} SET free_space=free_space\
            +(SELECT SUM({ptable}.size) FROM {ptable}, {podtable}\
                WHERE {ptable}.photoID={photo.getPhotoID()} AND {podtable}.photoID={ptable}.photoID AND {podtable}.diskID={diskID}\
        )\
        WHERE {dtable}.diskID={diskID}",
        f"DELETE FROM {podtable} WHERE photoID={photo.getPhotoID()} AND diskID={diskID}",
    )
    if ret == ReturnValue.BAD_PARAMS:
        return ReturnValue.OK
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

def getCostForDescription(description: str) -> int:
    ret, res = sql_exe(f"SELECT SUM({dtable}.cost*{ptable}.size)\
        FROM {ptable}, {podtable}, {dtable}\
        WHERE {ptable}.description='{description}' AND {ptable}.photoID={podtable}.photoID AND {dtable}.diskID={podtable}.diskID"
    )
    if ret != ReturnValue.OK:
        return -1
    sum = res[1][0]['sum']
    return 0 if sum == None else sum

def getPhotosCanBeAddedToDisk(diskID: int) -> List[int]:
    ret, res = sql_exe(f"SELECT {ptable}.photoID FROM {ptable}\
        WHERE {ptable}.size <= (SELECT free_space FROM {dtable} WHERE {dtable}.diskID={diskID})\
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
    return sql_exe_list(f"\
        (\
            SELECT {ptable}.photoID FROM {ptable}\
            WHERE {ptable}.size <= (SELECT free_space FROM {dtable} WHERE {dtable}.diskID={diskID})\
        )\
        INTERSECT\
        (\
            SELECT {ptable}.photoID FROM {ptable}\
            WHERE {ptable}.size <=\
            (\
                SELECT SUM({rtable}.size) FROM {rtable}, {rodtable}\
                WHERE {rtable}.ramID={rodtable}.ramID AND {rodtable}.diskID={diskID}\
            )\
        )\
        ORDER BY photoID ASC\
        LIMIT 5"
    )

def isCompanyExclusive(diskID: int) -> bool:
    ret, res = sql_exe(f"\
        SELECT diskID FROM {dtable} WHERE\
        (\
            (SELECT company FROM {dtable} WHERE {dtable}.diskID={diskID})\
            =\
            ALL(SELECT company FROM {rodtable}, {rtable} WHERE {rodtable}.ramID={rtable}.ramID AND {rodtable}.diskID={diskID})\
        )\
        AND\
            {dtable}.diskID={diskID}\
    ")
    if ret != ReturnValue.OK or res[1] == None:
        return False
    return (res[0] != 0)

def isDiskContainingAtLeastNumExists(description : str, num : int) -> bool:
    ret, res = sql_exe(f"SELECT ({podtable}.diskID, COUNT({ptable}.description)) FROM {ptable}, {podtable}\
        WHERE {ptable}.photoID={podtable}.photoID AND {ptable}.description='{description}'\
        GROUP BY {podtable}.diskID\
        HAVING COUNT(*) >= {num}"
    )
    if ret != ReturnValue.OK or res[1] == None:
        return False
    return (res[0] != 0)

def getDisksContainingTheMostData() -> List[int]:
    return sql_exe_list(f"SELECT {dtable}.diskID FROM {dtable}, {podtable}, {ptable}\
        WHERE {dtable}.diskID={podtable}.diskID AND {podtable}.photoID={ptable}.photoID\
        GROUP BY {dtable}.diskID\
        ORDER BY SUM({ptable}.size) DESC\
        LIMIT 5"
    )

# Advanced API:
def getConflictingDisks() -> List[int]:
    return sql_exe_list(f"SELECT DISTINCT pod1.diskID AS did FROM {podtable} pod1, {podtable} pod2\
        WHERE pod1.photoID=pod2.photoID AND pod1.diskID!=pod2.diskID\
        ORDER BY did ASC"
    )

def mostAvailableDisks() -> List[int]:
    return sql_exe_list(f"\
        SELECT {dtable}.diskID FROM {dtable}\
        ORDER BY\
            (SELECT COUNT({ptable}.photoID) FROM {ptable} WHERE {ptable}.size <= {dtable}.free_space) DESC,\
            {dtable}.speed DESC,\
            {dtable}.diskID ASC\
        LIMIT 5\
        "
    )


def getClosePhotos(photoID: int) -> List[int]:
    return sql_exe_list(f"\
        (\
            SELECT {podtable}.photoID FROM {podtable}\
            WHERE\
                {podtable}.diskID IN (SELECT {podtable}.diskID FROM {podtable} WHERE {podtable}.photoID={photoID})\
            AND\
                {podtable}.photoID!={photoID}\
            GROUP BY {podtable}.photoID\
                HAVING 2*COUNT({podtable}.diskID) >= (SELECT COUNT({podtable}.diskID) FROM {podtable} WHERE {podtable}.photoID={photoID})\
        )\
        UNION\
        (\
            SELECT {ptable}.photoID FROM {ptable}\
            WHERE (SELECT COUNT(*) FROM {podtable} WHERE {podtable}.photoID={photoID})=0\
        )\
        ORDER BY photoID ASC\
    ")
