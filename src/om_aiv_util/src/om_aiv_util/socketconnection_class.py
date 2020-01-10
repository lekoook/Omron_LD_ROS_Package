#!/usr/bin/env python
import socket
import rospy

PARAM_IP_ADDR = str(rospy.get_param("ip_address"))
PARAM_PORT = int(rospy.get_param("port"))
DEFAULT_PASSWD = str(rospy.get_param("def_arcl_passwd"))
DEFAULT_SOCKET_TIMEOUT = 10
RECV_BUFFER = 2048
MAX_CONN_RETRY = 5  
CONN_RETRY_SLP = 2

# Feedback strings that is sent by ARCL server. We use them to identify the response of the ARCL server.
PASSWD_PROMPT_STRING = "Enter password:"
WELCOME_STRING = "Welcome to the server."
END_OF_CMDS_STRING = "End of commands"
MAX_TRIES_ERROR = "Maximum number of connection retries reached. Are you sure you are connected? Is the password correct?"

# Driver class to connect a socket to the ARCL server.
class ConnectSocket(object):

    def __init__(self, sock=None, passwd=None):
        # Assign all instance attributes
        if passwd is None:
            # \r\n needs to be appended to all strings sent to the socket in order for ARCL to terminate their read.
            self.passwd = (''.join([DEFAULT_PASSWD, "\r\n"])).encode('ascii')
        else:
            self.passwd = (''.join([passwd, "\r\n"])).encode('ascii')

        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(DEFAULT_SOCKET_TIMEOUT)
            retries = 0
            while retries < MAX_CONN_RETRY:
                try:
                    self.make_connection()
                except socket.error as err:
                    retries = retries + 1
                    rospy.logerr("Socket make connection failed: %s", err)
                    rospy.sleep(CONN_RETRY_SLP)
                else:
                    break
            if retries == MAX_CONN_RETRY:
                raise RuntimeError(MAX_TRIES_ERROR)
        else:
            self.sock = sock

    # Attempts to make the socket connection and login into ARCL server with the given password.
    def make_connection(self):
        self.sock.connect((PARAM_IP_ADDR, PARAM_PORT))
        self.login()

    # Attempts to login into ARCL server.
    # NOTE: This is a blocking function if password prompt or login strings are not received from socket.
    def login(self):
        # Look for the login message from ARCL.
        while True:
            try:
                ret = self.sock.recv(RECV_BUFFER)
            except socket.error as err:
                raise err
            else:
                if PASSWD_PROMPT_STRING in ret:
                    break
        
        self.sock.send(self.passwd)

        # Check for login success.
        while True:
            try:
                ret = self.sock.recv(RECV_BUFFER)
            except socket.error as err:
                raise err
            else:
                if END_OF_CMDS_STRING in ret:
                    rospy.loginfo("Login to %s", PARAM_IP_ADDR)
                    rospy.loginfo("using the socket ID %s", str(id(self)))
                    break
