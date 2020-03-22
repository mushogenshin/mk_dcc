for clus in pm.selected():
    
    clusName = clus.name()
    index = int(clusName.split("_")[1])
    
    loc = pm.spaceLocator(n=clusName + "_loc")
    
    loc.translate.set(pm.xform(clus, q=1, rp=1, ws=1))
    loc.rotateY.set(-(index-1)*18)
    pm.parent(clus, loc) 