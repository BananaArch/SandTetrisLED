import constants

import adafruit_lis3dh
import board
import busio
import math

class InputsManager:
    """
    This class is a sub-controller. It helps with managing all inputs for game.py.
    """

    def __init__(self):
        """
        Creates the InputManager object.
        This object is responsible for managing all inputs.
        """

        # --- Initialize hardware ---
        i2c = busio.I2C(board.SCL, board.SDA)  # Setup I2C for the accelerometer
        self.lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=constants.MATRIX_PORTAL_LIS3DH_ADDRESS)  # Creates accelerometer object
        self.lis3dh.range = adafruit_lis3dh.RANGE_2_G  # Sets a range of 2G for sensitivity
        self.lis3dh.set_tap(1, constants.TAP_THRESHOLD) # 1 sets single tap

        # --- Store the previous acceleration values to use to calculate if shaken ---
        self.last_accel_x, self.last_accel_y, self.last_accel_z = self.lis3dh.acceleration

    def get_all_inputs(self):
        """
        Gathers all player inputs from the accelerometer for the current frame.

        Returns:
            dict: A dictionary containing the state of all inputs, e.g.,
                  {'shaken': bool, 'tapped': bool, 'tilt_angle': float}
        """
        was_tapped = False # Default value
        was_shaken = False # Default value

        try:
            # Get the current raw acceleration values
            ax, ay, az = self.lis3dh.acceleration

            # Calculate the change (delta) in acceleration since the last frame
            delta_x = ax - self.last_accel_x
            delta_y = ay - self.last_accel_y
            delta_z = az - self.last_accel_z

            # Update the stored values for the next frame
            self.last_accel_x, self.last_accel_y, self.last_accel_z = ax, ay, az

            # Calculate the magnitude of the change. This is the "jerk".
            jerk_magnitude = math.sqrt(delta_x**2 + delta_y**2 + delta_z**2)

            if jerk_magnitude > constants.SHAKE_THRESHOLD:
                was_shaken = True

            # --- Tap Detection ---
            was_tapped = self.lis3dh.tapped

            # --- Tilt Angle ---
            angle_rad = math.atan2(-ay, ax)
            angle_deg = math.degrees(angle_rad)

        except OSError:
            # If I2C fails, return neutral inputs
            return {"shaken": False, "tapped": False, "tilt_angle": 0.0}

        # Return all inputs in a clean dictionary
        return {
            "shaken": was_shaken,
            "tapped": was_tapped,
            "tilt_angle": angle_deg
        }
