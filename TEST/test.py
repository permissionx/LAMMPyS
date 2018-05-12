import LAMMPyS as lp
steps = lp.Steps('test.dump')
step = steps[-1]
atoms = step.atoms