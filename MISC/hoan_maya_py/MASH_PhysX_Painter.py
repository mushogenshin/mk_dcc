import MASH.api as mapi
import pymel.core as pm
import maya.cmds as cmds

node_prefix = 'mnT2_'

dyn_friction = 0.3
dyn_rolling_friction = 0.2
dyn_damping = 0.1
dyn_rolling_damping = 0.02
dyn_bounce = 0.05

selected_objs = pm.ls(sl=1)

cloud_plane_mesh = selected_objs[0].getShape()  # TODO: the user should be able to load this in herself

mesh_instances = selected_objs[1:-1]
instances_num = len(mesh_instances)

ground_plane_mesh = selected_objs[-1].getShape()

# excludes the cloud and the ground

pm.select(mesh_instances, r=1)

mashNetwork = mapi.Network()
mashNetwork.createNetwork(name=node_prefix + "MASH")
# help(mashNetwork)

# accesses the default Distribute node
mashDistribute = pm.PyNode(mashNetwork.distribute)
mashDistribute.pointCount.set(0)

# accesses the default Repro node 
mashRepro = pm.PyNode(mashNetwork.instancer)

# adds a Placer node
mashPlacer = mashNetwork.addNode("MASH_Placer")
mashPlacer = pm.PyNode(mashPlacer.name)
mashPlacer.scatter.set(True)
mashPlacer.idMode.set(2)  # sets it to "Random"
mashPlacer.randomId1.set(instances_num - 1)  # array index # TODO: change this logic w/ implementing UI

# connects the "cloud plane" to the Placer's paint meshes
cloud_plane_mesh.worldMesh[0].connect(mashPlacer.paintMeshes[0])

# adds a Dynamics node
mashDynamics = mashNetwork.addNode("MASH_Dynamics")
mashDynamics = pm.PyNode(mashDynamics.name)
mashDynamics.collisionShape.set(4)  # sets it to "Convex Hull"
pm.listAttr(mashDynamics)

# TODO: tweak the Dynamics parameters
mashDynamics.friction.set(dyn_friction)
mashDynamics.rollingFriction.set(dyn_rolling_friction)
mashDynamics.damping.set(dyn_damping)
mashDynamics.rollingDamping.set(dyn_rolling_damping)
mashDynamics.bounce.set(dyn_bounce)

# accesses the Bullet Solver
mashBullet = pm.PyNode(mashNetwork.getSolver())
# pm.listAttr(mashBullet)

if not ground_plane_mesh:
    mashBullet.groundPlanePositionY.set(0)  # overrides the default value of -20
else:
    # disables the Bullet's built-in ground
    mashBullet.groundPlane.set(False)
    # loads the custom ground plane to the Bullet
    mashNetwork.addCollider(ground_plane_mesh.nodeName())  # TODO: add support for multiple collider objs 
    
# TODO: select the Placer node
# cmds.AttributeEditor()

# TODO: increase the time range; go to first frame
# pm.mel.InteractivePlayback()
# play -record;


