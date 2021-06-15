import maya.cmds as cmds
import maya.mel as mm
import os
import getpass
import tempfile

# Generate temp file
def generateTempFile(jobName, cameraName):
    print("Generating temp file for {printFileName}".format(printFileName=cmds.file(q=True, sn=True, shn=True)))
    taskList = "{jobName}_{cameraName}".format(jobName=jobName, cameraName=cameraName)
    tempFileName = tempfile.gettempdir()
    tempFileName = tempFileName.replace("\\", '/')
    tempFileName += '/' + taskList + '.txt'
    taskListFile = open(tempFileName, 'w')
    if (taskListFile == 0):
        mc.error('You dont have privilages')
    startFrame = 0
    endFrame = cmds.playbackOptions( q=True,max=True )
    taskSize = 4
    numberTasks = (float(endFrame) - float(startFrame)) / float(taskSize)
    if (numberTasks > int(numberTasks)):
        numberTasks = int(numberTasks) + 1
    startTaskFrame = startFrame
    lastTaskFrame = startFrame + taskSize - 1
    for task in range(int(numberTasks) + 1):
        if (lastTaskFrame >= endFrame):
            taskListFile.write("frameRange " + str(startTaskFrame) + "-" + str(endFrame) + "\t" + str(startTaskFrame) + "\t" + str(endFrame) + "\n")
            break
        taskListFile.write("frameRange " + str(startTaskFrame) + "-" + str(lastTaskFrame) + "\t" + str(startTaskFrame) + "\t" + str(lastTaskFrame) + "\n")
        startTaskFrame += taskSize
        lastTaskFrame += taskSize
    taskListFile.close()
    return tempFileName


# Execute Backburner job
def executeBackburner(cameraName, savePath):
    if cameraName is "FrontCam":
        cmds.showHidden('Carolina_GermanSpeak_Master:Carolina_IPA:Carolina')
        cmds.hide('Mouthbag')

        # Set front camera as render cam
        cmds.setAttr('perspShape.renderable', 0)
        cmds.setAttr('Carolina_GermanSpeak_Master:Carolina_Side.renderable', 0)
        cmds.setAttr('Carolina_GermanSpeak_Master:Carolina_Front', 1)
        cmds.setAttr('Evelyn_FrenchSpeak_Master:Mouthbag_Camera.renderable', 0)
    elif cameraName is "SideCam":
        cmds.showHidden('Carolina_GermanSpeak_Master:Carolina_IPA:Carolina')
        cmds.hide('Mouthbag')

        # Set side camera as render cam
        cmds.setAttr('perspShape.renderable', 0)
        cmds.setAttr('Carolina_GermanSpeak_Master:Carolina_Side.renderable', 1)
        cmds.setAttr('Carolina_GermanSpeak_Master:Carolina_Front', 0)
        cmds.setAttr('Evelyn_FrenchSpeak_Master:Mouthbag_Camera.renderable', 0)
    else:
        cmds.hide('Carolina_GermanSpeak_Master:Carolina_IPA:Carolina')
        cmds.showHidden('Mouthbag')

        # Set side camera as render cam
        cmds.setAttr('perspShape.renderable', 0)
        cmds.setAttr('Carolina_GermanSpeak_Master:Carolina_Side.renderable', 0)
        cmds.setAttr('Carolina_GermanSpeak_Master:Carolina_Front', 0)
        cmds.setAttr('Evelyn_FrenchSpeak_Master:Mouthbag_Camera.renderable', 1)

    # Save As a new file
    filePath = cmds.file(q=True, sn=True)
    slashIndex = filePath.rfind("/")
    # savePath = filePath[:slashIndex]
    jobName = filePath[slashIndex + 1:].split(".")[0]
    if jobName.count("_") is not 1: # FIXME: Do it by camera rather than the name since there are going to be a bunch of weird exceptions
        jobName = jobName[:jobName.rfind("_")]
    finalFileName = "{jobName}_{cameraName}.mb".format(jobName=jobName, cameraName=cameraName)
    finalSavePath = (os.path.join(savePath, finalFileName)).replace("\\", "/")
    print("Saving file: {finalSavePath}".format(finalSavePath))
    cmds.file(rename=finalSavePath)
    cmds.file(save=True, type="mayaBinary", f=True)

    # Generate temp
    generateTempFile(jobName, cameraName)

    # Generate and execute new Backburner command
    projectPath = r"V:/Animation/2021/BYU Online/French IPA/Projects/French_IPA_Project/Renders/MayaRenders"
    renderPath = filePath.split("Scenes/")[1]
    slashIndex = renderPath.rfind("/")
    renderPath = renderPath[:slashIndex]
    slashIndex = filePath.rfind("/")
    jobFolder = filePath[slashIndex + 1:].split(".")[0]
    finalRenderPath = (os.path.join(projectPath, renderPath, jobName, cameraName)).replace("\\", "/")
    print("Rendering to : {finalRenderPath}".format(finalRenderPath=finalRenderPath))
    final = "\"\\\"\\\"C:/Program Files (x86)/Autodesk/Backburner/cmdjob.exe\\\" -jobName \\\"{jobName}_{cameraName}\\\" -description \\\"\\\" -manager 10.25.15.188 -port 7347 -priority 1 -taskList \\\"C:/Users/{username}/AppData/Local/Temp/{jobName}_{cameraName}.txt\\\" -taskName 1 \\\"C:/Program Files/Autodesk/Maya2020/bin/Render\\\" -r file -s %tp2 -e %tp3 -proj \\\"C:/Users/{username}/Documents/maya/projects/default\\\" -rd \\\"{writeDirectory}\\\"  \\\"{projectName}\\\"\"".format(jobName = jobName, username = getpass.getuser(), cameraName = cameraName, projectName = finalSavePath, writeDirectory = finalRenderPath)
    print("Sending to Backburner")
    print(final)
    printSend = mm.eval('system (' + final + ')')
    print printSend


# Duplicate Side Camera and name it "Mouthbag_Camera"
def duplicateCam(CameraName):
    cmds.select(CameraName, r=True)
    cmds.duplicate(rr=True, n= 'Carolina_GermanSpeak_Master:Mouthbag_Camera')


#Duplicate Camera
duplicateCam('Carolina_GermanSpeak_Master:Carolina_Side')


# MARK: SETS GENERAL RENDER SETTINGS
render_default = 'defaultRenderGlobals'
render_arnold = 'defaultArnoldDriver'
render_glob = render_arnold
list_Attr = cmds.listAttr(render_glob, r = False, s = True)
for attr in list_Attr:
    get_attr_name = "%s.%s"%(render_glob, attr)
    print "stAttr %s %s"%(get_attr_name, cmds.getAttr(get_attr_name))

# Create a new folder to put all the extra Maya files into
filePath = cmds.file(q=True, sn=True)
slashIndex = filePath.rfind("/")
jobName = filePath[slashIndex + 1:].split(".")[0]
filePath = filePath[:slashIndex]
mode = 0o777
path = (os.path.join(filePath, jobName))

if not os.path.exists(path):
    os.mkdir(path, mode)
    print("Created folder at {path}".format(path=path))
else:
    print("Folder already exists, skipped creating")

#Set file output to tif
cmds.setAttr("defaultArnoldDriver.ai_translator", "tif", type="string")
cmds.setAttr('defaultArnoldDriver.tiffCompression', 0)
cmds.setAttr('defaultArnoldDriver.tiffFormat', 2)

#Setting the namespace to name_#.ext
cmds.setAttr ('defaultRenderGlobals.outFormatControl', 0)
cmds.setAttr ('defaultRenderGlobals.animation', 1)
cmds.setAttr ('defaultRenderGlobals.putFrameBeforeExt', 1)
cmds.setAttr ('defaultRenderGlobals.periodInExt', 2)
cmds.setAttr ('defaultRenderGlobals.extensionPadding', 3)

#Set end frame for rendering
anim_end_frame = cmds.playbackOptions(maxTime =True, q=True)
cmds.setAttr('defaultRenderGlobals.endFrame', anim_end_frame)

#Change image size
cmds.setAttr('defaultResolution.width',1920)
cmds.setAttr('defaultResolution.height',1080)
cmds.setAttr('defaultResolution.deviceAspectRatio',1.777)

executeBackburner("FrontCam", path)
executeBackburner("SideCam", path)

cmds.setAttr('Evelyn_FrenchSpeak_Master:DomeLightShape.camera', 0)
cmds.setAttr('Evelyn_FrenchSpeak_Master:DomeLight.visibility', 0)
executeBackburner("MouthBag", path)

print("Finished")
