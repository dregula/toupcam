# ===============================================================================
# Copyright 2021 Donald Regula
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

# ============= standard library imports ========================
import ctypes

# ============= local library imports  ==========================
from core import lib
import toupcamflags

TOUPCAM_MAX = 16  # toupcam.h Version: 33.13977.2019.0224


class HToupcamResolution(ctypes.Structure):
    # _pack_ = 8
    _fields_ = [
        ("width", ctypes.c_uint),
        ("height", ctypes.c_uint)
    ]

    def __init__(self, width=0, height=0):
        super(HToupcamResolution, self).__init__(width, height)


""" ToupcamModelV2 Structure
    Some basic attributes about a single camera
    from toupcam.h Version: 33.13977.2019.0224
typedef struct {
    const wchar_t*      name;        /* model name, in Windows, we use unicode */
    unsigned long long  flag;        /* TOUPCAM_FLAG_xxx, 64 bits */
    unsigned            maxspeed;    /* number of speed level, same as Toupcam_get_MaxSpeed(), the speed range = [0, maxspeed], closed interval */
    unsigned            preview;     /* number of preview resolution, same as Toupcam_get_ResolutionNumber() */
    unsigned            still;       /* number of still resolution, same as Toupcam_get_StillResolutionNumber() */
    unsigned            maxfanspeed; /* maximum fan speed */
    unsigned            ioctrol;     /* number of input/output control */
    float               xpixsz;      /* physical pixel size */
    float               ypixsz;      /* physical pixel size */
    ToupcamResolution   res[TOUPCAM_MAX];
}ToupcamModelV2; /* camera model v2 */
"""
class HToupcamModelV2(ctypes.Structure):
    _pack_ = 8
    _fields_ = [
        ("name", ctypes.c_wchar_p),  # model name
        ("flag", ctypes.c_longlong),  # TOUPCAM_FLAG_xxx
        ("maxspeed", ctypes.c_uint),
        # number of speed level, Toupcam_get_MaxSpeed, the speed range = [0, max], closed interval
        ("preview", ctypes.c_uint),  # number of preview resolution, Toupcam_get_ResolutionNumber
        ("still", ctypes.c_uint),  # number of still resolution, Toupcam_get_StillResolutionNumber
        ("maxfanspeed", ctypes.c_uint),  # maximum fan speed
        ("ioctrol", ctypes.c_uint),  # number of input/output control
        ("xpixsz", ctypes.c_float),  # physical pixel size
        ("ypixsz", ctypes.c_float),  # physical pixel size
        ("toupcamResolution", (HToupcamResolution * TOUPCAM_MAX))
        # TODO: refactor from overly-complicated HToupcamResolution to either a "plain" two-integer tuple or an cv.Size
    ]

    # https://stackoverflow.com/questions/7946519/default-values-in-a-ctypes-structure/25892189
    def __init__(self,
                 name=ctypes.cast(ctypes.create_unicode_buffer('empty', TOUPCAM_MAX), ctypes.c_wchar_p),
                 flags=0,
                 maxspeed=1,
                 preview=2,
                 still=3,
                 maxfanspeed=0,
                 ioctrl=0,
                 xpixsz=0,
                 ypixsz=0,
                 toupcamResolution=(HToupcamResolution * TOUPCAM_MAX)()
                 ):
        super(HToupcamModelV2, self).__init__(name, flags, maxspeed, preview, still, maxfanspeed, ioctrl, xpixsz,
                                              ypixsz, toupcamResolution)


""" ToupcamInstV2 Structure
    An V2 wrapper around an individual ToupCamModel structure
    ToupcamInstV2:displayname appears to be the same as ToupcamModelV2:name
typedef struct {
    wchar_t               displayname[64];    /* display name */
    wchar_t               id[64];             /* unique and opaque [string] id of a connected camera, for Toupcam_Open */
                                              /* NOT the same as the integer camera index [cid] */
    const ToupcamModelV2* model;
}ToupcamInstV2; /* camera instance for enumerating */


    note: the single native call using this structure is lib.Toupcam_EnumV2
            you pass an array (pointer) of HToupcamInstV2
"""
class HToupcamInstV2(ctypes.Structure):
    _pack_ = 8
    _fields_ = [
        ("displayname", ctypes.c_wchar * 64),
        ("id", ctypes.c_wchar * 64),
        ("model", ctypes.POINTER(HToupcamModelV2))
    ]

    def __init__(self, displayname='', id='', model=(HToupcamModelV2 * TOUPCAM_MAX)()):
        super(HToupcamInstV2, self).__init__(displayname, id, model)
        pass


class CameraProperties(object):
    _cam = None
    cid = -1
    displayname = ''
    id = ''
    name = ''
    _flags = 0
    flagnames = ''
    maxspeed = 0
    preview = 0
    still = 0
    maxfanspeed = 0
    ioctrol = 0
    xpixsz = 0
    ypixsz = 0
    _resolutions = []
    resolutions = []

    def __init__(self, object):
        _cam = object
        # print(f"type(object):{type(object)}.")
        # print(f"HToupcamModelV2:{HToupcamModelV2}.")
        if type(object) != HToupcamModelV2:
            try:
                _cam = ctypes.cast(object, HToupcamModelV2)
            except:
                raise TypeError(
                    f"Class CameraProperties: expect type HToupcamModelV2 as initial argument, got type:{type(object)}!")
        self.name = _cam.name
        self._flags = _cam.flag
        self.flagnames = toupcamflags.getAllFlags(_cam.flag)
        self.maxspeed = _cam.maxspeed
        self.preview = _cam.preview
        self.still = _cam.still
        self.maxfanspeed = _cam.maxfanspeed
        self.ioctorl = _cam.ioctrol
        self.xpixsz = _cam.xpixsz
        self.ypixsz = _cam.ypixsz
        self._resolutions = _cam.toupcamResolution
        for k in range(0,int(_cam.still)):
            self.resolutions.append((self._resolutions[k].width, self._resolutions[k].height))
        pass


    def __repr__(self):
        return f'CameraProperties(' \
               f'cid={self.cid}, ' \
               f'displayname={self.displayname}, ' \
               f'id={self.id}, ' \
               f'name={self.name}, ' \
               f'_flags={self._flags}, ' \
               f'flagnames={self.flagnames}, ' \
               f'maxspeed={self.maxspeed}, ' \
               f'preview={self.preview}, ' \
               f'still={self.still}, ' \
               f'maxfanspeed={self.maxfanspeed}, ' \
               f'ioctrol={self.ioctrol}, ' \
               f'xpixsz={self.xpixsz}, ' \
               f'ypixsz={self.ypixsz}, ' \
               f'resolutions={self.resolutions}' \
               f')'


class EnumCameras(object):
    num_cams = -1
    arrCameraProperties = []


    def __init__(self):
        """ Toupcam_EnumV2
            enumerate the cameras connected to the computer, return the number of enumerated.

            ToupcamInstV2 arr[TOUPCAM_MAX];
            unsigned cnt = Toupcam_EnumV2(arr);
            for (unsigned i = 0; i < cnt; ++i)

            if pti == NULL, then, only the number is returned.
            Toupcam_Enum is obsolete.
        """
        func_cam_enum = lib.Toupcam_EnumV2
        func_cam_enum.argtypes = [ctypes.POINTER(HToupcamInstV2)]
        func_cam_enum.restype = ctypes.c_int

        # arbitrary initial buffer
        arr_toupcaminst = (HToupcamInstV2 * TOUPCAM_MAX)()

        num_cams = func_cam_enum(arr_toupcaminst)

        if num_cams < 0:
            raise ValueError(f"Toupcam_Enum returned {num_cams} num_cams, expect greater than zero!")

        try:
            # try again with a num_cams - sized array of HToupcamInstV2
            arr_toupcaminst = (HToupcamInstV2 * num_cams)()
            num_cams = func_cam_enum(arr_toupcaminst)
        except:
            raise ValueError(f"Toupcam_Enum failed with {num_cams} num_cams!")
        if num_cams < 0:
            # we've now failed twice...
            raise ValueError(
                f"Toupcam_Enum returned {num_cams} num_cams, expect greater than zero!")


        for i in range(0, num_cams):
            tuopcaminst = arr_toupcaminst[i]
            # dereference to internal HToupcamModelV2 struct
            cam_prop = CameraProperties(ctypes.cast(tuopcaminst.model, ctypes.POINTER(HToupcamModelV2)).contents)
            # this is an index unique to this company's cameras and is unrelated to the cid returned in native opencv
            cam_prop.cid = i
            cam_prop.displayname = tuopcaminst.displayname
            cam_prop.id = tuopcaminst.id

            self.arrCameraProperties.append(cam_prop)


if __name__ == '__main__':
    import time

    cam_enum = EnumCameras()
    for camprops in cam_enum.arrCameraProperties:
        print(f"Cam#{camprops.cid}: {str(camprops)}")

    exit()
# ============= EOF =============================================
