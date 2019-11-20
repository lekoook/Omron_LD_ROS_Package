#!/usr/bin/env python
import sys
import rospy
from om_aiv_util.srv import *
def queueCancelLocal_client(a, b , c, d):
    rospy.wait_for_service('queueCancelLocal')
    try:
        service = rospy.ServiceProxy('queueCancelLocal', Service4)
        resp1 = service(a, b, c, d)
        return resp1.device
    except rospy.ServiceException, error:
        print "Service call failed: %s"%error

def usage():
    return "%s <type> <value> [echoString] [reason]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 5:
        a = str(sys.argv[1])
        b = str(sys.argv[2])
        c = str(sys.argv[3])
        d = str(sys.argv[4])
    elif len(sys.argv) == 3:
        a = str(sys.argv[1])
        b = str(sys.argv[2])
        c = ""
        d = ""
    elif len(sys.argv) == 2:
        a = str(sys.argv[1])
        b = ""
        c = ""
        d = ""

    else:
        print usage()
        sys.exit(1)
    print "running command"
    print queueCancelLocal_client(a, b , c, d)
