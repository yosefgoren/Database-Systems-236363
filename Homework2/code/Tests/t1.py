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

# import inspect
# def get_cur_func_name():
#    print(inspect.stack()[0][3])

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

if __name__ == '__main__':
    t = MyTest()
    t.t1_averagePhotosSizeOnDisk()
    t.t2_averagePhotosSizeOnDisk()
    t.t3_getTotalRamOnDisk()
    t.t4_getPhotosCanBeAddedToDisk()