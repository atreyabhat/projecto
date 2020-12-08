#!/usr/bin/env python
import rospy
#from cmvision.msg import Blobs, Blob
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
from sensor_msgs.msg import CameraInfo

from std_msgs.msg import Int16MultiArray

class MarkerBasics(object):

    def __init__(self):
        self.marker_objectlisher = rospy.Publisher('/ball_marker', Marker, queue_size=1)
        self.rate = rospy.Rate(1)
        self.init_marker(index=0,z_val=0)

    def init_marker(self,index=0, z_val=0):
        self.marker_object = Marker()
        self.marker_object.header.frame_id = "/camera_link"
        self.marker_object.header.stamp    = rospy.get_rostime()
        self.marker_object.ns = "mira"
        self.marker_object.id = index
        self.marker_object.type = Marker.SPHERE
        self.marker_object.action = Marker.ADD

        my_point = Point()
        my_point.z = z_val
        self.marker_object.pose.position = my_point

        self.marker_object.pose.orientation.x = 0
        self.marker_object.pose.orientation.y = 0
        self.marker_object.pose.orientation.z = 0.0
        self.marker_object.pose.orientation.w = 1.0
        self.marker_object.scale.x = 0.05
        self.marker_object.scale.y = 0.05
        self.marker_object.scale.z = 0.05

        self.marker_object.color.r = 1.0
        self.marker_object.color.g = 0.0
        self.marker_object.color.b = 0.0
        # This has to be otherwise it will be transparent
        self.marker_object.color.a = 1.0

        # If we want it for ever, 0, otherwise seconds before desapearing
        self.marker_object.lifetime = rospy.Duration(0)

    def update_position(self,position):        
        self.marker_object.pose.position = position
        self.marker_objectlisher.publish(self.marker_object)


class BallDetector(object):
    def __init__(self):        
        self.rate = rospy.Rate(1)
           
        rospy.Subscriber('/bounding_box', Int16MultiArray, self.ball_detect_callback)        
        self.markerbasics_object = MarkerBasics()


        self.cam_height_y = 440
        self.cam_width_x = 600
        rospy.loginfo("CAMERA INFO:: Image width=="+str(self.cam_width_x)+", Image Height=="+str(self.cam_height_y))

    def ball_detect_callback(self,data):

        redball_point = Point()
        middle_width = float(self.cam_width_x)/2.0 
        middle_height = float(self.cam_height_y)/2.0

        #print(data.data[1])

        redball_point.x = (data.data[1] - middle_width) / float(self.cam_width_x)
        redball_point.z = (data.data[2] - middle_height) / float(self.cam_height_y)                    
        redball_point.y = 0.6            
        rospy.loginfo("blob is at Point="+str(redball_point))
        self.markerbasics_object.update_position(position=redball_point)


    def start_loop(self):
        # spin() simply keeps python from exiting until this node is stopped
        rospy.spin()

if __name__ == '__main__':
    rospy.init_node('redball_detections_listener_node', anonymous=True)
    redball_detector_object = BallDetector()
    redball_detector_object.start_loop()