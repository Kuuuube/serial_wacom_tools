from pywinusb import hid
from internal_constants import *
from user_constants import *
import tablet_monitor_mapping

report = [0x00]*65

def send_vmulti_report_wacom_ii_s(vmulti_device_report, proximity, pointer, pos_x, pos_y, buttons, button_flag, pressure):
    pressure = pressure + PRESSURE_OFFSET
    if pressure <= PRESSURE_DEADZONE or pressure < 0:
        pressure = 0

    report[0] = VMULTI_ID
    report[1] = USAGE_PAGE_DIGITIZER
    report[2] = OUTPUT_MODE

    flags = 0
    if (pointer or button_flag):
        if (bool((buttons & 0x01))): # pen tip
            flags = flags | int(0x01) # pen tip

        if (pressure > 1): # pen tip
            flags = flags | int(0x01) # pen tip
    else:
        # mouse buttons are not implemented
        pass
    
    if (proximity):
        flags = flags | int(0x10)

    report[3] = flags

    scaled_pos_x = tablet_monitor_mapping.map_x(pos_x)
    report[4] = scaled_pos_x & 0x00FF
    report[5] = (scaled_pos_x & 0xFF00) >> 8

    scaled_pos_y = tablet_monitor_mapping.map_y(pos_y)
    report[6] = scaled_pos_y & 0x00FF
    report[7] = (scaled_pos_y & 0xFF00) >> 8

    scaled_pressure = int(pressure / WACOM_II_S_MAX_PRESSURE * 8191)
    report[8] = scaled_pressure & 0x00FF
    report[9] = (scaled_pressure & 0xFF00) >> 8

    vmulti_device_report.set_raw_data(report)
    vmulti_device_report.send()