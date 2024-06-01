import os
import unittest.mock
from lab_4 import *

def test_create_snapshot():

    with unittest.mock.patch('os.listdir') as mock_listdir:
        mock_listdir.return_value = ['file1.txt', 'file2.txt', 'file3.txt']


        folder_path = 'C:/Users/PC/Downloads/python/snapshots'
        create_snapshot(folder_path)


        snapshot_file_path = f'{snapshots_path}/{os.path.basename(folder_path)}.txt'
        assert os.path.exists(snapshot_file_path)


        with open(snapshot_file_path, 'r') as f:
            snapshot_contents = f.readlines()
        assert len(snapshot_contents) == 3
        assert 'file1.txt' in snapshot_contents[0]
        assert 'file2.txt' in snapshot_contents[1]
        assert 'file3.txt' in snapshot_contents[2]