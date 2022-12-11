import os
import sys

import bpy
sys.path.append(os.getcwd())
import urllib.request
import certifi
import urllib

sys.path.append(os.getcwd())

# check for CATS blender plugin
def check_cats_addon():
    addon_path = os.path.join(os.getcwd(), 'addons', 'cats-blender-plugin-master.zip')
    if not os.path.exists(addon_path):
        print('Combiner addon not found, downloading...')
        url = 'https://github.com/absolute-quantum/cats-blender-plugin/archive/master.zip'
        urllib.request.urlretrieve(url, addon_path)

# check_cats_addon()

# check if the file exists at ./addons/VRM_Addon_for_Blender-release.zip
# if not, download it from github
def check_vrm_addon():
    addon_path = os.path.join(os.getcwd(), 'addons', 'VRM_Addon_for_Blender-release.zip')
    if not os.path.exists(addon_path):
        print('VRM addon not found, downloading...')
        url = 'https://github.com/saturday06/VRM_Addon_for_Blender/raw/release-archive/VRM_Addon_for_Blender-release.zip'
        urllib.request.urlretrieve(url, addon_path)
        print('VRM addon downloaded')

check_vrm_addon()

bpy.ops.preferences.addon_install(overwrite=True,filepath='./addons/cats-blender-plugin-master.zip') 
bpy.ops.preferences.addon_enable(module='cats-blender-plugin-master')

bpy.ops.preferences.addon_install(overwrite=True,filepath='./addons/VRM_Addon_for_Blender-release.zip') 
bpy.ops.preferences.addon_enable(module='VRM_Addon_for_Blender-release')


bpy.ops.wm.save_userpref()

print('sys.argv', sys.argv)

# get the glb name from the first arg passed to the command line
glb_path = "combined/" + sys.argv[4] + '.glb'
print('glb name is', glb_path)

# open blend file
bpy.ops.wm.open_mainfile(filepath=os.path.abspath("./blend/combiner.blend"))

print("glb_path" + glb_path)
# import glb at glb_path
bpy.ops.import_scene.gltf(filepath=glb_path)

print('Scene contents:')
for obj in bpy.data.objects:
    print(obj.name)

print('Processing ' + glb_path)

# copy all of the bone positions and rotations from Armature to Armature.001
print('bpy.data.objects[AvatarRoot].pose.bones')

vrm_out_file = glb_path.replace('glb', 'vrm')
bpy.ops.vrm.load_human_bone_mappings(filepath="./bonemap.json")
print('Loaded bone map')

# empty dictionary called merge
merge = {}

# iterate over all objects
# if there is another object with the same name but .001 or .002 at the end, merge them into the first object
for obj in bpy.data.objects:
    merge = []
    # check if other objects have the same name but .001 or .002 at the end
    for obj2 in bpy.data.objects:
        # if obj2 name includes obj 1 name and .001 or .002 at the end
        if obj2.name.startswith(obj.name) and obj2.name.endswith('.001') or obj2.name.endswith('.002'):
            # add obj2 to merge
            merge.append(obj2)
    # if merge is not empty
    if merge:
        # merge all objects in merge into obj
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        for m in merge:
            m.select_set(True)
        # set obj as active object
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.join()

# iterate through all armatures in scene
# for each bone that contains the string 'mixamorig' but does not contain 'mixamorig:', replace 'mixamorig' with 'mixamorig:'
for armature in bpy.data.armatures:
    for bone in armature.bones:
        # remove all . : and ' ' from name
        bone.name = bone.name.replace('.', '').replace(':', '').replace(' ', '')

# Set the target of the armature modifier on all meshes in the scene to the "Armature" object
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        for mod in obj.modifiers:
            if mod.type == 'ARMATURE':
                mod.object = bpy.data.objects['Armature']

for obj in bpy.data.objects:
    if obj.type == 'MESH':
        # set the object parent to objects['Armature']
        obj.parent = bpy.data.objects['Armature']

# Delete any armatures that are not the "Armature" object
for obj in bpy.data.objects:
    if obj.type == 'ARMATURE' and obj.name != 'Armature':
        obj.select_set(True)
    else:
        obj.select_set(False)
bpy.ops.object.delete()

print('Exporting objects')
for obj in bpy.data.objects:
    print(obj.name)

# Export VRM

# # get all objects
# objects = bpy.context.selected_objects

# with bpy.context.temp_override(active_object=bpy.context.active_object, selected_editable_objects=objects):
#     bpy.ops.object.join()

# # select all objects
# bpy.ops.object.select_all(action='SELECT')

# # set the Armature to active
# bpy.context.view_layer.objects.active = bpy.data.objects['Armature']

# # print out the contents of the scene
# print('Scene contents:')
# for obj in bpy.data.objects:
#     print(obj.name)

# select armature
bpy.data.objects['Armature'].select_set(True)

# call 'fix model' from cats blender plugin
#bpy.ops.cats.fix_model()

bpy.ops.export_scene.vrm(filepath=vrm_out_file, export_invisibles=False, export_only_selections=False, enable_advanced_preferences=False, export_fb_ngon_encoding=False)
print('Exported', vrm_out_file)