#!/usr/bin/python27

from shade import *

conn = openstack_cloud(cloud='opentraffic') #osic-hackathon-team.c1')

server1_name = "opentraffic_trafficsync"
server2_name = "opentraffic_cartrack"
server3_name = "opentraffic_cargen"

servers = conn.list_servers()
servers = [str(server.name) for server in servers]
if server1_name in servers:
    conn.delete_server(server1_name)

if server2_name in servers:
    conn.delete_server(server2_name)


#images = conn.list_images()
#image_name="ubuntu"
#image_version="14"
#for x in images:
#   print 'NAME:' + str(x.name)
#   print 'ID  :' + str(x.id) + '\n'
#print image_id

# INSTANCE IMAGE AND FLAVOR - INTERSECTIONS
print "\nCREATE INSTANCE FOR INTERSECTION:"
image_id = "95576f28-afed-4b63-93b4-1d07928930da"
flavor_name = "m2.medium"
flavor_id="8"
external_network="7004a83a-13d3-4dcd-8cf5-52af1ace4cae"
ex_userdata = '''#!/usr/bin/env bash
curl -L -s https://raw.githubusercontent.com/openstack-hackathon/openTraffic/master/setup/setup_zmq.sh; bash setup_zmq.sh intersection
'''

sec_group_name = "opentraffic"
if conn.search_security_groups(sec_group_name):
    pass #print('Security group already exists. Skipping creation.')
else:
    #print('Creating security group.')
    conn.create_security_group(sec_group_name, 'Network access for OpenTraffic IoT application.')
    conn.create_security_group_rule(sec_group_name, 80, 80, 'TCP')
    conn.create_security_group_rule(sec_group_name, 5000, 5000, 'TCP')
    conn.create_security_group_rule(sec_group_name, 9000, 9000, 'TCP')
    conn.create_security_group_rule(sec_group_name, 5555, 5555, 'TCP')
    conn.create_security_group_rule(sec_group_name, 5556, 5556, 'TCP')

intersection = conn.create_server(wait=True, auto_ip=True,
    name=server1_name,
    image=image_id,
    flavor=flavor_id,
    userdata=ex_userdata,
    network=external_network,
    security_groups=['default',sec_group_name])

ip_intersection = intersection.accessIPv4
print ip_intersection

# INSTANCE IMAGE AND FLAVOR - INTERSECTIONS
print "\nCREATE INSTANCE FOR CARS:"
image_id = "95576f28-afed-4b63-93b4-1d07928930da"
flavor_name = "m2.medium"
external_network="7004a83a-13d3-4dcd-8cf5-52af1ace4cae"
ex_userdata = '''#!/usr/bin/env bash
curl -L -s https://raw.githubusercontent.com/openstack-hackathon/openTraffic/master/setup/setup_zmq.sh; bash setup_zmq.sh cartrack_god
''' + ' ' + ip_intersection

sec_group_name = 'opentraffic'
if conn.search_security_groups(sec_group_name):
    pass #print('Security group already exists. Skipping creation.')
else:
    #print('Creating security group.')
    conn.create_security_group(sec_group_name, 'Network access for OpenTraffic IoT application.')
    conn.create_security_group_rule(sec_group_name, 80, 80, 'TCP')
    conn.create_security_group_rule(sec_group_name, 5000, 5000, 'TCP')
    conn.create_security_group_rule(sec_group_name, 9000, 9000, 'TCP')
    conn.create_security_group_rule(sec_group_name, 5555, 5555, 'TCP')
    conn.create_security_group_rule(sec_group_name, 5556, 5556, 'TCP')

cartrack_god = conn.create_server(wait=True, auto_ip=True,
    name=server2_name,
    image=image_id,
    flavor=flavor_id,
    userdata=ex_userdata,
    network=external_network,
    security_groups=['default',sec_group_name])
