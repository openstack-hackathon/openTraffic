import sys
import getopt
import courier
from math import sqrt

CAUTIOUS_DISTANCE=1
ALMOST_HIT=0.01
STEP_REDUCTION=0.9

# Receive parameters
class interception(object):
    def __init__(self, args):
        self.info = {}
        # Parse parameters
        try:
            opts, trails = getopt.getopt(args[1:],"u:c:",["uuid=","coords="])
        except getopt.GetoptError as err:
            print str(err)
            sys.exit(2)

        for opt, arg in opts:
            if opt in ('-u', '--uuid'):
                self.uuid = str(arg)
            if opt in ('-c', '--coords'):
                self.coords = str(arg)

        # Start local sub/pub
        local = ['localhost']
        local2 = ["127.0.0.1"]
        self.courier = courier.apollo(['*'], local2, self.uuid, True)

    def ReceiveUpdate(self):
        car_update = self.courier.ReceiveMessages()
        for key, value in car_update.iteritems()
            self.info[key] = value 
        #make list #sort cars list
        self.cars = [value for key, value in self.info.iteritems()]
        self.cars = sorted(self.cars, key=lambda x: x['dist'])

    @staticmethod
    def ClassifyDirection(direction):
        x, y = direction[0], direction[1]
        if x == 0:
            if y < 0:
                return 'down' 
            elif y > 0:
                return 'up'
        if y == 0:
            if x < 0:
                return 'left'
            elif x > 0:
                return 'right'

    @staticmethod
    def WillCollide(c1,c2,v1,v2, safety):
        a = c2[0] - c1[0]
        b = v2[0] - v1[0]
        c = c2[1] - c1[1]
        d = v2[1] - v1[1]
        t_zero = - (a*b+c*d)/(d**2+b**2)
        min_dist = sqrt((a+b*t_zero)**2 + (c+d*t_zero)**2)
        if min_dist < safety:
            return True
        else:
            return False


    def AnalyzeIncomingCars(self, cars = self.info):
        # cars = [{'coords' : [1,1],
        #          'speed'  : [1,1],
        #          'radius' : 1,
        #          'uuid'  : 1,
        #          'dist' : 1},
        #         {'coords' : [1,1],
        #          'speed'  : [1,1],
        #          'radius' : 1,
        #          'uuid'  : 1,
        #          'dist' : 1}]
        # cars is sorted by dist
        cars = self.cars
        list_indexes = range(len(cars))

        # sepparate into 2 lists by
        street1=[]
        street2=[]
        street1.append(cars[0])
        dir1 = ClassifyDirection(street1[0])
        #NOTE THIS MUST BE MODIFIED TO ACCEPT LANES AND NOT "DIRECTION"
        for i in list_indexes[1:]:
            car = cars[i]
            if ClassifyDirection(car['speed']) == dir1:
                street1.append(car)
            else:
                street2.append(car)

        indexes1 = range(len(street1))
        indexes2 = range(len(street2))
        reduce_percent = 1
        to_reduce=[]
        for i in indexes1:
            for j in indexes2:
                car1, car2 = street1[i], street1[j]
                safety = car1['radius'] + car2['radius'] + CAUTIOUS_DISTANCE
                collision = WillCollide(car1['coords'], car2['coords'], car1['speed'], car2['speed'], safety)
                if collision == True:
                    # identify less effort - lazy method - slow car with less tail
                    if (i/len(indexes1)) < j/len(indexes2):
                        #reduce car1
                        to_reduce = street1[i:]
                        the_rest=street2+street1[:i]
                        while collision:
                            reduce_percent = reduce_percent*STEP_REDUCTION
                            new_speed = [reduce_percent*x for x in car1['speed']]
                            collision = WillCollide(car1['coords'], car2['coords'], new_speed, car2['speed'], safety)
                    else:
                        #reduce car2
                        to_reduce = street2[i:]
                        the_rest=street1+street2[:i]
                        while collision:
                            reduce_percent = reduce_percent*STEP_REDUCTION
                            new_speed = [reduce_percent*x for x in car1['speed']]
                            collision = WillCollide(car1['coords'], car2['coords'], car1['speed'], new_speed, safety)
                    break
            if reduce_percent != 1:
                break
        #reply_to_guilty
        if len(to_reduce) > 0:
            for car in to_reduce:
                new_speed = {'speed' : [reduce_percent*x for x in car['speed']]}
                msg = self.courier.MakeMessage(car['uuid'] + ':' + self.uuid, new_speed)
                self.courier.SendMessage(msg)
        for car in the_rest:
            new_speed = {'speed' : car['speed']}
            msg = self.courier.MakeMessage(car['uuid'] + ':' + self.uuid, new_speed)
            self.courier.SendMessage(msg)


args = sys.argv
intercept = interception(args)

while True:
    intercept.ReceiveUpdate()
    intercept.AnalyzeIncomingCars()