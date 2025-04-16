# Import `os`
import os

# Retrieve current working directory (`cwd`)
cwd = os.getcwd()
cwd

# Change directory
os.chdir("E:/work/bancas/uat")

# List all files and directories in current directory
list_files = os.listdir('.')
print(list_files)