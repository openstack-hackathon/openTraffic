import zmq
import json
import time

ITS_PUBPORT = 5555
ITS_SUBPORT = 5556
# cambiar funcion de ReceiveMessage con un time_limit o no_stop option para recibir todos los mensajes de carros
# sin saber cuantos carros hay. Asi nos ahorramos problemas con carros nuevos, carros salientes, etc.
class apollo(object):
	def __init__(self, pub_list, sub_list, sub_topic, intercept_node = True):
		# create ctx
		self.ctx = zmq.Context()
		self.pubs = {}

		# if interception then bind, else connect
		# if interception only one element in pub_list and sub_list
		if intercept_node == True:
			self.pubs[pub_list[0]] = self.ctx.socket(zmq.PUB)
			pub_address = "tcp://{0}:{1}".format(pub_list[0], ITS_PUBPORT)
			self.pubs[pub_list[0]].bind(pub_address)

			self.subs = self.ctx.socket(zmq.SUB)
			sub_address = "tcp://{0}:{1}".format(sub_list[0], ITS_SUBPORT)
			self.subs.bind(sub_address)
			self.subs.setsockopt(zmq.SUBSCRIBE, sub_topic)
		else: # GOD or CAR, which will create multiple pubs and 1 subs with multiple ports
			for address in pub_list:
				self.pubs[address] = self.ctx.socket(zmq.PUB)
				pub_address = "tcp://{0}:{1}".format(address, ITS_SUBPORT)
				self.pubs[address].connect(pub_address)

			self.subs = self.ctx.socket(zmq.SUB)
			for address in sub_list:
				sub_address = "tcp://{0}:{1}".format(sub_list[0], ITS_PUBPORT)
				self.subs.connect(sub_address)
			self.subs.setsockopt(zmq.SUBSCRIBE, sub_topic)
		time.sleep(1)

	def MakeMessage(self, header, payload): #destination:origin
		packed_payload = json.dumps(payload)
		return [header, packed_payload]

	def ParseMessage(self, msg):
		sender = msg[0].split(":", 2)[1]
		payload = self.byteify(json.loads(msg[1]))
		return sender, payload

	def SendMessage(self, msg):
		for host, publisher in self.pubs.iteritems():
			publisher.send_multipart(msg)

	# Modify to have a timeout of milliseconds
	# receive first msg, then receive with timeout (milliseconds)
	# receives one message, returns... enables quick updates and client side management
	def ReceiveMessages(self, expected_responses = 1):
		output = {}
		msg = self.subs.recv_multipart()
		sender, payload = self.ParseMessage(msg)
		output[sender] = payload
		return output

	def byteify(self, obj):
	    if isinstance(obj, dict):
	        return {self.byteify(key):byteify(value) for key, value in obj.iteritems()}
	    elif isinstance(obj, list):
	        return [self.byteify(element) for element in obj]
	    elif isinstance(obj, unicode):
	        return obj.encode('utf-8')
	    else:
	        return obj