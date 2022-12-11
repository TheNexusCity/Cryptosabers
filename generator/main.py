import bpy
import os
import re
import json
import sys
import math
from pathlib import Path

sys.path.append(os.getcwd())

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

print('Running script...')
print('Start frame: ', start_frame)
print('End frame: ', end_frame)

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
        # print("$$$$$ collection for activation:", x.name)
        # if x.name != 'Frame_Environment':
        print("$$$$$ activating collection ", x.name)
        activate_obj(x)
        for y in x.objects:
            activate_obj(y)


# def activate_collection(coll):
#     if coll in bpy.data.collections:
#         x = bpy.data.collections[coll]
#     activate_obj(x)
#     for y in x.objects:
#         activate_obj(y)


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
    counter = start_frame

    # open blend file
    bpy.ops.wm.open_mainfile(filepath=os.path.abspath("./blend/scene.blend"))

    # for name in obj_map.all:
    #     if str(name) in bpy.data.objects:
    #         pass
    #     else:
    #         print(" ########### not found", name)

    # bpy.data.objects.remove(bpy.data.objects['Camera'])

    # base_object_path = os.path.join('./base.blend', "Object")
    # bpy.ops.wm.append(filename='Camera', directory=str(base_object_path))
    # bpy.ops.wm.append(filename='Point', directory=str(base_object_path))
    # bpy.ops.wm.append(filename='Point.001', directory=str(base_object_path))

    # bpy.data.objects["Point"].data.energy = light_intesity
    # bpy.data.objects["Point.001"].data.energy = light_intesity
    # if "Camera" in bpy.data.objects:
    #     print("camera imported")

    # if "Point" in bpy.data.objects:
    #     print("light imported")

    bpy.context.scene.render.film_transparent = True

    # open and load json file
    with open("./data.json", "r") as file:
        data = json.load(file)

    # create render collection within blender file
    collection = bpy.context.blend_data.collections.new(name=result_coll)
    bpy.context.scene.collection.children.link(collection)

    # sets armature to pose mode
    armature = bpy.data.objects["Armature"]
    armature.data.pose_position = 'POSE'
    # scale_obj(armature)

    # loop through data, from start_frame to end_frame
    for i in range(start_frame, end_frame):
        x = data[i]
        # activates all objects and collections
        deactivate_this_collection("Cryptosaber")

        for attr in x["attributes"]:
            print(attr["value"])
            # finds the traits of current json object and moves the to output collection
            if attr["trait_type"] == "outfit":
                show_all_inside_obj(obj_map.oufit[attr["value"]])
            if attr["trait_type"] == "head":
                show_all_inside_obj(obj_map.head[attr["value"]])
            if attr["trait_type"] == "hat":
                show_all_inside_obj(obj_map.hat[attr["value"]])
            if attr["trait_type"] == "boots":
                show_all_inside_obj(obj_map.boots[attr["value"]])
            if attr["trait_type"] == "vambrace":
                show_all_inside_obj(obj_map.vambrace[attr["value"]])
            if attr["trait_type"] == "epaulettes":
                show_all_inside_obj(obj_map.epaulettes[attr["value"]])
            if attr["trait_type"] == "back":
                show_all_inside_obj(obj_map.back[attr["value"]])
            if attr["trait_type"] == "torso":
                show_all_inside_obj(obj_map.torso[attr["value"]])
            if attr["trait_type"] == "arms":
                show_all_inside_obj(obj_map.arms[attr["value"]])
            if attr["trait_type"] == "garment":
                show_all_inside_obj(obj_map.garment[attr["value"]])
            if attr["trait_type"] == "guns":
                show_all_inside_obj(obj_map.guns[attr["value"]])
            # if attr["trait_type"] == "backgrounds":
            #     move_obj_to_collection(obj_map.background_map[attr["value"]])
            if attr["trait_type"] == "backgrounds":
                bpy.context.scene.frame_set(
                    obj_map.background[attr["value"]])  # set frame with pose

        #sets objects as children of armature
        # for i in bpy.data.collections[result_coll].objects:
        #     if len(i.modifiers) > 0:
        #         i.modifiers["Armature"].object = armature
        #         i.modifiers["Armature"].use_bone_envelopes = True
        #     i.parent = armature

        # for debugging
        for i in bpy.data.collections["output"].objects:
            print(i.name)

        for obj in objectIterator(bpy.data.collections["Cryptosaber"]):
            try:
                obj.select_set(True)
            except:
                pass

        render(output_dir="./out", output_filename=str(counter))
        clear_output()
        counter += 1


if __name__ == "__main__":
    main()