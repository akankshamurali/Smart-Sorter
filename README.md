Smart Sorter is a real-time object classification system that utilizes computer vision to sort items based on their shape and color. The system integrates a Raspberry Pi for image processing and an Arduino for hardware control, enabling automated sorting through motorized mechanisms.

Project Overview
Computer Vision: Employs OpenCV on Raspberry Pi to detect and classify objects by shape and color.
Hardware Control: Uses Arduino to manage motors and actuators for physical sorting.
Communication: Raspberry Pi and Arduino communicate via serial interface to coordinate actions.

System Architecture
Image Acquisition: Raspberry Pi captures images of objects using a connected camera.
Processing: OpenCV processes the images to identify object features.
Classification: Objects are classified based on predefined shape and color parameters.
Sorting: Classification results are sent to Arduino, which actuates motors to sort objects accordingly.

Hardware Requirements
Raspberry Pi (with camera module), Arduino Uno, Servo motors, Power supply
Assorted objects for sorting (varying in shape and color)

Software Requirements
Python 3.x, OpenCV library, PySerial for serial communication, Arduino IDE
