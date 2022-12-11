import bpy
from pathlib import Path

def load_image(img_path):
    if Path(img_path).is_file():
        img = bpy.data.images.load(img_path, check_existing=True)
    
    return img

def composite_canyon():
    scene = bpy.context.scene
    node_tree = scene.node_tree
    
    for i in node_tree.nodes:
        node_tree.nodes.remove(i)

    filepath1 = "D:\Downloads\Canyon_Cowboy_Rendered_Layers-20220216T121744Z-001\Canyon_Cowboy_Rendered_Layers\Background.png"
    filepath2 = "D:\Downloads\Canyon_Cowboy_Rendered_Layers-20220216T121744Z-001\Canyon_Cowboy_Rendered_Layers\Foreground.png"
    filepath3 = "D:\Downloads\Canyon_Cowboy_Rendered_Layers-20220216T121744Z-001\Canyon_Cowboy_Rendered_Layers\Sky_Background.png"

    image_1 = node_tree.nodes.new(type="CompositorNodeImage")
    image_1.image = load_image(filepath1)
    image_2 = node_tree.nodes.new(type="CompositorNodeImage")
    image_2.image = load_image(filepath2)
    image_3 = node_tree.nodes.new(type="CompositorNodeImage")
    image_3.image = load_image(filepath3)

    node_1 = node_tree.nodes.new(type="CompositorNodeAlphaOver")
    node_2 = node_tree.nodes.new(type="CompositorNodeAlphaOver")
    node_3 = node_tree.nodes.new(type="CompositorNodeAlphaOver")

    render_node = node_tree.nodes.new(type="CompositorNodeRLayers")

    composite_node = node_tree.nodes.new(type="CompositorNodeComposite")

    node_tree.links.new(image_3.outputs["Image"], node_3.inputs[1])
    node_tree.links.new(image_1.outputs["Image"], node_3.inputs[2])

    node_tree.links.new(node_3.outputs["Image"], node_1.inputs[1])
    node_tree.links.new(render_node.outputs["Image"], node_1.inputs[2])

    node_tree.links.new(image_2.outputs["Image"], node_2.inputs[2])
    node_tree.links.new(node_1.outputs["Image"], node_2.inputs[1])

    node_tree.links.new(node_2.outputs["Image"], composite_node.inputs[0])
