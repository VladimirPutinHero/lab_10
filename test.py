import os
import pytest
from unittest.mock import patch
from datetime import datetime
from lab_4 import *

@patch('os.listdir')
def test_create_snapshot(mock_listdir):
    # Arrange
    snapshot_path = 'C:/Users/PC/Downloads/python/snapshots'
    mock_listdir.return_value = ['file1.txt', 'file2.py', 'file3.jpg']

    # Act
    create_snapshot(folder_path)

    # Assert
    snapshot_file_path = f'{snapshots_path}/{os.path.basename(folder_path)}.txt'
    assert os.path.exists(snapshot_file_path)

    with open(snapshot_file_path, 'r') as f:
        lines = f.readlines()

    assert len(lines) == 3
    for i, line in enumerate(lines):
        file_name, file_creation_time = line.strip().split()
        assert file_name == f'file{i+1}.{"txt" if i == 0 else "py" if i == 1 else "jpg"}'
        assert datetime.strptime(file_creation_time, '%d%m%Y%H%M%S')

    # Cleanup
    os.remove(snapshot_file_path)
