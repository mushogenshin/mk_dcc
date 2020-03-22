import pymel.core as pm

node_prefix = "mnT2"
morphUV_suffix = "morphed_UV"

selected_xform = pm.ls(sl=1)[0]  # TODO: improve
givenMesh = selected_xform.getShape()

# duplicates the mesh
morphedUV = pm.duplicate(givenMesh, n="_".join([node_prefix, selected_xform.nodeName(), morphUV_suffix]))
morphedUV_mesh = morphedUV[0].getShape()

# queries the vertices that have more than one UV
vertUVs = [vert for vert in morphedUV_mesh.vtx if vert.numUVs() > 1]
# splits those vertices
pm.polySplitVertex(vertUVs)       
# deletes the construction history
pm.delete(morphedUV_mesh, ch=True)

# flattens the mesh
for vert in morphedUV_mesh.vtx:
    pos = vert.getUV()
    vert.setPosition((pos[0], pos[1]))
    
# TODO: scale it? (to size of bounding box?)

# duplicates the "morphed UV"
morphedUV_dup = pm.duplicate(morphedUV_mesh, n="_".join([selected_xform.nodeName(), 'target']))
morphedUV_mesh_dup = morphedUV_dup[0].getShape()
# transfers the attributes to morph this "flattened UV, duplicated" back to the original shape
pm.transferAttributes(givenMesh, morphedUV_mesh_dup, pos=1, nml=1, col=0, uvs=0, sampleSpace=3, searchMethod=3)

# creates a blendShape between the morphed UV meshes
pm.select(morphedUV_mesh_dup, morphedUV_mesh, r=1)
pm.mel.blendShape(origin='world', topologyCheck=0, n="_".join([node_prefix, selected_xform.nodeName(), 'blendShape']))

# hides the blendShape target
pm.hide(morphedUV_dup)