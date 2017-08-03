import piserve

client = piserve.server_connection(('',4000))

while True:   
    piserve.waitForCommand(client,True)
