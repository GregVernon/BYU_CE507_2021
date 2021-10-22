abaqusDirectory = "C:/Users/Owner/Documents/AbaqusTemp/"

odb = session.odbs[abaqusDirectory + "Resonant_Plate_Dynamic.odb"]

hKeys = odb.steps['Impact'].historyRegions.keys()
for key in hKeys:
    histRegion = odb.steps['Impact'].historyRegions[key]
    isSetData = False
    if histRegion.point.region == None:
        pass
    else:
        setName = histRegion.point.region.name
        if setName == "PROBE_X0_Y0":
            histKey = key

histRegion = odb.steps['Impact'].historyRegions[histKey]

histData = histRegion.historyOutputs['U3'].data
filename = abaqusDirectory + "displacement.csv"
f = open(filename,"w+")
f.write("time,displacement" + "\n")
for val in histData:
    f.write(str(val[0]) + "," + str(val[1]) + "\n")

f.close()

histData = histRegion.historyOutputs['V3'].data
filename = abaqusDirectory + "velocity.csv"
f = open(filename,"w+")
f.write("time,velocity" + "\n")
for val in histData:
    f.write(str(val[0]) + "," + str(val[1]) + "\n")

f.close()

histData = histRegion.historyOutputs['A3'].data
filename = abaqusDirectory + "acceleration.csv"
f = open(filename,"w+")
f.write("time,acceleration" + "\n")
for val in histData:
    f.write(str(val[0]) + "," + str(val[1]) + "\n")

f.close()

