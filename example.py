# import the brightsign class
from brightsign import brightsign

# create a bs object with an ip and then call the update function on it
# by default, .update() will update to the version specified as latest_ver in the brightsign class
# this can be overriden by using update with a version parameter: .update('8.5.31') 
brightsign('192.168.1.122').update()
