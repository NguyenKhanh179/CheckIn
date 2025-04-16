# gunicorn.conf.py
# Non logging stuff
bind = "0.0.0.0:8443"
workers = 10
# Access log - records incoming HTTP requests
accesslog = "/home/devadmin/logs/gunicorn.access.sme.log"
# Error log - records Gunicorn server goings-on
errorlog = "/home/devadmin/logs/gunicorn.error.sme.log"
# Whether to send Django output to the error log 
capture_output = True
# How verbose the Gunicorn error logs should be 
loglevel = "info"
#certfile ="/home/devadmin/setup/cert/kdtcert/ca.crt"
#keyfile="/home/devadmin/setup/cert/kdtcert/ca.key"
secure_schema_headers={'X-FORWARDED-PROTOCOL': 'ssl', 'X-FORWARDED-PROTO': 'https', 'X-FORWARDED-SSL': 'on'}

