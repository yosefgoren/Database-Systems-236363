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

if __name__ == '__main__':
    # Solution.createTables()
    # Solution.addPhoto(Photo(52, "tree", 9001))
    # Solution.addPhoto(Photo(42, "house", 4444))
    # p = Solution.getPhotoByID(52)
    # print(p)
