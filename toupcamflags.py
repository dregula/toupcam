# toupcam_flags
# toupcam.h Version: 33.13977.2019.0224

from enum import Enum

class ToupCamFlags(Enum):
    CMOS = 0x00000001  # cmos sensor
    CCD_PROGRESSIVE = 0x00000002  # progressive ccd sensor
    CCD_INTERLACED = 0x00000004  # interlaced ccd sensor
    ROI_HARDWARE = 0x00000008  # support hardware ROI
    MONO = 0x00000010  # monochromatic
    BINSKIP_SUPPORTED = 0x00000020  # support bin/skip mode, see Toupcam_put_Mode and Toupcam_get_Mode
    USB30 = 0x00000040  # usb3.0
    TEC = 0x00000080  # Thermoelectric Cooler
    USB30_OVER_USB20 = 0x00000100  # usb3.0 camera connected to usb2.0 port
    ST4 = 0x00000200  # ST4 port
    GETTEMPERATURE = 0x00000400  # support to get the temperature of the sensor
    PUTTEMPERATURE = 0x00000800  # support to put the target temperature of the sensor
    RAW10 = 0x00001000  # pixel format, RAW 10bits
    RAW12 = 0x00002000  # pixel format, RAW 12bits
    RAW14 = 0x00004000  # pixel format, RAW 14bits
    RAW16 = 0x00008000  # pixel format, RAW 16bits
    FAN = 0x00010000  # cooling fan
    TEC_ONOFF = 0x00020000  # Thermoelectric Cooler can be turn on or off, support to set the target temperature of TEC
    ISP = 0x00040000  # ISP (Image Signal Processing) chip
    TRIGGER_SOFTWARE = 0x00080000  # support software trigger
    TRIGGER_EXTERNAL = 0x00100000  # support external trigger
    TRIGGER_SINGLE = 0x00200000  # only support trigger single: one trigger, one image
    BLACKLEVEL = 0x00400000  # support set and get the black level
    AUTO_FOCUS = 0x00800000  # support auto focus
    BUFFER = 0x01000000  # frame buffer
    DDR = 0x02000000  # use very large capacity DDR (Double Data Rate SDRAM) for frame buffer
    CG = 0x04000000  # Conversion Gain: HCG, LCG
    YUV411 = 0x08000000  # pixel format, yuv411
    VUYY = 0x10000000  # pixel format, yuv422, VUYY
    YUV444 = 0x20000000  # pixel format, yuv444
    RGB888 = 0x40000000  # pixel format, RGB888
    RAW8 = 0x80000000  # pixel format, RAW 8 bits
    GMCY8 = 0x0000000100000000  # pixel format, GMCY, 8bits
    GMCY12 = 0x0000000200000000  # pixel format, GMCY, 12bits
    UYVY = 0x0000000400000000  # pixel format, yuv422, UYVY
    CGHDR = 0x0000000800000000  # Conversion Gain: HCG, LCG, HDR
    GLOBALSHUTTER = 0x0000001000000000  # global shutter


# class Flags:
#     flags = None
#     flag_names = []
#
#     def __init__(self, flags=None):
#         self.flags = flags
#
#     def __repr__(self):
#         return self.flag_names


def getAllFlags(flags=None):
    flag_names = []
    for name, member in ToupCamFlags.__members__.items():
        if (flags & member.value):
            flag_names.append(name)
    return flag_names


""" currently unused """
class ToupCamConstants(Enum):
    TEMP_DEF = 6503  # temp
    TEMP_MIN = 2000  # temp
    TEMP_MAX = 15000  # temp
    TINT_DEF = 1000  # tint
    TINT_MIN = 200  # tint
    TINT_MAX = 2500  # tint
    HUE_DEF = 0  # hue
    HUE_MIN = (-180)  # hue
    HUE_MAX = 180  # hue
    SATURATION_DEF = 128  # saturation
    SATURATION_MIN = 0  # saturation
    SATURATION_MAX = 255  # saturation
    BRIGHTNESS_DEF = 0  # brightness
    BRIGHTNESS_MIN = (-64)  # brightness
    BRIGHTNESS_MAX = 64  # brightness
    CONTRAST_DEF = 0  # contrast
    CONTRAST_MIN = (-100)  # contrast
    CONTRAST_MAX = 100  # contrast
    GAMMA_DEF = 100  # gamma
    GAMMA_MIN = 20  # gamma
    GAMMA_MAX = 180  # gamma
    AETARGET_DEF = 120  # target of auto exposure
    AETARGET_MIN = 16  # target of auto exposure
    AETARGET_MAX = 220  # target of auto exposure
    WBGAIN_DEF = 0  # white balance gain
    WBGAIN_MIN = (-127)  # white balance gain
    WBGAIN_MAX = 127  # white balance gain
    BLACKLEVEL_MIN = 0  # minimum black level
    BLACKLEVEL8_MAX = 31  # maximum black level for bit depth = 8
    BLACKLEVEL10_MAX = (31 * 4)  # maximum black level for bit depth = 10
    BLACKLEVEL12_MAX = (31 * 16)  # maximum black level for bit depth = 12
    BLACKLEVEL14_MAX = (31 * 64)  # maximum black level for bit depth = 14
    BLACKLEVEL16_MAX = (31 * 256)  # maximum black level for bit depth = 16
    SHARPENING_STRENGTH_DEF = 0  # sharpening strength
    SHARPENING_STRENGTH_MIN = 0  # sharpening strength
    SHARPENING_STRENGTH_MAX = 500  # sharpening strength
    SHARPENING_RADIUS_DEF = 2  # sharpening radius
    SHARPENING_RADIUS_MIN = 1  # sharpening radius
    SHARPENING_RADIUS_MAX = 10  # sharpening radius
    SHARPENING_THRESHOLD_DEF = 0  # sharpening threshold
    SHARPENING_THRESHOLD_MIN = 0  # sharpening threshold
    SHARPENING_THRESHOLD_MAX = 255  # sharpening threshold


if __name__ == '__main__':
    flags = Flags()
    flags.getAllFlags(2164532329)   # an example flags from my oen camera...
    print(flags.flag_names)
    exit()

