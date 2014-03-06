from bluetooth import *
from serial_stub import *
from serial_comminication import *
import json

def goodbye(client_sock, server_sock):
    if client_sock:
        print_msg("goodbye", "Closing bluetooth client")
        client_sock.close()
    if server_sock:
        print_msg("goodbye", "Closing bluetooth server")
        server_sock.close()

class androidCommander(object):
    def __init__(self, serial_commander):
        self.client_sock = None
        self.server_sock = None
        self.is_connected = False
        #self.serial_commander = SerialCommanderStub()
        self.serial_commander = serial_commander

        self.map_outgoing = Queue()
        self.name = "Android Commander"


    def is_connect(self):
        return self.is_connected

    def init_bluetooth(self, btport = 4):
        """
        manual connect to nexus
        channel port: 4
        nexus address "08:60:6E:A5:90:50" #mac number
        """
        self.server_sock = BluetoothSocket( RFCOMM )
        self.server_sock.bind(("", btport))
        self.server_sock.listen(1)
        port = self.server_sock.getsockname()[1]
        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        advertise_service(self.server_sock, "SampleServer",
                          service_id=uuid,
                          service_classes=[uuid, SERIAL_PORT_CLASS],
                          profiles=[SERIAL_PORT_PROFILE],
        )
        import atexit
        atexit.register(goodbye, None, self.server_sock)
        #print "atexit registered 1"
        print_msg(self.name, "waiting for connection on RFCOMM channel %d" % port)
        self.client_sock, client_info = self.server_sock.accept() # blocking
        atexit.register(goodbye, self.client_sock, self.server_sock)
        #print "atexit registered 2"
        print_msg(self.name, "Accepted connection from "+str(client_info))
        self.is_connected = True


    def disconnect(self):
        print "disconnect"
        self.server_sock.close()

    def connect(self):
        """
        auto connect to nexus
        """
        print_msg(self.name, "Connecting...")
        self.client_sock = BluetoothSocket( RFCOMM )
        uuid = "00001101-0000-1000-8000-00805F9B34FB"
        btaddr = "08:60:6E:A5:90:50"
        service_match = find_service(uuid = uuid, address = btaddr)
        while len(service_match) ==  0:
                service_match = find_service(uuid = uuid, address = btaddr)

        first_match = service_match[0]
        port = first_match["port"]
        host = first_match["host"]
        self.client_sock.connect((host,port))
        print_msg(self.name, "Connected to "+str(host))
        self.is_connected = True

    def write(self,msg):
        """
        write to nexus
        :status + msg
        """
        try:
            while self.is_connect():
            #while self.is_connect():
                self.client_sock.send("status "+str(msg))
                print_msg(self.name, "Write to Android: %s" % msg)
                return True

        except IOError:
            print_msg(self.name, "disconnected")
            self.is_connected = False
            self.client_sock.close()
            self.disconnect()

    def write_map(self,msg):
        """
        write to nexus
        :status + msg
        """
        try:
            while self.is_connect():
            #while self.is_connect():
                #self.client_sock.send("GRID 5 5 2 2 3 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0")#str(msg))
                self.client_sock.send("GRID 15 20 "+str(msg))
                print_msg(self.name, "Write to Android: %s" % msg[:15])
                return True

        except IOError:
            print_msg(self.name, "disconnected")
            self.is_connected = False
            self.client_sock.close()
            self.disconnect()

    def __translate_robot_location(self, x, y):
        """
        :param x: int
        :param y: int
        :return: String
        """
        c1 = str(x)+str(y)
        c2 = str(x+1)+str(y)
        #c1 = ("0"+str(x))[-2:]+("0"+str(y))[-2:]
        #c2 = ("0"+str(x+1))[-2:]+("0"+str(y))[-2:]
        #c3 = ("0"+str(x))[-2:]+("0"+str(y+1))[-2:]
        #c4 = ("0"+str(x+1))[-2:]+("0"+str(y+1))[-2:]
        #print "Robot Location: " + c1+c2+c3+c4
        print_msg(self.name, "Robot Location: " + c1+c2)
        return c1+c2



    def update_android(self, map_coordinate, location_coordinate):
        """
        Main Flow of Auto
        Send: F1, L90, R90
        """
        robot_x, robot_y = location_coordinate.split(",")
        #map_x, map_y = map_coordinate.split(",")
        robot_coordinate = self.__translate_robot_location(int(robot_x), int(robot_y))
        #robot_coord = str(robot_coordinate)+str(map_coordinate)
        final_coordinate = " ".join(str(robot_coordinate)+str(map_coordinate))
        self.write_map(str(final_coordinate))
        #return final_coordinate


    def read_for_remote_control(self):
        """
        listen from nexus
        Main Flow of Remote Control
        """
        try:
            if self.is_connect():
                print_msg(self.name, "Receiving socket package")
                b_data = self.client_sock.recv(1024)
                print "Received from Android: %s" % b_data
                if len(b_data) != 0:
                    print_msg(self.name, "decoding")
                    message =  self.__decode_n_execute(b_data)
                    self.write(message)
        except IOError:
            print_msg(self.name, "disconnected")
            self.is_connected = False
            self.client_sock.close()
            self.disconnect()

    def __execute_msg(self, function_code, parameter):
        #self.write("Forward")
        self.serial_commander.command_put(function_code, parameter)
        while True:
            lst = self.serial_commander.response_pop()
            print_msg(self.name, "Waiting for response")
            print lst
            if lst==None:
                time.sleep(2)
                continue
            else:
                ack, type_data, data = lst[0], lst[1], lst[2]
                print ack, type_data, data
                if ack==True:
                    break
                else:
                    continue


    def __decode_n_execute(self, msg):
        if msg == "w":
            self.__execute_msg(0, 10)
            return "Forward"
        elif msg == "a":
            self.__execute_msg(1, 90)
            return "Turn Left"
        elif msg == "d":
            self.__execute_msg(2, 90)
            return "Turn Right"
        elif msg == "run":#shortest path
            #self.write("run")
            return ""
        elif msg == "explore":#explore maze
            #self.write("explore")
            return ""

    ########################################################################################################################
    def map_pop_n_exe(self):
        if not self.map_outgoing.empty():
            #self.ack = False
            command_pair = self.map_outgoing.get()
            self.update_android(str(command_pair[0]), str(command_pair[1]))
            #self.write_map(str(command_pair[0])+str(command_pair[1]))

    def map_put(self, map_grid, location):
        self.map_outgoing.put([map_grid, location])

    def is_map_empty(self):
        return self.map_outgoing.empty()


class androidThread(AbstractThread):
    @Override(AbstractThread)
    def __init__(self, name, serial_commander, mode, production):
        """
        :param name: name for the thread
        :param serial_commander: Shared resoureces
        :param mode: either "auto" or "control"
        :param production: Boolean, if false, use __test_run_pipeline_style rather than waiting for PC
        """
        super(androidThread, self).__init__(name)
        self.android_commander = androidCommander(serial_commander)
        self.mode = mode
        self.production = production


    @Override(AbstractThread)
    def run(self):
        self.print_msg("Starting")
        if self.mode=="control":
            self.print_msg("In remote control mode")
            self.__remote_control_mode()
        else:
            self.production("In auto mode")
            self.__auto_mode()
        self.print_msg("Ending")


    def __auto_mode(self):
        """
        Auto run mode. Android update the map
        """
        while True:
            while True:
                if self.android_commander.is_connect():
                    break
                self.android_commander.init_bluetooth()
                time.sleep(1)
            if self.android_commander.is_map_empty():
                if self.production:
                    self.print_msg("Waiting for map update")
                    time.sleep(1)
                    continue
                else:
                    self.__test_run_pipeline_style()

            else:
                self.print_msg("Updating map")
                self.android_commander.map_pop_n_exe()



    def __remote_control_mode(self):
        """
        Android remotely control the robot
        """
        while True:
            while True:
                if self.android_commander.is_connect():
                    break
                self.android_commander.init_bluetooth()
                time.sleep(1)

            self.android_commander.read_for_remote_control()
            time.sleep(1)


    def __test_run_pipeline_style(self):
        loc = ""
        for i in range(300): #300
            loc = loc+str(i%2)
        msg_received = "{\"map\":\"%s\", \"location\":\"1,1\"}"%loc
        msg_json = json.loads(msg_received)
        location = msg_json["location"]
        map_grid = msg_json["map"]
        self.android_commander.map_put(map_grid, location)
        msg_received = "{\"map\":\"%s\", \"location\":\"2,1\"}"%loc
        msg_json = json.loads(msg_received)
        location = msg_json["location"]
        map_grid = msg_json["map"]
        self.android_commander.map_put(map_grid, location)
        msg_received = "{\"map\":\"%s\", \"location\":\"3,1\"}"%loc
        msg_json = json.loads(msg_received)
        location = msg_json["location"]
        map_grid = msg_json["map"]
        self.android_commander.map_put(map_grid, location)
        msg_received = "{\"map\":\"%s\", \"location\":\"3,2\"}"%loc
        msg_json = json.loads(msg_received)
        location = msg_json["location"]
        map_grid = msg_json["map"]
        self.android_commander.map_put(map_grid, location)
        msg_received = "{\"map\":\"%s\", \"location\":\"3,3\"}"%loc
        msg_json = json.loads(msg_received)
        location = msg_json["location"]
        map_grid = msg_json["map"]
        self.android_commander.map_put(map_grid, location)


# testing
if __name__=="__main__":
    print "Executing main flow"
    serial_commander = SerialCommanderStub()
    androidT = androidThread("android", serial_commander, mode="auto", production=True)
    androidT.start()