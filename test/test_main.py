import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
import subprocess
from main import execute_rsync_download, execute_rsync_upload, REMOTE, LOCAL

class TestExecuteRsyncDownload(unittest.TestCase):

    @patch('subprocess.Popen')
    def test_execute_rsync_download_success(self, mock_popen):
        mock_process = MagicMock()
        mock_process.stdout = iter(["file1\n", "file2\n"])
        mock_process.returncode = 0
        mock_popen.return_value = mock_process

        process = execute_rsync_download(REMOTE, LOCAL)
        
        mock_popen.assert_called_once_with(
            ["rsync", "-avz", REMOTE + '/', LOCAL],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        self.assertEqual(process, mock_process)
        self.assertEqual(process.returncode, 0)

    @patch('subprocess.Popen')
    def test_execute_rsync_download_failure(self, mock_popen):
        mock_process = MagicMock()
        mock_process.stdout = iter(["error\n"])
        mock_process.returncode = 1
        mock_popen.return_value = mock_process

        process = execute_rsync_download(REMOTE, LOCAL)
        
        mock_popen.assert_called_once_with(
            ["rsync", "-avz", REMOTE + '/', LOCAL],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        self.assertEqual(process, mock_process)
        self.assertEqual(process.returncode, 1)

class TestExecuteRsyncUpload(unittest.TestCase):
    
    @patch('subprocess.Popen')
    def test_execute_rsync_upload_success(self, mock_popen):
        mock_process = MagicMock()
        mock_process.stdout = iter(["file1\n", "file2\n"])
        mock_process.returncode = 0
        mock_popen.return_value = mock_process

        process = execute_rsync_upload(LOCAL, REMOTE)
        
        mock_popen.assert_called_once_with(
            ["rsync", "-avz", "--update", LOCAL + '/', REMOTE],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        self.assertEqual(process, mock_process)
        self.assertEqual(process.returncode, 0)

    @patch('subprocess.Popen')
    def test_execute_rsync_upload_failure(self, mock_popen):
        mock_process = MagicMock()
        mock_process.stdout = iter(["error\n"])
        mock_process.returncode = 1
        mock_popen.return_value = mock_process

        process = execute_rsync_upload(LOCAL, REMOTE)
        
        mock_popen.assert_called_once_with(
            ["rsync", "-avz", "--update", LOCAL + '/', REMOTE],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        self.assertEqual(process, mock_process)
        self.assertEqual(process.returncode, 1)


if __name__ == '__main__':
    unittest.main()