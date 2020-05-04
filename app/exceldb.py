# import arcpy
# import sys, os
# import numpy
# import pandas as pd
#
# ws = r'myworkspace.sde'
# fcname = r'MyFeatureClass'
# input_fc = os.path.join(ws, fcname)
#
# #create the numpy array
# narr = arcpy.da.FeatureClassToNumPyArray(input_fc, ("Field1", "Field2", "Field3"))
#
# #I prefer to use pandas to export from.  personal preference is all
# df = pd.DataFrame(narr)
# df.to_csv('H:\somefolder\dfoutput.csv', header=None)