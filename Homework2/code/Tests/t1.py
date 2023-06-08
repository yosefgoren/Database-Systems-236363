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
    
    def t8_getClosePhotos(self):
        Solution.clearTables()
        p1, p2, p3 = [Photo(i, "p", 1) for i in range(1, 4)]
        d1, d2, d3 = [Disk(i, "sanDisk", 9001, 2000, 10) for i in range(1, 4)]
        self.init_items(p1, p2, p3, d1, d2, d3)
        self.assertEqual(Solution.getClosePhotos(p1.getPhotoID()), [p1.getPhotoID(), p2.getPhotoID(), p3.getPhotoID()])
        self.assertOk(Solution.addPhotoToDisk(p1, d1.getDiskID()))
        self.assertOk(Solution.addPhotoToDisk(p1, d2.getDiskID()))
        self.assertOk(Solution.addPhotoToDisk(p2, d2.getDiskID()))
        self.assertOk(Solution.addPhotoToDisk(p2, d1.getDiskID()))
        self.assertOk(Solution.addPhotoToDisk(p3, d3.getDiskID()))
        self.assertEqual(Solution.getClosePhotos(p1.getPhotoID()), [p2.getPhotoID()])
        self.assertEqual(Solution.getClosePhotos(p2.getPhotoID()), [p1.getPhotoID()])
        self.assertEqual(Solution.getClosePhotos(p3.getPhotoID()), [])
        print("t8_getClosePhotos finished successfully")
    
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

if __name__ == '__main__':
    t = MyTest()
    t.t1_averagePhotosSizeOnDisk()
    t.t2_averagePhotosSizeOnDisk()
    t.t3_getTotalRamOnDisk()
    t.t4_getPhotosCanBeAddedToDisk()
    t.t5_isDiskContainingAtLeastNumExists()
    t.t6_getDisksContainingTheMostData()
    t.t7_getConflictingDisks()
    t.t8_getClosePhotos()
    t.t9_getCostForDescription()
    t.t10_getPhotosCanBeAddedToDiskAndRAM()
    t.t11_mostAvailableDisks()
    t.t12_isCompanyExclusive()

    #TODO: check removing from photo from a disk where it is not located (so don't increase free_space)