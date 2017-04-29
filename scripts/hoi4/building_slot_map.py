import _initpath
import os
import math
import re
import collections
import pyradox.config
import pyradox.txt
import pyradox.worldmap
import pyradox.image
from PIL import Image

# Load states.
states = pyradox.txt.parseMerge(os.path.join(pyradox.config.getBasedir('HoI4'), 'history', 'states'), verbose=False)
stateCategories = pyradox.txt.parseMerge(os.path.join(pyradox.config.getBasedir('HoI4'), 'common', 'state_category'), verbose=False)
provinceMap = pyradox.worldmap.ProvinceMap(basedir = pyradox.config.getBasedir('HoI4'))

# provinces -> state id
groups = {}
colormap = {}

for state in states.values():
    stateCategoryKey = state['state_category']
    buildingSlots = stateCategories[stateCategoryKey]['local_building_slots'] or 0

    k = []
    for provinceID in state['provinces']:
        if not provinceMap.isWaterProvince(provinceID):
            k.append(provinceID)
            colormap[provinceID] = pyradox.image.colormapRedGreen(buildingSlots / 10)
    k = tuple(x for x in k)
    groups[k] = '%d' % buildingSlots


# Create a blank map and scale it up 2x.
out = provinceMap.generateImage(colormap, defaultLandColor=(255, 255, 255), edgeColor=(191, 191, 191), edgeGroups = groups.keys())
# out = out.resize((out.size[0] * scale, out.size[1] * scale), Image.NEAREST)

# unfortunately lakes don't have unitstacks.txt
provinceMap.overlayText(out, groups, fontfile = "tahoma.ttf", fontsize = 9, antialias = False)
out.save('out/building_slot_map.png')
#pyradox.image.saveUsingPalette(out, 'out/province_ID_map.png')
