import pymel.core as pm
import math

def average(a):
    return sum(a) / len(a)
    
def get_distorted_quad():
    
    mesh = pm.selected()[0].getShape()
    mesh_name = mesh.nodeName()
        
    # queries non-planar faces
    pm.mel.eval('polyCleanupArgList 4 { "0","2","0","0","0","0","0","1","0","1e-05","0","1e-05","0","1e-05","0","-1","0","0" };')
    
    # working on all the non-planar faces found now
    non_planar_faces = pm.selected()
    
    for face_series in non_planar_faces:
        for face_id in face_series.indices()
            face = pm.PyNode(mesh_name + ".f[{}]".format(face_id))
        
            face_normal = face.getNormal()
            edgeList = face.getEdges()
    
            dot_list = []
        
            for edge_id in edgeList:
                edge = pm.PyNode(mesh_name + ".e[{}]".format(edge_id))
                edge_vec = edge.getPoint(0, space='world') - edge.getPoint(1, space='world')
                edge_vec.normalize()
            
                dot_prod = face_normal.dot(edge_vec)
                angle_dif = math.fabs(90 - math.degrees(math.acos(dot_prod)))
                dot_list.append(angle_dif)
                
            epsilon = average(dot_list)
    
    
