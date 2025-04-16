base_dir = r'D:\Source_MB\\checkin\\venv'
my_app = r'D:\Source_MB\\checkin'
activate_this = base_dir+'/Scripts/activate'
# execfile(activate_this, dict(__file__=activate_this))
exec(open(activate_this).read(),dict(__file__=activate_this))

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir(base_dir+'/lib/python3.9/site-packages')
site.addsitedir(base_dir+'/lib64/python3.9/site-packages')




# Add the app's directory to the PYTHONPATH
sys.path.append(my_app)
sys.path.append(my_app+'/app')

from app import app as application
