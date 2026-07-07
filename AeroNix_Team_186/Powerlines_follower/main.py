import airsim
import os
import math
import time
import cv2
import numpy as np
from numpy import radians, degrees
from scipy.spatial.transform import Rotation as R

class PowerlineFollower:
    def __init__(self, client, 
                 cameras=["front_center_custom"],  
                 takeoff_altitude=-10,
                 takeoff_speed=2,
                 detection_altitude=-0):
        """
        Initialize PowerlineFollower with the front camera
        """
        self.client = client
        self.cameras = cameras
        self.takeoff_altitude = takeoff_altitude
        self.takeoff_speed = takeoff_speed
        self.detection_altitude = detection_altitude
        
        # Line detection parameters
        self.rho_resolution = 1
        self.theta_resolution = np.pi/180
        self.threshold = 50  
        
        # Debugging
        self.img_counter = 0
        self.debug_mode = True

    def capture_images(self):
        """Capture images from all specified cameras"""
        images = {}
        for camera in self.cameras:
            try:
                png_image = self.client.simGetImage(camera, airsim.ImageType.Scene)
                if png_image is None:
                    print(f"Failed to capture image from {camera}")
                    continue
                image = cv2.imdecode(airsim.string_to_uint8_array(png_image), cv2.IMREAD_UNCHANGED)
                images[camera] = image
            except Exception as e:
                print(f"Error capturing image from {camera}: {e}")
        return images

    def detect_powerline(self, images):
        """
        Detect powerline from multiple camera images
        Returns the best detected line or None
        """
        best_line = None
        best_confidence = 0

        for camera, image in images.items():
            try:
                # Convert to grayscale
                gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                blurred_image = cv2.GaussianBlur(gray_image, (9, 9), 0)
                blurred_image2 = (blurred_image * 255).astype(np.uint8)
                
                # Edge detection
                edges_image = cv2.Canny(blurred_image2, 50, 120)
                
                # Hough Line Transform
                hough_lines = cv2.HoughLines(
                    edges_image, 
                    self.rho_resolution, 
                    self.theta_resolution, 
                    self.threshold
                )
                
                # Debug: save images
                if self.debug_mode:
                    cv2.imwrite(f"debug_edges_{camera}_{self.img_counter}.png", edges_image)
                    self.img_counter += 1

                # Check if lines are detected
                if hough_lines is not None and hough_lines.size > 0:
                    # Use the first line detected
                    line = hough_lines[0][0]
                    
                    # Calculate confidence (number of detected lines)
                    confidence = hough_lines.size
                    
                    # Update best line if this has higher confidence
                    if confidence > best_confidence:
                        best_line = line
                        best_confidence = confidence
                        
                    # Optional: draw lines for debugging
                    if self.debug_mode:
                        self._draw_lines(image, hough_lines, camera)

            except Exception as e:
                print(f"Error detecting powerline in {camera}: {e}")

        return best_line

    def _draw_lines(self, img, houghLines, camera_name, color=[0, 255, 0], thickness=10):
        """Draw detected lines for debugging"""
        rho, theta = houghLines[0][0][0], houghLines[0][0][1]
        a, b = np.cos(theta), np.sin(theta)
        x0, y0 = a * rho, b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        
        cv2.line(img, (x1, y1), (x2, y2), color, thickness)
        cv2.imwrite(f"debug_line_{camera_name}_{self.img_counter}.png", img)

    def follow_powerline(self, speed=2, duration=3):
        """Follow detected powerline"""
        # Capture images from the front camera
        images = self.capture_images()
        
        if not images:
            print("No images captured. Cannot detect powerline.")
            return False

        # Detect powerline
        powerline = self.detect_powerline(images)
        
        if powerline is not None:
            # Convert line to yaw angle
            rho, theta = powerline
            line_angle = degrees(theta)
            
            # Ensure angle is within -180 to 180 degrees
            line_angle = (line_angle + 180) % 360 - 180
            
            print(f"Powerline detected at angle: {line_angle}")
            
            # Calculate velocity components
            # Use sin and cos to convert angle to velocity
            vx = speed * math.cos(math.radians(line_angle))
            vy = speed * math.sin(math.radians(line_angle))
            
            # Get current altitude and position
            current_pose = self.client.simGetObjectPose("Drone1")
            z = current_pose.position.z_val
            
            # Print debug info
            print(f"Calculated velocities - VX: {vx}, VY: {vy}")
            
            # Move drone
            try:
                print("Attempting to move drone...")
                move_future = self.client.moveByVelocityZAsync(
                    vx, vy, z, 
                    duration, 
                    airsim.DrivetrainType.ForwardOnly, 
                    airsim.YawMode(False, 0)
                )
                move_future.join()
                print("Drone movement completed.")
                return True
            except Exception as e:
                print(f"Error moving drone: {e}")
                return False
        else:
            print("No powerline detected. Hovering.")
            return False

    def takeoff_and_position(self):
        """Takeoff and position drone"""
        print("Preparing for takeoff...")
        
        try:
            # Enable API control and arm the drone
            self.client.enableApiControl(True)
            self.client.armDisarm(True)
            
            # Takeoff to initial altitude
            print(f"Taking off to initial altitude: {self.takeoff_altitude}")
            takeoff_future = self.client.takeoffAsync(timeout_sec=10)
            takeoff_future.join()
            
            # Move to detection altitude
            print(f"Moving to detection altitude: {self.detection_altitude}")
            move_future = self.client.moveToPositionAsync(
                0,  # X position 
                0,  # Y position 
                self.detection_altitude,  # Z position (altitude)
                self.takeoff_speed  # Speed
            )
            move_future.join()
            
            # Hover briefly to stabilize
            time.sleep(2)
            print("Drone positioned and ready for powerline detection.")
            return True
        except Exception as e:
            print(f"Error during takeoff and positioning: {e}")
            return False

def main():
    # Connect to the AirSim simulator
    client = airsim.MultirotorClient()
    client.confirmConnection()

    # Initialize powerline follower with front camera
    follower = PowerlineFollower(
        client, 
        cameras=["front_center_custom"],  
        takeoff_altitude=-10,
        detection_altitude=-10,
        takeoff_speed=2
    )

    try:
        # Takeoff and position drone
        if not follower.takeoff_and_position():
            print("Failed to takeoff and position drone.")
            return

        # Main powerline tracking loop
        loop_count = 0
        while loop_count < 10:  # Limit loops to prevent infinite running
            print(f"\nPowerline tracking iteration {loop_count + 1}")
            follower.follow_powerline()
            loop_count += 1
            time.sleep(3)

    except KeyboardInterrupt:
        print("Powerline tracking stopped.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        # Land and disarm
        try:
            client.landAsync().join()
            client.armDisarm(False)
            client.enableApiControl(False)
        except Exception as e:
            print(f"Error during landing: {e}")

if __name__ == "__main__":
    main()
