import sys
sys.path.append('..')

import unittest
import Solution
from Utility.ReturnValue import ReturnValue
from Tests.abstractTest import AbstractTest
from Business.Photo import Photo
from Business.RAM import RAM
from Business.Disk import Disk

import Utility.DBConnector as Connector
from Tests.abstractTest import AbstractTest

def cuts():
    print("cutshort")
    exit(0)


class MyTest(AbstractTest):
# Utilities ==================================================
    def assertOk(self, value):
        self.assertEqual(ReturnValue.OK, value)
    
    def init_items(self, *items: list):
        for item in items:
            if type(item) is RAM:
                self.assertOk(Solution.addRAM(item))
            elif type(item) is Disk:
                self.assertOk(Solution.addDisk(item))
            elif type(item) is Photo:
                self.assertOk(Solution.addPhoto(item))
        
# Tests ==================================================
    def t1_averagePhotosSizeOnDisk(self):
        Solution.clearTables()
        avl_tree = Photo(52, "tree", 20)
        Cdrive = Disk(3, "dell-disks", 9001, 30, 33)
        self.init_items(avl_tree, Cdrive)
        self.assertOk(Solution.addPhotoToDisk(avl_tree, Cdrive.getDiskID()))
        avg = Solution.averagePhotosSizeOnDisk(3)
        self.assertEqual(avg, 20)
        print("t1_averagePhotosSizeOnDisk finished succesfully")
    
    def t2_averagePhotosSizeOnDisk(self):
        Solution.clearTables()
        avl_tree = Photo(52, "tree", 20)
        b23_tree = Photo(15, "bibi hamelech", 10)
        Cdrive = Disk(3, "dell-disks", 9001, 30, 33)
        self.init_items(Cdrive, avl_tree, b23_tree)
        self.assertOk(Solution.addPhotoToDisk(avl_tree, Cdrive.getDiskID()))
        self.assertOk(Solution.addPhotoToDisk(b23_tree, Cdrive.getDiskID()))
        self.assertEqual(Solution.averagePhotosSizeOnDisk(Cdrive.getDiskID()), 15)

        Ddrive = Disk(4, "sanDisk", 89, 5000, 30)
        self.assertEqual(Solution.averagePhotosSizeOnDisk(Ddrive.getDiskID()), 0)
        print("t2_averagePhotosSizeOnDisk finished succesfully")

    def t3_getTotalRamOnDisk(self):
        Solution.clearTables()
        r1 = RAM(60, "hp", 300)
        r2 = RAM(1, "hp", 700)
        d = Disk(30, "hp", 9001, 90, 3)
        d2 = Disk(1, "hp", 9001, 90, 3)
        self.init_items(r1, r2, d, d2)

        self.assertOk(Solution.addRAMToDisk(r1.getRamID(), d.getDiskID()))
        self.assertOk(Solution.addRAMToDisk(r2.getRamID(), d.getDiskID()))
        self.assertEqual(Solution.getTotalRamOnDisk(d.getDiskID()), 1000)

        self.assertEqual(Solution.getTotalRamOnDisk(d2.getDiskID()), 0)
        print("t3_getTotalRamOnDisk finished successfully")

    def t4_getPhotosCanBeAddedToDisk(self):
        Solution.clearTables()
        p1 = Photo(111, "hp", 89)
        p2 = Photo(222, "hp", 93)
        p3 = Photo(333, "hp", 90)
        p4 = Photo(444, "hp", 9001)
        d = Disk(30, "hp", 9001, 90, 3)
        self.init_items(p1, p2, p3, p4, d)

        self.assertEqual(Solution.getPhotosCanBeAddedToDisk(d.getDiskID()), [
            p3.getPhotoID(),
            p1.getPhotoID(),
        ])
        print("t4_getPhotosCanBeAddedToDisk finished successfully")
    
    def t5_isDiskContainingAtLeastNumExists(self):
        Solution.clearTables()
        p1 = Photo(111, "memez", 89)
        p2 = Photo(222, "memez", 93)
        p3 = Photo(333, "memez", 90)
        p4 = Photo(444, "yolo", 88)
        d = Disk(30, "hp", 9001, 1000, 3)
        self.init_items(p1, p2, p3, p4, d)
        self.assertOk(Solution.addPhotoToDisk(p1, d.getDiskID()))
        self.assertOk(Solution.addPhotoToDisk(p2, d.getDiskID()))
        self.assertOk(Solution.addPhotoToDisk(p3, d.getDiskID()))
        self.assertOk(Solution.addPhotoToDisk(p4, d.getDiskID()))

        self.assertTrue(Solution.isDiskContainingAtLeastNumExists("memez", 1))
        self.assertTrue(Solution.isDiskContainingAtLeastNumExists("memez", 3))
        self.assertFalse(Solution.isDiskContainingAtLeastNumExists("memez", 4))
        self.assertFalse(Solution.isDiskContainingAtLeastNumExists("yolo", 3))
        self.assertFalse(Solution.isDiskContainingAtLeastNumExists("potatos", 3))

        print("t5_isDiskContainingAtLeastNumExists finished successfully")
    
    def prep_t6(self):
        """
        Disk 1 should have 1 photo of size 1, disk 3 should have 3 photos of size 1...
        """
        Solution.clearTables()
        photos = [Photo(i, "p", 1) for i in range(1, 11)]
        disks = [Disk(i, "sanDisk", 9001, 2000, 10) for i in range(1, 11)]
        self.init_items(*photos, *disks)
        for d in disks:
            for i in range(d.getDiskID()):
                self.assertOk(Solution.addPhotoToDisk(photos[i], d.getDiskID()))
        
    def t6_getDisksContainingTheMostData(self):
        self.prep_t6()
        self.assertEqual(Solution.getDisksContainingTheMostData(), [10, 9, 8, 7, 6])
        print("t6_getDisksContainingTheMostData finished successfully")
    
    def t7_getConflictingDisks(self):
        Solution.clearTables()
        p1, p2, p3 = [Photo(i, "p", 1) for i in range(1, 4)]
        d1, d2, d3 = [Disk(i, "sanDisk", 9001, 2000, 10) for i in range(1, 4)]
        self.init_items(p1, p2, p3, d1, d2, d3)
        self.assertOk(Solution.addPhotoToDisk(p1, d1.getDiskID()))
        self.assertOk(Solution.addPhotoToDisk(p1, d2.getDiskID()))
        self.assertOk(Solution.addPhotoToDisk(p2, d2.getDiskID()))
        self.assertOk(Solution.addPhotoToDisk(p2, d1.getDiskID()))
        self.assertOk(Solution.addPhotoToDisk(p3, d3.getDiskID()))
        self.assertEqual(Solution.getConflictingDisks(), [d1.getDiskID(), d2.getDiskID()])
        print("t7_getConflictingDisks finished successfully")
    
    #PROBOBLY BUG IN TEST
    # def t8_getClosePhotos(self):
    #     Solution.clearTables()
    #     p1, p2, p3 = [Photo(i, "p", 1) for i in range(1, 4)]
    #     d1, d2, d3 = [Disk(i, "sanDisk", 9001, 2000, 10) for i in range(1, 4)]
    #     self.init_items(p1, p2, p3, d1, d2, d3)
    #     self.assertEqual(Solution.getClosePhotos(p1.getPhotoID()), [p1.getPhotoID(), p2.getPhotoID(), p3.getPhotoID()])
    #     self.assertOk(Solution.addPhotoToDisk(p1, d1.getDiskID()))
    #     self.assertOk(Solution.addPhotoToDisk(p1, d2.getDiskID()))
    #     self.assertOk(Solution.addPhotoToDisk(p2, d2.getDiskID()))
    #     self.assertOk(Solution.addPhotoToDisk(p2, d1.getDiskID()))
    #     self.assertOk(Solution.addPhotoToDisk(p3, d3.getDiskID()))
    #     self.assertEqual(Solution.getClosePhotos(p1.getPhotoID()), [p2.getPhotoID()])
    #     self.assertEqual(Solution.getClosePhotos(p2.getPhotoID()), [p1.getPhotoID()])
    #     self.assertEqual(Solution.getClosePhotos(p3.getPhotoID()), [])
    #     print("t8_getClosePhotos finished successfully")
    
    def t9_getCostForDescription(self):
        Solution.clearTables()
        p1 = Photo(111, "memez", 1)
        p2 = Photo(222, "memez", 2)
        p3 = Photo(333, "memez", 3)
        p4 = Photo(444, "yolo", 4)
        d1 = Disk(30, "hp", 9001, 1000, 10)
        d2 = Disk(40, "hp", 9001, 1000, 100)
        self.init_items(p1, p2, p3, p4, d1, d2)
        for p in [p1, p2, p3, p4]:
            self.assertOk(Solution.addPhotoToDisk(p, d1.getDiskID()))
        self.assertOk(Solution.addPhotoToDisk(p3, d2.getDiskID()))
        self.assertOk(Solution.addPhotoToDisk(p4, d2.getDiskID()))
        self.assertEqual((1+2+3)*10 + 3*100, Solution.getCostForDescription("memez"))
        print("t9_getCostForDescription finished successfully")

    def t10_getPhotosCanBeAddedToDiskAndRAM(self):
        Solution.clearTables()
        p1 = Photo(1, "memez", 35)
        p2 = Photo(2, "memez", 5)
        p3 = Photo(3, "memez", 15)
        p4 = Photo(4, "yolo", 10)
        d1 = Disk(1, "hp", 9001, 1000, 10)
        d2 = Disk(2, "hp", 9001, 1000, 100)
        d3 = Disk(3, "hp", 9001, 7, 100)
        r1 = RAM(1, "pip", 10)
        r2 = RAM(2, "pip", 20)
        self.init_items(p1, p2, p3, p4, d1, d2, d3, r1, r2)
        self.assertOk(Solution.addRAMToDisk(r1.getRamID(), d1.getDiskID()))
        self.assertOk(Solution.addRAMToDisk(r2.getRamID(), d1.getDiskID()))
        self.assertOk(Solution.addRAMToDisk(r1.getRamID(), d2.getDiskID()))
        self.assertOk(Solution.addRAMToDisk(r1.getRamID(), d3.getDiskID()))
        self.assertOk(Solution.addRAMToDisk(r2.getRamID(), d3.getDiskID()))
        self.assertEqual(Solution.getPhotosCanBeAddedToDiskAndRAM(d1.getDiskID()), [2, 3, 4])
        self.assertEqual(Solution.getPhotosCanBeAddedToDiskAndRAM(d2.getDiskID()), [2, 4])
        self.assertEqual(Solution.getPhotosCanBeAddedToDiskAndRAM(d3.getDiskID()), [2])
        print("t10_getPhotosCanBeAddedToDiskAndRAM finished successfully")
    
    def t11_mostAvailableDisks(self):
        Solution.clearTables()
        p1 = Photo(1, "memez", 2)
        p2 = Photo(2, "memez", 3)
        p3 = Photo(3, "memez", 4)
        d1 = Disk(1, "hp", 10, 1, 10)
        d2 = Disk(2, "hp", 10, 2, 10)
        d3 = Disk(3, "hp", 20, 3, 10)
        d4 = Disk(4, "hp", 10, 3, 10)
        self.init_items(p1, p2, p3, d1, d2, d3, d4)
        self.assertEqual(Solution.mostAvailableDisks(), [3, 4, 2, 1])
        print("t11_mostAvailableDisks finished successfully")
    
    def t12_isCompanyExclusive(self):
        Solution.clearTables()
        r1 = RAM(1, "hp", 1)
        r2 = RAM(2, "hp", 1)
        r3 = RAM(3, "hp", 1)
        d1 = Disk(1, "hp", 10, 1000, 10)
        d2 = Disk(2, "dell", 10, 1000, 10)
        self.init_items(r1, r2, r3, d1, d2)
        for r in [r1, r2, r3]:
            for d in [d1, d2]:
                self.assertOk(Solution.addRAMToDisk(r.getRamID(), d.getDiskID()))
        self.assertTrue(Solution.isCompanyExclusive(d1.getDiskID()))
        self.assertFalse(Solution.isCompanyExclusive(d2.getDiskID()))
        print("t12_isCompanyExclusive finished successfully")

    #OTHERS:
    def test_Disk_add_get_and_remove(self) -> None:
        self.assertEqual(ReturnValue.OK, Solution.addDisk(Disk(1, "DELL", 10, 10, 10)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addDisk(Disk(2, "DELL", 10, 10, 10)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addDisk(Disk(3, "DELL", 10, 10, 10)), "Should work")
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.addDisk(Disk(1, "DELL", 10, 10, 10)),
                         "ID 1 ALREADY_EXISTS")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addDisk(Disk(4, "HP", 0, 10, 10)), "Speed 0 is illegal")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addDisk(Disk(0, "HP", 10, 10, 10)), "ID 0 is illegal")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addDisk(Disk(4, "HP", 10, 10, 0)), "Cost 0 is illegal")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addDisk(Disk(4, "HP", 10, -1, 10)), "Free space -1 is illegal")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addDisk(Disk(None, "HP", 10, -1, 10)), "NULL is not allowed")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addDisk(Disk(4, None, 10, 10, 10)), "NULL is not allowed")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addDisk(Disk(4, "HP", None, 10, 10)), "NULL is not allowed")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addDisk(Disk(4, "HP", 10, None, 10)), "NULL is not allowed")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addDisk(Disk(4, "HP", 10, 10, None)), "NULL is not allowed")
        self.assertEqual(ReturnValue.OK, Solution.addDisk(Disk(4, "HP", 10, 0, 10)), "Should work")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addDisk(Disk(1, "HP", 0, 10, 10)),
                         "BAD_PARAMS has precedence over ALREADY_EXISTS")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addDisk(Disk(1, None, 10, 10, 10)),
                         "BAD_PARAMS has precedence over ALREADY_EXISTS")
        disk = Solution.getDiskByID(2)
        self.assertEqual(disk.getDiskID(), 2, "Should work")
        self.assertEqual(disk.getCompany(), "DELL", "Should work")
        self.assertEqual(disk.getSpeed(), 10, "Should work")
        self.assertEqual(disk.getCost(), 10, "Should work")
        self.assertEqual(disk.getFreeSpace(), 10, "Should work")
        self.assertEqual(ReturnValue.OK, Solution.deleteDisk(4), "Should work")
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.deleteDisk(4), "ID 4 was already removed")
        Solution.clearTables()
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.deleteDisk(1), "Tables should be empty")
        Solution.dropTables()
        self.assertEqual(ReturnValue.ERROR, Solution.addDisk(Disk(1,"HP",1,1,1)), "Should error")
        self.assertEqual(ReturnValue.ERROR, Solution.deleteDisk(1), "Should error")
        disk = Solution.getDiskByID(1)
        self.assertEqual(disk.getDiskID(), None, "Should return badDisk")
        self.assertEqual(disk.getCompany(), None, "Should return badDisk")
        self.assertEqual(disk.getSpeed(), None, "Should return badDisk")
        self.assertEqual(disk.getCost(), None, "Should return badDisk")
        self.assertEqual(disk.getFreeSpace(), None, "Should return badDisk")
        Solution.createTables()
        self.assertEqual(ReturnValue.OK, Solution.addDisk(Disk(1, "DELL", 10, 10, 10)), "Should work")
        self.assertEqual(ReturnValue.OK,Solution.deleteDisk(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addDisk(Disk(1, "HP", 5, 5, 5)), "Re-adding disk 1")

    def test_Photo_add_get_and_remove(self) -> None:
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(1, "find minimum value", 10)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(2, "find minimum value", 10)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(3, "find minimum value", 10)), "Should work")
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.addPhoto(Photo(1, "find minimum value", 10)),
                         "ID 1 ALREADY_EXISTS")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addPhoto(Photo(4, "find minimum value", -1)),
                         "Size -1 is illegal")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addPhoto(Photo(0, "find minimum value", 10)),
                         "ID 0 is illegal")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addPhoto(Photo(None, "find minimum value", 10)),
                         "NULL is not allowed")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addPhoto(Photo(4, None, 10)), "NULL is not allowed")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addPhoto(Photo(4, "find minimum value", None)),
                         "NULL is not allowed")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(4, "find minimum value", 0)), "Should work")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addPhoto(Photo(1, "find minimum value", -1)),
                         "BAD_PARAMS has precedence over ALREADY_EXISTS")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addPhoto(Photo(1, None, 0)),
                         "BAD_PARAMS has precedence over ALREADY_EXISTS")
        photo = Solution.getPhotoByID(2)
        self.assertEqual(photo.getPhotoID(), 2, "Should work")
        self.assertEqual(photo.getDescription(), "find minimum value", "Should work")
        self.assertEqual(photo.getSize(), 10, "Should work")
        self.assertEqual(ReturnValue.OK, Solution.deletePhoto(Photo(4, "find minimum value", 0)), "Should work")
        Solution.dropTables()
        self.assertEqual(ReturnValue.ERROR, Solution.addPhoto(Photo(1, "HP", 1)), "Should error")
        self.assertEqual(ReturnValue.ERROR, Solution.deletePhoto(Photo(1, "HP", 1)), "Should error")
        photo = Solution.getPhotoByID(1)
        self.assertEqual(photo.getPhotoID(), None, "Should return badPhoto")
        self.assertEqual(photo.getDescription(), None, "Should return badPhoto")
        self.assertEqual(photo.getSize(), None, "Should return badPhoto")
        Solution.createTables()
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(1, "DELL", 10)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.deletePhoto(Photo(1, "DELL", 10)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(2, "HP", 5)), "Re-adding RAM 1")

    def test_add_and_remove_photo_from_disk(self):
        self.assertEqual(ReturnValue.OK, Solution.addDiskAndPhoto(Disk(1, "DELL", 10, 10, 10),
                         Photo(1, "stuff", 7)), "Should work")
        disk = Solution.getDiskByID(1)
        self.assertEqual(disk.getFreeSpace(), 10, "Should work")
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.addPhotoToDisk(Photo(2,"stuff",0),1), "Photo does not exist")
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.addPhotoToDisk(Photo(1, "stuff", 7), 2), "Disk does not exist")
        self.assertEqual(ReturnValue.OK, Solution.addPhotoToDisk(Photo(1, "stuff", 7),1), "Should work")
        disk = Solution.getDiskByID(1)
        self.assertEqual(disk.getFreeSpace(), 3, "Should work")
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.addPhotoToDisk(Photo(1, "stuff", 7),1),
                         "ALREADY_EXISTS has precedence over BAD_PARAMS")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(2, "stuff", 7)), "Should work")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addPhotoToDisk(Photo(2, "stuff", 7),1),
                         "Not enough space on disk")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(3, "stuff", 3)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhotoToDisk(Photo(3, "stuff", 3), 1), "Should work")
        disk = Solution.getDiskByID(1)
        self.assertEqual(disk.getFreeSpace(), 0, "Should work")
        self.assertEqual(ReturnValue.OK, Solution.removePhotoFromDisk(Photo(4, "stuff", 7),1),
                         "Photo does not exist, but should still return OK")
        self.assertEqual(ReturnValue.OK, Solution.removePhotoFromDisk(Photo(2, "stuff", 7), 1),
                         "Photo is not running on disk, but should still return OK")
        self.assertEqual(ReturnValue.OK, Solution.removePhotoFromDisk(Photo(1, "stuff", 7), 2),
                         "Disk does not exist, but should still return OK")
        self.assertEqual(ReturnValue.OK, Solution.removePhotoFromDisk(Photo(1, "stuff", 7), 1), "Should work")
        disk = Solution.getDiskByID(1)
        self.assertEqual(disk.getFreeSpace(), 7, "Should work")
        self.assertEqual(ReturnValue.OK, Solution.removePhotoFromDisk(Photo(3, "stuff", 3), 1), "Should work")
        disk = Solution.getDiskByID(1)
        self.assertEqual(disk.getFreeSpace(), 10, "Should work")
        self.assertEqual(ReturnValue.OK, Solution.removePhotoFromDisk(Photo(1, "stuff", 7), 1),
                         "Photo is not running on disk, but should still return OK")
        self.assertEqual(ReturnValue.OK, Solution.removePhotoFromDisk(Photo(3, "stuff", 3), 1),
                         "Photo is not running on disk, but should still return OK")
        disk = Solution.getDiskByID(1)
        self.assertEqual(disk.getFreeSpace(), 10, "Should work")
        Solution.clearTables()
        self.assertEqual(ReturnValue.OK, Solution.addDiskAndPhoto(Disk(1, "DELL", 10, 10, 10),
                                                                  Photo(1, "stuff", 3)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addDiskAndPhoto(Disk(2, "DELL", 10, 10, 10),
                                                                  Photo(2, "stuff", 3)), "Should work")
        disk = Solution.getDiskByID(1)
        self.assertEqual(disk.getFreeSpace(), 10, "Should work")
        disk = Solution.getDiskByID(2)
        self.assertEqual(disk.getFreeSpace(), 10, "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhotoToDisk(Photo(2, "stuff", 3), 1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhotoToDisk(Photo(2, "stuff", 3), 2), "Should work")
        disk = Solution.getDiskByID(1)
        self.assertEqual(disk.getFreeSpace(), 7, "Should work")
        disk = Solution.getDiskByID(2)
        self.assertEqual(disk.getFreeSpace(), 7, "Should work")
        self.assertEqual(ReturnValue.OK, Solution.deletePhoto(Photo(2, "stuff", 3)), "Should work")
        disk = Solution.getDiskByID(1)
        self.assertEqual(disk.getFreeSpace(), 10, "Photo should have been removed from disk")
        disk = Solution.getDiskByID(2)
        self.assertEqual(disk.getFreeSpace(), 10, "Photo should have been removed from disk")
        self.assertEqual(ReturnValue.OK, Solution.addPhotoToDisk(Photo(1, "stuff", 3), 1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhotoToDisk(Photo(1, "stuff", 3), 2), "Should work")
        disk = Solution.getDiskByID(1)
        self.assertEqual(disk.getFreeSpace(), 7, "Should work")
        disk = Solution.getDiskByID(2)
        self.assertEqual(disk.getFreeSpace(), 7, "Should work")
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.addPhotoToDisk(Photo(2, "stuff", 3), 1), "Photo doesn't exist")
        disk = Solution.getDiskByID(1)
        self.assertEqual(disk.getFreeSpace(), 7, "Should work")
        self.assertEqual(ReturnValue.OK, Solution.removePhotoFromDisk(Photo(1, "stuff", 3),1), "Should work")
        disk = Solution.getDiskByID(1)
        self.assertEqual(disk.getFreeSpace(), 10, "Should work")
        disk = Solution.getDiskByID(2)
        self.assertEqual(disk.getFreeSpace(), 7, "Should work")
        self.assertEqual(ReturnValue.OK, Solution.deletePhoto(Photo(1, "stuff", 3)), "Should work")
        disk = Solution.getDiskByID(1)
        self.assertEqual(disk.getFreeSpace(), 10, "Photo should have been removed from disk")
        disk = Solution.getDiskByID(2)
        self.assertEqual(disk.getFreeSpace(), 10, "Photo should have been removed from disk")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(1,"stuff",3)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhotoToDisk(Photo(1, "stuff", 3), 1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhotoToDisk(Photo(1, "stuff", 3), 2), "Should work")
        self.assertEqual(ReturnValue.OK,Solution.deleteDisk(1), "Should work")
        disk = Solution.getDiskByID(1)
        self.assertEqual(disk.getFreeSpace(), None, "Disk was deleted")
        disk = Solution.getDiskByID(2)
        self.assertEqual(disk.getFreeSpace(), 7, "Disk still has Photo on it")
        Solution.dropTables()
        self.assertEqual(ReturnValue.ERROR, Solution.addPhotoToDisk(Photo(1,"stuff",1),1), "Should error")
        self.assertEqual(ReturnValue.ERROR, Solution.removePhotoFromDisk(Photo(1, "stuff", 1), 1), "Should error")
        Solution.createTables()
        self.assertEqual(ReturnValue.OK, Solution.addDiskAndPhoto(Disk(1, "DELL", 10, 10, 10),
                                                                  Photo(1, "stuff", 7)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhotoToDisk(Photo(1, "stuff", 7), 1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.deletePhoto(Photo(1, "stuff", 7)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(1, "stuff", 17)), "Should work")
        self.assertEqual(ReturnValue.BAD_PARAMS, Solution.addPhotoToDisk(Photo(1, "stuff", 17), 1), "Photo too big now")
        self.assertEqual(ReturnValue.OK, Solution.deleteDisk(1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addDisk(Disk(1, "DELL", 10, 20, 10)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhotoToDisk(Photo(1, "stuff", 17), 1), "Disk big enough now")

    def test_add_and_remove_ram_from_disk(self):
        self.assertEqual(ReturnValue.OK, Solution.addDisk(Disk(1,"DELL",10,10,10)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addRAM(RAM(1, "DELL", 10)), "Should work")
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.addRAMToDisk(1,2), "Disk doesn't exist")
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.addRAMToDisk(2,1), "RAM doesn't exist")
        self.assertEqual(ReturnValue.OK, Solution.addRAMToDisk(1,1), "Should work")
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.addRAMToDisk(1, 1), "RAM is already on disk")
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.removeRAMFromDisk(1,2), "Disk doesn't exist")
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.removeRAMFromDisk(2,1), "RAM doesn't exist")
        self.assertEqual(ReturnValue.OK, Solution.removeRAMFromDisk(1,1), "Should work")
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.removeRAMFromDisk(1,1), "RAM was already removed")
        self.assertEqual(ReturnValue.OK, Solution.addRAMToDisk(1, 1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.deleteRAM(1), "Should work")
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.removeRAMFromDisk(1,1),
                         "RAM should have been removed when deleted")
        self.assertEqual(ReturnValue.OK, Solution.addDisk(Disk(2, "DELL", 10, 10, 10)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addRAM(RAM(1, "DELL", 10)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addRAM(RAM(2, "DELL", 10)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addRAMToDisk(1,1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addRAMToDisk(2,1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addRAMToDisk(1,2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addRAMToDisk(2,2), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.deleteRAM(1), "Should work")
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.removeRAMFromDisk(1,1),
                         "RAM should have been removed when deleted")
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.removeRAMFromDisk(1,2),
                         "RAM should have been removed when deleted")
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.addRAMToDisk(2,1), "RAM is already on disk")
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.addRAMToDisk(2,2), "RAM is already on disk")
        self.assertEqual(ReturnValue.OK, Solution.deleteDisk(1), "Should work")
        self.assertEqual(ReturnValue.NOT_EXISTS, Solution.addRAMToDisk(2,1), "Disk was deleted")
        self.assertEqual(ReturnValue.ALREADY_EXISTS, Solution.addRAMToDisk(2,2), "RAM is already on disk")
        Solution.dropTables()
        self.assertEqual(ReturnValue.ERROR, Solution.addRAMToDisk(1, 1), "Should error")
        self.assertEqual(ReturnValue.ERROR, Solution.removeRAMFromDisk(1, 1), "Should error")

    def test_getClosePhotos(self):
        self.assertEqual(ReturnValue.OK,Solution.addPhoto(Photo(1,"stuff",0)),"Should work")
        self.assertListEqual([], Solution.getClosePhotos(1), "Photo can't be close to itself")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(2, "stuff", 0)), "Should work")
        self.assertListEqual([2],Solution.getClosePhotos(1),"Close in an empty sense")
        self.assertListEqual([1], Solution.getClosePhotos(2), "Close in an empty sense")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(3, "stuff", 0)), "Should work")
        self.assertListEqual([2,3], Solution.getClosePhotos(1), "Close in an empty sense")
        self.assertListEqual([1,3], Solution.getClosePhotos(2), "Close in an empty sense")
        self.assertListEqual([1,2], Solution.getClosePhotos(3), "Close in an empty sense")
        self.assertEqual(ReturnValue.OK,Solution.addDisk(Disk(1,"HP",1,1,1)),"Should work")
        self.assertListEqual([2, 3], Solution.getClosePhotos(1), "Shouldn't change")
        self.assertListEqual([1, 3], Solution.getClosePhotos(2), "Shouldn't change")
        self.assertListEqual([1, 2], Solution.getClosePhotos(3), "Shouldn't change")
        self.assertEqual(ReturnValue.OK,Solution.addPhotoToDisk(Photo(1,"stuff",0),1),"Should work")
        self.assertListEqual([], Solution.getClosePhotos(1), "Can't be Close in an empty sense any more")
        self.assertListEqual([1,3], Solution.getClosePhotos(2), "Still close in an empty sense")
        self.assertListEqual([1,2], Solution.getClosePhotos(3), "Still close in an empty sense")
        self.assertEqual(ReturnValue.OK, Solution.addPhotoToDisk(Photo(2, "stuff", 0), 1), "Should work")
        self.assertListEqual([2], Solution.getClosePhotos(1), "photos 1 and 2 run on same disk")
        self.assertListEqual([1], Solution.getClosePhotos(2), "photos 1 and 2 run on same disk")
        self.assertListEqual([1, 2], Solution.getClosePhotos(3), "Still close in an empty sense")
        self.assertEqual(ReturnValue.OK,Solution.addDisk(Disk(2,"HP",1,1,1)),"Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhotoToDisk(Photo(3, "stuff", 0), 2), "Should work")
        self.assertListEqual([2], Solution.getClosePhotos(1), "Shouldn't change")
        self.assertListEqual([1], Solution.getClosePhotos(2), "Shouldn't change")
        self.assertListEqual([], Solution.getClosePhotos(3), "Can't be Close in an empty sense any more")
        self.assertEqual(ReturnValue.OK, Solution.addPhotoToDisk(Photo(3, "stuff", 0), 1), "Should work")
        self.assertListEqual([2, 3], Solution.getClosePhotos(1), "Everyone is running on disk 1")
        self.assertListEqual([1, 3], Solution.getClosePhotos(2), "Everyone is running on disk 1")
        self.assertListEqual([1, 2], Solution.getClosePhotos(3), "Everyone is running on disk 1, which is 50%")
        self.assertEqual(ReturnValue.OK, Solution.addDisk(Disk(3, "HP", 1, 1, 1)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhotoToDisk(Photo(3, "stuff", 0), 3), "Should work")
        self.assertListEqual([2, 3], Solution.getClosePhotos(1), "Shouldn't change")
        self.assertListEqual([1, 3], Solution.getClosePhotos(2), "Shouldn't change")
        self.assertListEqual([], Solution.getClosePhotos(3), "Not 50% any more")
        self.assertEqual(ReturnValue.OK, Solution.addDisk(Disk(4, "HP", 1, 1, 1)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhotoToDisk(Photo(3, "stuff", 0), 4), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhotoToDisk(Photo(2, "stuff", 0), 2), "Should work")
        self.assertListEqual([2, 3], Solution.getClosePhotos(1), "Everyone is running on disk 1")
        self.assertListEqual([1, 3], Solution.getClosePhotos(2), "Everyone is running on disk 1, which is 50%")
        self.assertListEqual([2], Solution.getClosePhotos(3), "Exactly 50%")
        self.assertEqual(ReturnValue.OK, Solution.addPhotoToDisk(Photo(1, "stuff", 0), 4), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhotoToDisk(Photo(2, "stuff", 0), 4), "Should work")
        self.assertListEqual([1,2], Solution.getClosePhotos(3), "2 is closer but should be ordered by id")
        self.assertEqual(ReturnValue.OK,Solution.deleteDisk(4),"Should work")
        self.assertListEqual([2,3], Solution.getClosePhotos(1), "Everyone is running on disk 1")
        self.assertListEqual([1,3], Solution.getClosePhotos(2), "Everyone is running on disk 1, which is 50%")
        self.assertListEqual([2], Solution.getClosePhotos(3), "2 is running on 2 and 3")
        self.assertEqual(ReturnValue.OK,Solution.deletePhoto(Photo(2, "stuff", 0)),"Should work")
        self.assertListEqual([3], Solution.getClosePhotos(1), "Photo 2 deleted")
        self.assertListEqual([], Solution.getClosePhotos(3), "Photo 2 deleted")
        self.assertEqual(ReturnValue.OK, Solution.removePhotoFromDisk(Photo(3, "stuff", 0), 2), "Should work")
        self.assertListEqual([3], Solution.getClosePhotos(1), "Shouldn't change")
        self.assertListEqual([1], Solution.getClosePhotos(3), "1 is now close")
        Solution.clearTables()
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(1, "stuff", 0)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(12, "stuff", 0)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(8, "stuff", 0)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(54, "stuff", 0)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(9, "stuff", 0)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(2, "stuff", 0)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(23, "stuff", 0)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(7, "stuff", 0)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(10, "stuff", 0)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(11, "stuff", 0)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(3, "stuff", 0)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(15, "stuff", 0)), "Should work")
        self.assertListEqual([1, 2, 7, 8, 9, 10, 11, 12, 15, 23], Solution.getClosePhotos(3),
                             "Max 10, should not include 3 itself")
    

    def test_getPhotosCanBeAddedToDiskAndRAM(self):
        self.assertListEqual([], Solution.getPhotosCanBeAddedToDiskAndRAM(1), "Disk doesn't exist. Should return empty list")
        self.assertEqual(ReturnValue.OK, Solution.addDisk(Disk(1,"HP",10,10,10)),"Should work")
        self.assertEqual(ReturnValue.OK, Solution.addDisk(Disk(2,"HP",10,20,10)),"Should work")
        self.assertListEqual([], Solution.getPhotosCanBeAddedToDiskAndRAM(1), "No photos")
        self.assertListEqual([], Solution.getPhotosCanBeAddedToDiskAndRAM(2), "No photos")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(1,"stuff",3)), "Should work")
        self.assertListEqual([], Solution.getPhotosCanBeAddedToDiskAndRAM(1), "Disk 1 has no RAM")
        self.assertListEqual([], Solution.getPhotosCanBeAddedToDiskAndRAM(2), "Disk 2 has no RAM")
        self.assertEqual(ReturnValue.OK, Solution.addRAM(RAM(1,"HP",10)), "Should work")
        self.assertListEqual([], Solution.getPhotosCanBeAddedToDiskAndRAM(1), "Disk 1 has no RAM")
        self.assertListEqual([], Solution.getPhotosCanBeAddedToDiskAndRAM(2), "Disk 2 has no RAM")
        self.assertEqual(ReturnValue.OK,Solution.addRAMToDisk(1,1), "Should work")
        self.assertListEqual([1], Solution.getPhotosCanBeAddedToDiskAndRAM(1), "Disk 1 now has 10 RAM")
        self.assertListEqual([], Solution.getPhotosCanBeAddedToDiskAndRAM(2), "Disk 2 still has no RAM")
        self.assertEqual(ReturnValue.OK, Solution.addRAM(RAM(2, "HP", 10)), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addRAMToDisk(2,1), "Should work")
        self.assertEqual(ReturnValue.OK, Solution.addRAMToDisk(2,2), "Should work")
        self.assertListEqual([1], Solution.getPhotosCanBeAddedToDiskAndRAM(1), "Shouldn't change")
        self.assertListEqual([1], Solution.getPhotosCanBeAddedToDiskAndRAM(2), "Disk 2 now has 10 RAM")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(2, "stuff", 15)), "Should work")
        self.assertListEqual([1], Solution.getPhotosCanBeAddedToDiskAndRAM(1), "Not enough free space for Photo 2")
        self.assertListEqual([1], Solution.getPhotosCanBeAddedToDiskAndRAM(2), "Not enough RAM for Photo 2")
        self.assertEqual(ReturnValue.OK, Solution.removeRAMFromDisk(2,2), "Should work")
        self.assertListEqual([1], Solution.getPhotosCanBeAddedToDiskAndRAM(1), "Shouldn't change")
        self.assertListEqual([], Solution.getPhotosCanBeAddedToDiskAndRAM(2), "Disk 2 now has no RAM")
        self.assertEqual(ReturnValue.OK, Solution.addRAMToDisk(2,2), "Should work")
        self.assertListEqual([1], Solution.getPhotosCanBeAddedToDiskAndRAM(1), "Shouldn't change")
        self.assertListEqual([1], Solution.getPhotosCanBeAddedToDiskAndRAM(2), "Disk 2 now has 10 RAM")
        self.assertEqual(ReturnValue.OK, Solution.deleteRAM(2), "Should work")
        self.assertListEqual([1], Solution.getPhotosCanBeAddedToDiskAndRAM(1), "Disk 1 should still have 10 RAM")
        self.assertListEqual([], Solution.getPhotosCanBeAddedToDiskAndRAM(2), "Disk 2 now has no RAM")
        self.assertEqual(ReturnValue.OK, Solution.addRAMToDisk(1,2), "Should work")
        self.assertEqual(ReturnValue.OK,Solution.deleteDisk(2), "Should work")
        self.assertListEqual([1], Solution.getPhotosCanBeAddedToDiskAndRAM(1), "Shouldn't change")
        self.assertListEqual([], Solution.getPhotosCanBeAddedToDiskAndRAM(2), "Disk 2 was deleted")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(5, "stuff", 3)), "Should work")
        self.assertListEqual([1,5], Solution.getPhotosCanBeAddedToDiskAndRAM(1), "Photo 5 available, ascending")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(3, "stuff", 3)), "Should work")
        self.assertListEqual([1,3,5], Solution.getPhotosCanBeAddedToDiskAndRAM(1), "Photo 3 available, ascending")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(10, "stuff", 3)), "Should work")
        self.assertListEqual([1,3,5,10], Solution.getPhotosCanBeAddedToDiskAndRAM(1), "Photo 10 available")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(20, "stuff", 3)), "Should work")
        self.assertListEqual([1,3,5,10,20], Solution.getPhotosCanBeAddedToDiskAndRAM(1), "Photo 20 available")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(15, "stuff", 3)), "Should work")
        self.assertListEqual([1,3,5,10,15], Solution.getPhotosCanBeAddedToDiskAndRAM(1), "Max 5")
        self.assertEqual(ReturnValue.OK, Solution.deletePhoto(Photo(15, "stuff", 3)), "Should work")
        self.assertListEqual([1,3,5,10,20], Solution.getPhotosCanBeAddedToDiskAndRAM(1), "Photo 15 deleted")
        self.assertEqual(ReturnValue.OK,Solution.addPhotoToDisk(Photo(20, "stuff", 3),1), "Should work")
        self.assertListEqual([1, 3, 5, 10, 20], Solution.getPhotosCanBeAddedToDiskAndRAM(1),
                             "List can include photos already on on disk")
        self.assertEqual(ReturnValue.OK, Solution.deleteRAM(1), "Should work")
        self.assertListEqual([], Solution.getPhotosCanBeAddedToDiskAndRAM(1), "Disk 1 now has no RAM")
        self.assertEqual(ReturnValue.OK, Solution.addPhoto(Photo(7, "stuff", 0)), "Should work")
        #HERE
        self.assertListEqual([7],Solution.getPhotosCanBeAddedToDiskAndRAM(1),
                             "Photo 7 requires no space, so can be added to RAM even if there is no RAM")
        cuts()
        self.assertEqual(ReturnValue.OK, Solution.deleteDisk(1), "Should work")
        self.assertEqual([],Solution.getPhotosCanBeAddedToDiskAndRAM(1), "Disk doesn't exist")
        Solution.dropTables()
        self.assertEqual([], Solution.getPhotosCanBeAddedToDiskAndRAM(1), "Should error and return empty list")


if __name__ == '__main__':
    # t.t8_getClosePhotos()

    Solution.createTables()
    Solution.clearTables()
    t = MyTest()
    t.t1_averagePhotosSizeOnDisk()
    t.t2_averagePhotosSizeOnDisk()
    t.t3_getTotalRamOnDisk()
    t.t4_getPhotosCanBeAddedToDisk()
    t.t5_isDiskContainingAtLeastNumExists()
    t.t6_getDisksContainingTheMostData()
    t.t7_getConflictingDisks()
    t.t9_getCostForDescription()
    t.t10_getPhotosCanBeAddedToDiskAndRAM()
    t.t11_mostAvailableDisks()
    t.t12_isCompanyExclusive()
    
    Solution.clearTables()
    t.test_Disk_add_get_and_remove()
    Solution.clearTables()
    t.test_Photo_add_get_and_remove()
    Solution.clearTables()
    t.test_add_and_remove_photo_from_disk()
    Solution.clearTables()
    t.test_add_and_remove_ram_from_disk()
    Solution.clearTables()
    t.test_getClosePhotos()
    # Solution.clearTables()
    # t.test_getPhotosCanBeAddedToDiskAndRAM()

    print("finsihed all t1, success")