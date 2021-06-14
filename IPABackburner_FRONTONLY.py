import maya.cmds as cmds
import maya.mel as mm
import os


# MARK: SETS GENERAL RENDER SETTINGS

render_default = 'defaultRenderGlobals'
render_arnold = 'defaultArnoldDriver'
render_glob = render_arnold
list_Attr = cmds.listAttr(render_glob, r = False, s = True)
for attr in list_Attr:
    get_attr_name = "%s.%s"%(render_glob, attr)
    print "stAttr %s %s"%(get_attr_name, cmds.getAttr(get_attr_name))

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



# MARK: SETUP FOR FRONT RENDER

# Show everything (body and mouthbag)
cmds.showHidden('Evelyn_Full')
cmds.hide('Mouthbag_Full')

# Set front camera as render cam
cmds.setAttr('perspShape.renderable', 0)
cmds.setAttr('Evelyn_FrenchSpeak_Master:Side_Camera.renderable', 0)
cmds.setAttr('Evelyn_FrenchSpeak_Master:Front_Camera.renderable', 1)

# Save As a new file (_frontCam)
filePath = cmds.file(q=True, sn=True)
slashIndex = filePath.rfind("/")
savePath = filePath[:slashIndex]
jobName = filePath[slashIndex + 1:].split(".")[0]

finalFileName = "{jobName}_frontCam.mb".format(jobName=jobName)

finalSavePath = (os.path.join(savePath, finalFileName)).replace("\\", "/")
cmds.file(rename=finalSavePath)
cmds.file(save=True, type="mayaBinary", f=True)

# Give user new Backburner command
projectPath = "V:/Animation/2021/BYU Online/French IPA/Projects/French_IPA_Project/Renders/MayaRenders"

renderPath = filePath.split("Scenes/")[1]
slashIndex = renderPath.rfind("/")
renderPath = renderPath[:slashIndex]

finalRenderPath = (os.path.join(projectPath, renderPath, jobName)).replace("\\", "/")


final = "\"\\\"\\\"C:/Program Files (x86)/Autodesk/Backburner/cmdjob.exe\\\" -jobName \\\"{jobName}\\\" -description \\\"\\\" -manager 10.25.15.188 -port 7347 -priority 50 -taskList \\\"C:/Users/gjr215/AppData/Local/Temp/{jobName}.txt\\\" -taskName 1 \\\"C:/Program Files/Autodesk/Maya2020/bin/Render\\\" -r file -s %tp2 -e %tp3 -proj \\\"C:/Users/gjr215/Documents/maya/projects/default\\\" -rd \\\"{writeDirectory}\\\"  \\\"{projectName}\\\"\"".format(jobName = jobName, projectName = filePath, writeDirectory = finalRenderPath)
print("***COPY AND PASTE THIS COMMAND INTO THE BACKBURNER WINDOW***")
print(final)
printSend = mm.eval('system (' + final + ')')
print printSend
