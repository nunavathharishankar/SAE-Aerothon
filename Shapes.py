import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import numpy as np

# Initialize the ROS node
rospy.init_node('shape_detector')

# Initialize the OpenCV bridge
bridge = CvBridge()

# Initialize the video capture device
cap = cv2.VideoCapture(0)

# Define the minimum and maximum area of the contour to be detected
min_area = 1000
max_area = 5000

# Define the minimum and maximum number of sides of the contour to be detected
min_sides = 3
max_sides = 5

# Define the color of the contour to be drawn
color = (0, 255, 0)

# Define the thickness of the contour to be drawn
thickness = 2

# Define the font of the text to be displayed
font = cv2.FONT_HERSHEY_SIMPLEX

# Define the size of the text to be displayed
font_scale = 1

# Define the thickness of the text to be displayed
font_thickness = 2

# Define the position of the text to be displayed
text_position = (20, 40)

# Define the text to be displayed
text = ""

# Define the ROS publisher for the detected image
image_pub = rospy.Publisher('/camera/image_raw', Image, queue_size=1)

while not rospy.is_shutdown():
    # Capture a frame from the video stream
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply a threshold to the grayscale image
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Find the contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through the contours
    for contour in contours:
        # Compute the area and perimeter of the contour
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)

        # Compute the number of sides of the contour
        approx = cv2.approxPolyDP(contour, 0.03 * perimeter, True)
        sides = len(approx)

        # Check if the contour meets the criteria for a triangle
        if min_area < area < max_area and min_sides <= sides <= max_sides:
            # Draw the contour on the frame
            cv2.drawContours(frame, [approx], 0, color, thickness)

            # Update the text to be displayed
            text = "Triangle"

    # Draw the text on the frame
    cv2.putText(frame, text, text_position, font, font_scale, color, font_thickness)

    # Convert the frame back to a ROS image message
    image_msg = bridge.cv2_to_imgmsg(frame, encoding="bgr8")

    # Publish the image message
    image_pub.publish(image_msg)

    # Show the frame
    cv2.imshow('frame', frame)

    # Wait for a key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture device
cap.release()

# Destroy all OpenCV windows
cv2.destroyAllWindows()
