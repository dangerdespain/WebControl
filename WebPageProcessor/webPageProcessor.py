from __main__ import socketio

import time
import math
import json
from os import listdir
from os.path import isfile, join
from flask import render_template
import os

class WebPageProcessor:

    data = None

    def __init__(self, data):
        self.data = data

    def createWebPage(self, pageID, isMobile, args):
        # returns a page and a bool specifying whether the user has to click close to exit modal
        if pageID == "maslowSettings":
            setValues = self.data.config.getJSONSettingSection("Maslow Settings")
            # because this page allows you to select the comport from a list that is not stored in webcontrol.json, we need to package and send the list of comports
            # Todo:? change it to store the list?
            ports = self.data.comPorts
            if isMobile:
                page = render_template(
                    "settings_mobile.html",
                    title="Maslow Settings",
                    settings=setValues,
                    ports=ports,
                    pageID="maslowSettings",
                )
            else:
                page = render_template(
                    "settings.html",
                    title="Maslow Settings",
                    settings=setValues,
                    ports=ports,
                    pageID="maslowSettings",
                )
            return page, "Maslow Settings", False, "medium", "content"
        elif pageID == "advancedSettings":
            setValues = self.data.config.getJSONSettingSection("Advanced Settings")
            if isMobile:
                page = render_template(
                    "settings_mobile.html",
                    title="Advanced Settings",
                    settings=setValues,
                    pageID="advancedSettings",
                )
            else:
                page = render_template(
                    "settings.html",
                    title="Advanced Settings",
                    settings=setValues,
                    pageID="advancedSettings",
                )
            return page, "Advanced Settings", False, "medium", "content"
        elif pageID == "webControlSettings":
            setValues = self.data.config.getJSONSettingSection("WebControl Settings")
            if isMobile:
                page = render_template(
                    "settings_mobile.html",
                    title="WebControl Settings",
                    settings=setValues,
                    pageID="webControlSettings",
                )
            else:
                page = render_template(
                    "settings.html",
                    title="WebControl Settings",
                    settings=setValues,
                    pageID="webControlSettings",
                )
            return page, "WebControl Settings", False, "medium", "content"
        elif pageID == "openGCode":
            lastSelectedFile = self.data.config.getValue("Maslow Settings", "openFile")
            lastSelectedDirectory = self.data.config.getValue("Computed Settings", "lastSelectedDirectory")
            home = self.data.config.getHome()
            homedir = home+"/.WebControl/gcode"
            directories = []
            files = []
            try:
                for _root, _dirs, _files in os.walk(homedir):
                    if _dirs:
                        directories = _dirs
                    for file in _files:
                        if _root != homedir:
                            _dir = _root.split("\\")[-1].split("/")[-1]
                        else:
                            _dir = "."
                        files.append({"directory":_dir, "file":file})
            except Exception as e:
                print(e)
           # files = [f for f in listdir(homedir) if isfile(join(homedir, f))]
            directories.insert(0, "./")
            if lastSelectedDirectory is None:
                lastSelectedDirectory="."
            page = render_template(
                "openGCode.html", directories=directories, files=files, lastSelectedFile=lastSelectedFile, lastSelectedDirectory=lastSelectedDirectory
            )
            return page, "Open GCode", False, "medium", "content"
        elif pageID == "uploadGCode":
            validExtensions = self.data.config.getValue(
                "WebControl Settings", "validExtensions"
            )
            lastSelectedDirectory = self.data.config.getValue("Computed Settings", "lastSelectedDirectory")
            home = self.data.config.getHome()
            homedir = home + "/.WebControl/gcode"
            directories = []
            try:
                for _root, _dirs, _files in os.walk(homedir):
                    if _dirs:
                        directories = _dirs
            except Exception as e:
                print(e)
            directories.insert(0, "./")
            if lastSelectedDirectory is None:
                lastSelectedDirectory = "."
            page = render_template("uploadGCode.html", validExtensions=validExtensions, directories=directories, lastSelectedDirectory=lastSelectedDirectory)
            return page, "Upload GCode", False, "medium", "content"
        elif pageID == "importGCini":
            page = render_template("importFile.html")
            return page, "Import groundcontrol.ini", False, "medium", "content"
        elif pageID == "actions":
            page = render_template("actions.html")
            return page, "Actions", False, "large", "content"
        elif pageID == "zAxis":
            socketio.emit("closeModals", {"data": {"title": "Actions"}}, namespace="/MaslowCNC")
            distToMoveZ = self.data.config.getValue("Computed Settings", "distToMoveZ")
            unitsZ = self.data.config.getValue("Computed Settings", "unitsZ")
            page = render_template("zaxis.html", distToMoveZ=distToMoveZ, unitsZ=unitsZ)
            return page, "Z-Axis", False, "medium", "content"
        elif pageID == "setSprockets":
            socketio.emit("closeModals", {"data": {"title": "Actions"}}, namespace="/MaslowCNC")
            page = render_template("setSprockets.html")
            return page, "Set Sprockets", False, "medium", "content"
        elif pageID == "triangularCalibration":
            socketio.emit("closeModals", {"data": {"title": "Actions"}}, namespace="/MaslowCNC")
            motorYoffset = self.data.config.getValue("Maslow Settings", "motorOffsetY")
            rotationRadius = self.data.config.getValue("Advanced Settings", "rotationRadius")
            chainSagCorrection = self.data.config.getValue(
                "Advanced Settings", "chainSagCorrection"
            )
            page = render_template(
                "triangularCalibration.html",
                pageID="triangularCalibration",
                motorYoffset=motorYoffset,
                rotationRadius=rotationRadius,
                chainSagCorrection=chainSagCorrection,
            )
            return page, "Triangular Calibration", True, "large", "content"
        elif pageID == "opticalCalibration":
            socketio.emit("closeModals", {"data": {"title": "Actions"}}, namespace="/MaslowCNC")
            opticalCenterX = self.data.config.getValue("Optical Calibration Settings", "opticalCenterX")
            opticalCenterY = self.data.config.getValue("Optical Calibration Settings", "opticalCenterY")
            scaleX = self.data.config.getValue("Optical Calibration Settings", "scaleX")
            scaleY = self.data.config.getValue("Optical Calibration Settings", "scaleY")
            gaussianBlurValue = self.data.config.getValue("Optical Calibration Settings", "gaussianBlurValue")
            cannyLowValue = self.data.config.getValue("Optical Calibration Settings", "cannyLowValue")
            cannyHighValue = self.data.config.getValue("Optical Calibration Settings", "cannyHighValue")
            autoScanDirection = self.data.config.getValue("Optical Calibration Settings", "autoScanDirection")
            markerX = self.data.config.getValue("Optical Calibration Settings", "markerX")
            markerY = self.data.config.getValue("Optical Calibration Settings", "markerY")
            tlX = self.data.config.getValue("Optical Calibration Settings", "tlX")
            tlY = self.data.config.getValue("Optical Calibration Settings", "tlY")
            brX = self.data.config.getValue("Optical Calibration Settings", "brX")
            brY = self.data.config.getValue("Optical Calibration Settings", "brY")
            calibrationExtents = self.data.config.getValue("Optical Calibration Settings", "calibrationExtents")
            page = render_template("opticalCalibration.html", pageID="opticalCalibration", opticalCenterX=opticalCenterX, opticalCenterY=opticalCenterY, scaleX=scaleX, scaleY=scaleY, gaussianBlurValue=gaussianBlurValue, cannyLowValue=cannyLowValue, cannyHighValue=cannyHighValue, autoScanDirection=autoScanDirection, markerX=markerX, markerY=markerY, tlX=tlX, tlY=tlY, brX=brX, brY=brY, calibrationExtents=calibrationExtents, isMobile=isMobile)
            return page, "Optical Calibration", True, "large", "content"
        elif pageID == "quickConfigure":
            socketio.emit("closeModals", {"data": {"title": "Actions"}}, namespace="/MaslowCNC")
            motorOffsetY = self.data.config.getValue("Maslow Settings", "motorOffsetY")
            rotationRadius = self.data.config.getValue("Advanced Settings", "rotationRadius")
            kinematicsType = self.data.config.getValue("Advanced Settings", "kinematicsType")
            if kinematicsType != "Quadrilateral":
                if abs(float(rotationRadius) - 138.4) < 0.01:
                    kinematicsType = "Ring"
                else:
                    kinematicsType = "Custom"
            motorSpacingX = self.data.config.getValue("Maslow Settings", "motorSpacingX")
            chainOverSprocket = self.data.config.getValue(
                "Advanced Settings", "chainOverSprocket"
            )
            print("MotorOffsetY=" + str(motorOffsetY))
            page = render_template(
                "quickConfigure.html",
                pageID="quickConfigure",
                motorOffsetY=motorOffsetY,
                rotationRadius=rotationRadius,
                kinematicsType=kinematicsType,
                motorSpacingX=motorSpacingX,
                chainOverSprocket=chainOverSprocket,
            )
            return page, "Quick Configure", False, "medium", "content"
        elif pageID == "screenAction":
            print(args["x"])
            page = render_template("screenAction.html", posX=args["x"], posY=args["y"])
            return page, "Screen Action", False, "medium", "content"

