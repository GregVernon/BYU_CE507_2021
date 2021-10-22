import numpy

def monte_carlo():
    num_samples = 100
    radius, stiffness, poisson = initialize_monte_carlo(num_samples)
    max_mises = numpy.zeros(num_samples, dtype="double")
    for i in range(0,num_samples):
        print("Iteration: " + str(i+1) + " / " + str(num_samples) + "\n")
        update_model(radius[i], stiffness[i], poisson[i])
        submit_job()
        max_mises[i] = get_results()
    write_results(radius, stiffness, poisson, max_mises)

def write_results(radius, stiffness, poisson, max_mises):
    f = open("C://Users/Owner/Documents/AbaqusTemp/PWH_monte_carlo_results.csv" ,"w+")
    f.write("radius,stiffness,poisson,max_mises" + "\n")
    for i in range(0,len(radius)):
        f.write(",".join([str(radius[i]), str(stiffness[i]), str(poisson[i]), str(max_mises[i])]) + "\n")
    f.close()

def get_results():
    odb = session.openOdb("C://Users/Owner/Documents/AbaqusTemp/PWH_monte_carlo.odb")
    values = odb.steps['Step-1'].frames[-1].fieldOutputs['S'].values
    max_mises = -float("inf")
    for i in range(0,len(values)):
        if values[i].mises > max_mises:
            max_mises = values[i].mises
    odb.close()
    return max_mises

def submit_job():
    mdb.jobs['PWH_monte_carlo'].submit(consistencyChecking=OFF)
    mdb.jobs['PWH_monte_carlo'].waitForCompletion()

def update_model(radius, stiffness, poisson):
    update_material(stiffness, poisson)
    update_geometry(radius)
    update_mesh()

def update_material(stiffness, poisson):
    mdb.models['PWH_Implicit_Static-H3'].materials['Material-1'].elastic.setValues(table=((stiffness, poisson), ))

def update_geometry(radius):
    mdb.models['PWH_Implicit_Static-H3'].ConstrainedSketch(name='__edit__', objectToCopy=mdb.models['PWH_Implicit_Static-H3'].parts['Part-1'].features['Shell planar-1'].sketch)
    mdb.models['PWH_Implicit_Static-H3'].sketches['__edit__'].parameters['radius'].setValues(expression=str(radius))
    mdb.models['PWH_Implicit_Static-H3'].parts['Part-1'].features['Shell planar-1'].setValues(sketch=mdb.models['PWH_Implicit_Static-H3'].sketches['__edit__'])
    del mdb.models['PWH_Implicit_Static-H3'].sketches['__edit__']
    mdb.models['PWH_Implicit_Static-H3'].parts['Part-1'].regenerate()

def update_mesh():
    mdb.models['PWH_Implicit_Static-H3'].parts['Part-1'].generateMesh()
    mdb.models['PWH_Implicit_Static-H3'].rootAssembly.regenerate()

def initialize_monte_carlo(num_samples):
    radius = initialize_radius(num_samples)
    stiffness = initialize_stiffness(num_samples)
    poisson = initialize_poisson(num_samples)
    return radius, stiffness, poisson

def initialize_radius(num_samples):
    radius = numpy.zeros(num_samples)
    r_mean = 1.0
    r_min = r_mean - 0.1
    r_max = r_mean + 0.1
    r_std = 0.01
    for i in range(0,num_samples):
      isValid = False
      while isValid == False:
        r_rand = numpy.random.normal(r_mean, r_std)
        if r_rand < r_max and r_rand > r_min:
            isValid = True
            radius[i] = r_rand
    return radius

def initialize_stiffness(num_samples):
    stiffness = numpy.zeros(num_samples)
    k_mean = 29e6
    k_min = k_mean - 5e6
    k_max = k_mean + 5e6
    k_std = 1e6
    for i in range(0,num_samples):
      isValid = False
      while isValid == False:
        k_rand = numpy.random.normal(k_mean, k_std)
        if k_rand < k_max and k_rand > k_min:
            isValid = True
            stiffness[i] = k_rand
    return stiffness

def initialize_poisson(num_samples):
    poisson = numpy.zeros(num_samples)
    p_mean = 0.25
    p_min = 0.2
    p_max = 0.33
    p_std = 0.1
    for i in range(0,num_samples):
      isValid = False
      while isValid == False:
        p_rand = numpy.random.normal(p_mean, p_std)
        if p_rand < p_max and p_rand > p_min:
            isValid = True
            poisson[i] = p_rand
    return poisson



