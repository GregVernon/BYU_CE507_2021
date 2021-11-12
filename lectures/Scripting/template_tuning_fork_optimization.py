from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
from abaqusConstants import *

session.journalOptions.setValues(INDEX)

def initializeInputs( ):
    designVariables = {}
    designVariables[ "crossSectionWidth"] = 5.0
    designVariables[ "stemLength" ] = 40.0
    designVariables[ "forkLength" ] = 100.0
    jobSettings = {}
    jobSettings[ "jobName" ] = "TuningFork_Eigen"
    jobSettings[ "odbPath" ] = "C:/Users/greg/Documents/AbaqusTemp/"
    return designVariables, jobSettings

def bisection_method(targetFrequency, lowerBound, upperBound, maxIter, tolerance ):
    designVariables, jobSettings = initializeInputs()
    designVariables[ "forkLength" ] = lowerBound
    lowerObjective = evaluate_objective_function( designVariables, jobSettings )
    designVariables[ "forkLength" ] = upperBound
    upperObjective = evaluate_objective_function( designVariables, jobSettings )
    for iter in range( 0, maxIter ):
        ## Compute current guess & current objective
        currentGuess = ( lowerBound + upperBound ) / 2.0
        designVariables[ "forkLength" ] = currentGuess
        currentFrequency = evaluate_objective_function( designVariables, jobSettings )
        currentObjective = targetFrequency - currentFrequency
        print "Iteration = " + str( iter + 1 ) 
        print "\t Current Guess = " + str( currentGuess )
        print "\t Frequency = " + str( currentFrequency )
        print "\t Error = " + str( currentObjective )
        if currentObjective < 0:
            lowerBound = currentGuess
        elif currentObjective > 0:
            upperBound = currentGuess
        ## Check for convergence
        if abs(currentObjective) <= tolerance:
            print "Objective function has converged!"
            break
        if ( upperBound - lowerBound ) < tolerance:
            print "Search space has converged!"
            break
    return currentGuess, currentFrequency

def evaluate_objective_function(designVariables, jobSettings):
    create_geometry( designVariables["crossSectionWidth"], designVariables["stemLength"], designVariables["forkLength"] )
    create_materials( )
    create_assembly( )
    create_step( )
    create_boundary_conditions( )
    partition_geometry_for_mesh( )
    generate_mesh( designVariables["crossSectionWidth"] )
    submit_job( jobSettings["jobName"] )
    frequency = extract_frequency( jobSettings["odbPath"], jobSettings["jobName"])
    return frequency

def create_geometry( crossSectionWidth=5, stemLength=40, forkLength=100 ):
    ## Create the STEM
    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(-crossSectionWidth/2.0, -crossSectionWidth/2.0), point2=(crossSectionWidth/2.0, crossSectionWidth/2.0))
    mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Tuning_Fork', type=DEFORMABLE_BODY)
    mdb.models['Model-1'].parts['Tuning_Fork'].BaseSolidExtrude(depth=stemLength, sketch=mdb.models['Model-1'].sketches['__profile__'])
    del mdb.models['Model-1'].sketches['__profile__']
    ## Create the CROSS BEAM
    mdb.models['Model-1'].ConstrainedSketch(gridSpacing=2.03, name='__profile__', sheetSize=81.24, transform=mdb.models['Model-1'].parts['Tuning_Fork'].MakeSketchTransform(sketchPlane=mdb.models['Model-1'].parts['Tuning_Fork'].faces[4], sketchPlaneSide=SIDE1, sketchUpEdge=mdb.models['Model-1'].parts['Tuning_Fork'].edges[0],sketchOrientation=RIGHT, origin=(0.0, 0.0, stemLength)))
    mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(-(3.0/2.0)*crossSectionWidth, -(1.0/2.0)*crossSectionWidth), point2=((3.0/2.0)*crossSectionWidth, (1.0/2.0)*crossSectionWidth))
    mdb.models['Model-1'].parts['Tuning_Fork'].SolidExtrude(depth=crossSectionWidth, flipExtrudeDirection=OFF, sketch=mdb.models['Model-1'].sketches['__profile__'], sketchOrientation=RIGHT, sketchPlane=mdb.models['Model-1'].parts['Tuning_Fork'].faces[4], sketchPlaneSide=SIDE1, sketchUpEdge=mdb.models['Model-1'].parts['Tuning_Fork'].edges[0])
    del mdb.models['Model-1'].sketches['__profile__']
    ## Create the FORKS
    mdb.models['Model-1'].ConstrainedSketch(gridSpacing=0.82, name='__profile__', sheetSize=33.16, transform=mdb.models['Model-1'].parts['Tuning_Fork'].MakeSketchTransform(sketchPlane=mdb.models['Model-1'].parts['Tuning_Fork'].faces[4], sketchPlaneSide=SIDE1, sketchUpEdge=mdb.models['Model-1'].parts['Tuning_Fork'].edges[8], sketchOrientation=RIGHT, origin=(0.0, 0.0, stemLength + crossSectionWidth)))
    mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(-(3.0/2.0)*crossSectionWidth, -(1.0/2.0)*crossSectionWidth), point2=(-(1.0/2.0)*crossSectionWidth, (1.0/2.0)*crossSectionWidth))
    mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(+(3.0/2.0)*crossSectionWidth, -(1.0/2.0)*crossSectionWidth), point2=(+(1.0/2.0)*crossSectionWidth, (1.0/2.0)*crossSectionWidth))
    mdb.models['Model-1'].parts['Tuning_Fork'].SolidExtrude(depth=forkLength, flipExtrudeDirection=OFF, sketch=mdb.models['Model-1'].sketches['__profile__'], sketchOrientation=RIGHT, sketchPlane=mdb.models['Model-1'].parts['Tuning_Fork'].faces[4], sketchPlaneSide=SIDE1, sketchUpEdge=mdb.models['Model-1'].parts['Tuning_Fork'].edges[8])
    del mdb.models['Model-1'].sketches['__profile__']
    ## Assign "WholePart" set
    mdb.models['Model-1'].parts['Tuning_Fork'].Set(cells=mdb.models['Model-1'].parts['Tuning_Fork'].cells.getSequenceFromMask(('[#1 ]', ), ), name='WholePart')
    ## Decompose for Boundary Conditions
    mdb.models['Model-1'].parts['Tuning_Fork'].DatumPlaneByPrincipalPlane(offset=stemLength, principalPlane=XYPLANE)
    mdb.models['Model-1'].parts['Tuning_Fork'].PartitionCellByDatumPlane(cells=mdb.models['Model-1'].parts['Tuning_Fork'].cells.getSequenceFromMask(mask=('[#1 ]', ), ), datumPlane=
    mdb.models['Model-1'].parts['Tuning_Fork'].datums[5])
    mdb.models['Model-1'].parts['Tuning_Fork'].Set(cells=mdb.models['Model-1'].parts['Tuning_Fork'].cells.getSequenceFromMask(mask=('[#2 ]', ), ), name='HoldStem')
    mdb.models['Model-1'].parts['Tuning_Fork'].Set(faces=mdb.models['Model-1'].parts['Tuning_Fork'].faces.getSequenceFromMask(mask=('[#2002 ]', ), ), name='YMax')
    mdb.models['Model-1'].parts['Tuning_Fork'].Set(faces=mdb.models['Model-1'].parts['Tuning_Fork'].faces.getSequenceFromMask(mask=('[#8004 ]', ), ), name='YMin')

def create_materials( massDensity=0.0072, youngsModulus=82e9, poissonRatio=0.28 ):
    ## CREATE MATERIAL
    ## Create / Assign Section
    
def create_assembly( ):
    ## CREATE ASSEMBLY

def create_step( ):
    ## CREATE STEP

def create_boundary_conditions( ):
    ## ASSIGN BOUNDARY CONDITIONS

def partition_geometry_for_mesh( ):
    mdb.models['Model-1'].parts['Tuning_Fork'].PartitionCellByExtendFace(cells=mdb.models['Model-1'].parts['Tuning_Fork'].cells.getSequenceFromMask(mask=('[#1 ]', ), ), extendFace=mdb.models['Model-1'].parts['Tuning_Fork'].faces[11])
    mdb.models['Model-1'].parts['Tuning_Fork'].PartitionCellByPlanePointNormal(cells=mdb.models['Model-1'].parts['Tuning_Fork'].cells.getSequenceFromMask(mask=('[#4 ]', ), ), normal=mdb.models['Model-1'].parts['Tuning_Fork'].edges[14], point=mdb.models['Model-1'].parts['Tuning_Fork'].vertices[4])
    mdb.models['Model-1'].parts['Tuning_Fork'].PartitionCellByPlanePointNormal(cells=mdb.models['Model-1'].parts['Tuning_Fork'].cells.getSequenceFromMask(mask=('[#8 ]', ), ), normal=mdb.models['Model-1'].parts['Tuning_Fork'].edges[23], point=mdb.models['Model-1'].parts['Tuning_Fork'].vertices[10])

def generate_mesh( meshSize=5.0 ):
    mdb.models['Model-1'].parts['Tuning_Fork'].deleteMesh()
    mdb.models['Model-1'].parts['Tuning_Fork'].seedPart(deviationFactor=0.1, minSizeFactor=0.1, size=meshSize)
    mdb.models['Model-1'].parts['Tuning_Fork'].setElementType(elemTypes=(ElemType(elemCode=C3D20, elemLibrary=STANDARD), ElemType(elemCode=C3D15, elemLibrary=STANDARD), ElemType(elemCode=C3D10, elemLibrary=STANDARD)), regions=(mdb.models['Model-1'].parts['Tuning_Fork'].cells.getSequenceFromMask(mask=('[#3f ]', ), ), ))
    mdb.models['Model-1'].parts['Tuning_Fork'].generateMesh()

def submit_job( jobName="TuningFork_Eigen"):
    mdb.models['Model-1'].rootAssembly.regenerate()
    mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, name=jobName, nodalOutputPrecision=SINGLE, queue=None, resultsFormat=ODB, scratch='', type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
    mdb.jobs[jobName].submit(consistencyChecking=OFF)
    mdb.jobs[jobName].waitForCompletion()

def extract_frequency(odbPath, odbName="TuningFork_Eigen"):
    odbName = odbPath + odbName + ".odb"
    session.openOdb(odbName)
    odb = session.odbs[odbName]
    ## Write a routine that gets the desired mode number from the history data 
    # (i.e. lowest mode with (near) zero effective mass in x-component, and significant participation factor in x-component
    modeNumber = ...?
    frequency = odb.steps['Step-1'].frames[modeNumber].frequency
    odb.close()
    return frequency


if __name__ == "__main__":
    mdb.close()
    targetFrequency = 440.0
    lowerBound = 20.0
    upperBound = 100.0
    maxIter = 10
    tolerance = 1e-4
    bisection_method(targetFrequency, lowerBound, upperBound, maxIter, tolerance )

