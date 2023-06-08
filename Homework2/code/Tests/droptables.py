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

if __name__ == '__main__':
    Solution.dropTables()