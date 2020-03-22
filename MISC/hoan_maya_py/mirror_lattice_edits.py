import pymel.core as pm

# queries the lattices from selection

src_Lattice = pm.selected()[0]
dst_Lattice = pm.selected()[1]

# gets the lattice shapes
src_LatticeShape = src_Lattice.getShape()
dst_LatticeShape = dst_Lattice.getShape()

# gets the FFDs
src_FFD = src_LatticeShape.worldMatrix[0].listConnections()[0]
dst_FFD = dst_LatticeShape.worldMatrix[0].listConnections()[0]

# creates a new lattice
custom_LatticeShape = pm.createNode("lattice")
custom_Lattice = custom_LatticeShape.getParent()

# connects the destination lattice xform to the custom lattice xform

dst_Lattice.t.connect(custom_Lattice.t)
dst_Lattice.r.connect(custom_Lattice.r)
dst_Lattice.sy.connect(custom_Lattice.sy)
dst_Lattice.sz.connect(custom_Lattice.sz)

# negates the Scale X value of the custom lattice xform

negate_doubleLinear = pm.createNode("multDoubleLinear")
negate_doubleLinear.input2.set(-1)

dst_Lattice.sx.connect(negate_doubleLinear.input1)
negate_doubleLinear.output.connect(custom_Lattice.sx)

# does the same for the lattice base

dst_LatticeBase = dst_FFD.baseLatticeMatrix.listConnections(d=True)[0]
negate_doubleLinear.output.connect(dst_LatticeBase.sx)

# connects the lattice shapes
src_LatticeShape.latticeOutput.connect(custom_LatticeShape.latticeInput)

dst_FFD.deformedLatticePoints.disconnect()
custom_LatticeShape.latticeOutput.connect(dst_FFD.deformedLatticePoints)

dst_FFD.deformedLatticeMatrix.disconnect()
custom_LatticeShape.worldMatrix[0].connect(dst_FFD.deformedLatticeMatrix)

# cleans up the redundant lattice
pm.delete(dst_Lattice)

pm.select(src_Lattice, r=True)