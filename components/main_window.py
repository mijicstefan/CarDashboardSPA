from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QPushButton, QProgressBar, QSlider, QLCDNumber, QVBoxLayout, QLabel
import sys
import time
from PySide2.QtCore import *
from PySide2.QtGui import *
import threading
import random
from sll.sll import SinglyLinkedList
import json
from datetime import datetime


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.speed_logs_databse = []

        # Based on this value engine will run or wil stop running.
        self.engine_run_condition = False

        # Braking functionality get activated based on this variable.
        self.brake_run_condition = False

        # GEAR INDICATOR
        self.gear_indicator = QLabel('CURRENT GEAR INDICATOR')

        # SLIDER
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMaximum(100)
        self.slider.setMinimum(0)

        # LCD NUMBER FOR KMPH
        self.lcd_speed = QLCDNumber(self)
        self.lcd_speed.setStyleSheet("width:300")
        self.lcd_speed.rect().center()

        # LCD INDICATOR FOR CURRENT GEAR
        self.lcd_gear = QLCDNumber(self)

        # START ENGINE BUTTON
        self.start_engine = QPushButton('Start Engine')
        self.start_engine.clicked.connect(self.engine_thread)

        # TURN OFF ENGINE BUTTON
        self.turn_off_engine = QPushButton('Turn Off Engine')
        self.turn_off_engine.clicked.connect(self.turn_off_engine_thread)

        # PRESS BRAKE
        self.brake_pedal = QPushButton('Use Brakes To Slow Down')
        self.brake_pedal.clicked.connect(self.brakes_thread)

        # MAIN APP LAYOUT
        self.appLayout = QVBoxLayout(self)

        # ROW2
        self.row2 = QHBoxLayout(self)
        self.row2.addWidget(self.lcd_speed)
        self.row2.addWidget(self.lcd_gear)

        # ROW3
        self.row3 = QHBoxLayout(self)
        self.row3.addWidget(self.start_engine)
        self.row3.addWidget(self.turn_off_engine)

        # ROW4
        self.row4 = QVBoxLayout(self)
        self.row4.addWidget(self.slider)

        # ROW5
        self.row5 = QVBoxLayout(self)
        self.row5.addWidget(self.gear_indicator)

        # ROW6
        self.row6 = QVBoxLayout(self)
        self.row6.addWidget(self.brake_pedal)

        # APPENDING ROWS TO MAIN APP LAYOUT
        self.appLayout.addLayout(self.row2)
        self.appLayout.addLayout(self.row3)
        self.appLayout.addLayout(self.row4)
        self.appLayout.addLayout(self.row5)
        self.appLayout.addLayout(self.row6)

        # Main Window METADATA
        self.setWindowTitle("Car Dashboard")
        self.setGeometry(300, 300, 600, 800)
        self.setMinimumHeight(600)
        self.setMinimumWidth(800)
        self.setMaximumHeight(600)
        self.setMaximumWidth(800)

        # SETTING MAIN LAYOUT FOR APP
        self.setLayout(self.appLayout)

    # Engine thread which will be responsible for updating GUI values based on engine functionality.
    def engine_thread(self):
        thread = threading.Thread(target=self.engine_logic)
        thread.start()

    # MAIN PHYSICS AND ENGINE LOGIC
    def engine_logic(self):
        self.engine_run_condition = True
        start_time = time.time()
        while self.engine_run_condition:
            time.sleep(0.001)
            gas_pedal = self.slider.value()
            if gas_pedal == 0:
                start_time = time.time()
            self.gear_logic(start_time)

    # Shifting gears based on velocity treshold limit.
    def gear_logic(self, start_time):
        shifting_gears = [
            {"gear": "1", "next_gear": "2", "prev_gear": "Car has stopped."},
            {"gear": "2", "next_gear": "3", "prev_gear": "1"},
            {"gear": "3", "next_gear": "4", "prev_gear": "2"},
            {"gear": "4", "next_gear": "5", "prev_gear": "4"},
            {"gear": "5", "next_gear": "6", "prev_gear": "4"},
            {"gear": "6", "next_gear": "Gear limit", "prev_gear": "5"}
        ]

        # Logging al velocity changes while car is moving.
        data_logs = SinglyLinkedList()

        # Max acceleration rate based on BMW X6, 7 m/s^2.
        max_acceleration_rate = 7

        # Throttle percentage, it simulates how hard the gas pedal has being pressed.
        throttle_percentage = self.slider.value()

        # Based on percetage which represents how hard the pedal has being pressed
        current_acceleration = (throttle_percentage /
                                100) * max_acceleration_rate
        # For acceleration we must use start time and end time.
        end_time = time.time()
        final_time = end_time - start_time
        # average speed is: a * t
        current_speed = current_acceleration * final_time
        # current speed is average speed + speed at the moment with that acceleration.
        real_speed = current_speed + current_acceleration * final_time

        self.global_real_speed = real_speed

        # MAX SPEED LIMIT
        if real_speed > 320:
            real_speed = 320

        # AUTO-SWITCHING GEAR SYSTEM
        #!IF THE CURRENT SPEED IS 0, TELL THE DRIVER THAT CAR IS NOT MOVING.
        if real_speed == 0:
            self.gear_indicator.setText('Current gear is: Car is not moving.')
            data_logs.append({"gear": 0, "speeed": real_speed})
        #!IF THE CURRENT SPEED IS IN RANGE(1, 45), SHOW ACTIVE GEAR(1).
        elif 0 < real_speed <= 45:
            self.gear_indicator.setText(
                'Current gear is: {}'.format(shifting_gears[0]['gear']))
            self.lcd_gear.display(shifting_gears[0]['gear'])
            data_logs.append({"gear": 1, "speeed": real_speed})
        #!IF THE CURRENT SPEED IS IN RANGE(46, 75), SHOW ACTIVE GEAR(2).
        elif 45 < real_speed <= 75:
            self.gear_indicator.setText(
                'Current gear is: {}'.format(shifting_gears[1]['gear']))
            self.lcd_gear.display(shifting_gears[1]['gear'])
            data_logs.append({"gear": 2, "speeed": real_speed})
        #!IF THE CURRENT SPEED IS IN RANGE(76, 110), SHOW ACTIVE GEAR(3).
        elif 75 < real_speed <= 110:
            self.gear_indicator.setText(
                'Current gear is: {}'.format(shifting_gears[2]['gear']))
            self.lcd_gear.display(shifting_gears[2]['gear'])
            data_logs.append({"gear": 3, "speeed": real_speed})
        #!IF THE CURRENT SPEED IS IN RANGE(111, 150), SHOW ACTIVE GEAR(4).
        elif 110 < real_speed <= 150:
            self.gear_indicator.setText(
                'Current gear is: {}'.format(shifting_gears[3]['gear']))
            self.lcd_gear.display(shifting_gears[3]['gear'])
            data_logs.append({"gear": 4, "speeed": real_speed})
        #!IF THE CURRENT SPEED IS IN RANGE(151, 260), SHOW ACTIVE GEAR(5).
        elif 150 < real_speed <= 260:
            self.gear_indicator.setText(
                'Current gear is: {}'.format(shifting_gears[4]['gear']))
            self.lcd_gear.display(shifting_gears[4]['gear'])
            data_logs.append({"gear": 5, "speeed": real_speed})
        #!IF THE CURRENT SPEED IS IN RANGE(261, 320), SHOW ACTIVE GEAR(6).
        elif 260 < real_speed <= 320:
            self.gear_indicator.setText(
                'Current gear is: {}'.format(shifting_gears[5]['gear']))
            self.lcd_gear.display(shifting_gears[5]['gear'])
            data_logs.append({"gear": 6, "speeed": real_speed})
        print('Current speed is: {}'.format(real_speed))

        # Update kmph number in GUI
        self.lcd_speed.display(int(real_speed))

        # Handle log data
        for data_log in data_logs:
            self.speed_logs_databse.append(data_log)

    # Brake thread is responsible for braking when Brake action is called.
    def brakes_thread(self):
        brake_thread = threading.Thread(target=self.use_brakes)
        brake_thread.start()

    def use_brakes(self):
        self.brake_run_condition = True
        while self.brake_run_condition:
            print("Brake pedal is being pressed.")
            current_slider_value = self.slider.value()
            for i in range(current_slider_value, -1, -1):
                # based on this formula:
                """Conditions: Good tyres and good brakes.
                    Formula: d = s2 / (250 * f)

                    d = braking distance in metres (to be calculated).
                    s = speed in km/h.
                    250 = fixed figure which is always used.
                    f = coefficient of friction, approx. 0.8 on dry asphalt and 0.1 on ice.

                    Example of calculation with a speed of 50 km/h on dry asphalt:

                    50^2 / (250 * 0.8) = 12.5 metres braking distance
                """
                # breaking time at average speed of 100 kmph
                time.sleep(0.025)
                self.slider.setValue(i)
            self.turn_off_brake_thread()

    # When engines gets turned off, end the engine - thread process.

    def turn_off_engine_thread(self):
        self.engine_run_condition = False
        with open('./speed_system_logs/datalogs.txt', 'w') as f:
            json.dump(self.speed_logs_databse, f)

    # When current velocity reaches 0, end the break - thread process.
    def turn_off_brake_thread(self):
        self.brake_run_condition = False
