# config

# genral
# ignores everything starting with '}'
IGNORE_TECHNICAL_OBJECTS = True
# show process/rule name on graph edge
SHOW_EDGE_LABELS = True


# NOT IMPLEMETED
# ToDo TEST!
SHOW_SHORTENED_LABELS = True
# LABEL_LINE_BREAK_ATFER = 10

# make sure to use the right port as configured in tm1 cfg via HTTPPortNumber
SERVER_ADRESS = 'myTM1Server:8080'
#currently no single sign on auth possible
SERVER_USER = 'admin'
SERVER_PASSWORD = 'admin'
# Certificate checking is DISABLED on my machine for testing purposes
# don't be that guy and let someone mitm your tm1 login!
SERVER_CERTIFICATE_VERIFY = False
# make sure this matches you tm1.cfg 'UseSSL' config!
# UseSSL=1 ->
SERVER_PROTOCOLL = 'https://'
# UseSSL=0 ->
# SERVER_PROTOCOLL = 'http://'

# ignore this if you filled the above correctly
SERVER_API_RELATIVE_PATH = '/api/v1/'
SERVER_API_PATH = SERVER_PROTOCOLL + SERVER_ADRESS + SERVER_API_RELATIVE_PATH
