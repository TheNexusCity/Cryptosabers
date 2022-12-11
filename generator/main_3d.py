import json
import os
import subprocess

import bpy
import sys
import certifi
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
os.environ["SSL_CERT_FILE"] = certifi.where()

import obj_map

# check input args
# the first user arg is the start frame
# if none is provided, set the start frame to 0
if len(sys.argv) > 5:
    start_frame = int(sys.argv[5])
else:
    start_frame = 0
# the second user arg is the end frame
# if none is provided, set the end frame to 19999
if len(sys.argv) > 6:
    end_frame = int(sys.argv[6])
else:
    end_frame = 19999

#creates out folder for renders
OUT_PATH = "out"

if not os.path.exists(OUT_PATH):
    os.mkdir(OUT_PATH)

result_coll = "output"
light_intesity = 1.0
data = None


def render(output_dir, output_filename='render.jpg'):
    bpy.context.scene.render.filepath = os.path.join(
        os.path.abspath(output_dir), output_filename)
    bpy.ops.render.render(write_still=True)


def collectionIterator(collection):
    # yield collection

    if hasattr(collection, 'objects'):
        for obj in collection.objects:
            yield obj

    if hasattr(collection, 'children'):
        for coll in collection.children:
            yield from collectionIterator(coll)


def objectIterator(collection):
    yield collection

    if hasattr(collection, 'objects'):
        for obj in collection.objects:
            yield obj

    if hasattr(collection, 'children'):
        for coll in collection.children:
            yield from objectIterator(coll)


def deactivate_obj(obj):

    obj.hide_render = True
    obj.hide_select = True
    obj.hide_viewport = True


def activate_obj(obj):
    obj.hide_render = False
    obj.hide_select = False
    obj.hide_viewport = False


def deactivate_collections():
    for x in bpy.data.collections:
        print("##### collection for deactivation:", x.name)
        if x.name != 'Frame_Environment':
            if x.name != result_coll:
                deactivate_obj(x)
                for y in x.objects:
                    deactivate_obj(y)


def deactivate_this_collection(coll_name):
    parent_coll = bpy.data.collections[coll_name]

    for obj in collectionIterator(parent_coll):
        deactivate_obj(obj)


def activate_collections():
    for x in bpy.data.collections:
        print("$$$$$ activating collection ", x.name)
        activate_obj(x)
        for y in x.objects:
            activate_obj(y)


def move_obj_to_collection(obj_name, target=result_coll):
    if obj_name == "None":

        print("{} name None".format(obj_name))
        return

    try:
        for i in getChildren(bpy.data.objects[obj_name]):
            move_obj_to_collection(i.name)
        obj = bpy.data.objects[obj_name].copy()
        coll_target = bpy.data.collections[target]
        coll_target.objects.link(obj)
        activate_obj(obj)
        if len(getChildren(obj)) > 0:
            print(getChildren(obj))
            for i in getChildren(obj):
                move_obj_to_collection(i)
    except:
        print("{} not found".format(obj_name))
        return


def delete_collection(collection):
    for obj in collection.objects:
        bpy.data.objects.remove(obj, do_unlink=True)

    bpy.data.collections.remove(collection)


def clear_output():
    collection = bpy.data.collections[result_coll]
    for x in collection.objects:
        bpy.data.objects.remove(x, do_unlink=True)
    for x in collection.children:
        delete_collection(x)


def getChildren(obj):
    children = []
    for ob in bpy.data.objects:
        if ob.parent == obj:
            children.append(ob)
    return children


def scale_obj(obj, value=1):
    obj.scale = (value, value, value)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, scale=True, rotation=False)


def hide_all():
    return


def show_all_inside_obj(obj_name):

    parent_obj = bpy.data.objects[obj_name]

    for obj in objectIterator(parent_obj):
        activate_obj(obj)


def main():
    counter = 0

    # open blend file
    bpy.ops.wm.open_mainfile(filepath=os.path.abspath("./blend/scene.blend"))

    # iterate through all objects and remove all shape keys
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            if(obj.data.shape_keys != None and obj.data.shape_keys.key_blocks != None):
                obj.active_shape_key_index = 0
                for k in obj.data.shape_keys.key_blocks:
                    obj.shape_key_remove(k)

    bpy.context.view_layer.update()

    # iterate through all bones and replace 'mixamorig:' with ''
    for armature in bpy.data.armatures:
        for bone in armature.bones:
            bone.name = bone.name.replace('mixamorig:', '')
            bone.name = bone.name.replace('Wasit', 'Waist')
            bone.name = bone.name.replace('.', '')
            bone.name = bone.name.replace('001', '1')
            bone.name = bone.name.replace('002', '2')


    # open and load json file
    with open("./data.json", "r") as file:
        data = json.load(file)

    # create render collection within blender file
    collection = bpy.context.blend_data.collections.new(name=result_coll)
    bpy.context.scene.collection.children.link(collection)

    # loop through json file
    for i in range(start_frame, end_frame):
        x = data[i]
        # activates all objects and collections
        deactivate_this_collection("Cryptosaber")

        for attr in x["attributes"]:
            print(attr["value"])
            # finds the traits of current json object and moves the to output collection
            if attr["trait_type"] == "bladeColor":
                show_all_inside_obj(obj_map.bladeColor[attr["value"]])
            if attr["trait_type"] == "bladeColor":
                show_all_inside_obj(obj_map.bladeColor[attr["value"]])
            if attr["trait_type"] == "switchType":
                show_all_inside_obj(obj_map.switchType[attr["value"]])
            if attr["trait_type"] == "handleType":
                show_all_inside_obj(obj_map.handleType[attr["value"]])
            if attr["trait_type"] == "colorScheme":
                show_all_inside_obj(obj_map.colorScheme[attr["value"]])
            if attr["trait_type"] == "emitterType":
                show_all_inside_obj(obj_map.emitterType[attr["value"]])
            # if attr["trait_type"] == "backgrounds":
            #     bpy.context.scene.frame_set(
            #         obj_map.background[attr["value"]])  # set frame with pose

        for obj in objectIterator(bpy.data.collections["Cryptosaber"]):
            try:
                obj.select_set(True)
            except:
                pass

        # find the Armature object, make sure it is enabled and selected
        armature = bpy.data.objects["Armature"]
        armature.select_set(True)
        armature.hide_set(False)

        bpy.context.scene.frame_set(13)
        if os.path.exists("./out/{}.glb".format(counter)):
            os.remove("./out/{}.glb".format(counter))
        if os.path.exists("./combined/{}.glb".format(counter)):
            os.remove("./combined/{}.glb".format(counter))

        # if current frame is not 13, set it to 13
        if bpy.context.scene.frame_current != 13:
            bpy.context.scene.frame_set(13)

        bpy.ops.export_scene.gltf(filepath="./out/{}.glb".format(str(counter)),
                                  use_selection=True,
                                #   use_visible=True,
                                  use_renderable=True,
                                  export_animations=False,
                                  export_current_frame=True,
                                  export_apply=True)


        # call combine.sh with the arg of the current counter
        print("Calling combine script on model...")
        subprocess.call(["bash", "./combine.sh", str(counter)])
        clear_output()
        counter += 1


if __name__ == "__main__":
    main()
