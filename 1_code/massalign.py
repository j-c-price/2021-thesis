import sys
#sys.path.append("..\\massalign\\massalign")
#from core import *
import subprocess
import os
if __name__ == "__main__":
    file1 = "..//massalign//sample_data//test_document_complex.txt"
    file2 = "..//massalign//sample_data//test_document_simple.txt"

    script = ["C:\Python27\python2.exe", "py2-massalign-run.py", file1, file2]

    my_env = os.environ.copy()
    my_env["PATH"] = "/usr/sbin:/sbin:" + my_env["PATH"]
    my_env["PYTHONPATH"] = "."
    process = subprocess.Popen(" ".join(script),
                               shell=True,
                            env=my_env
                               )
    print(process.communicate())