import secret_sharing as ss

T1s = [(x + 1) * 1e-06 for x in range(10)]
T2s = [(x + 1) * 1e-06 for x in range(10)]
ro_fidelities = [(x + 1)/1000.0 for x in range(1000)]
# from the pyquil defaults
default_T1 = 5e-06
#default_T1 = 3e-05
default_T2 = 5e-06
#default_T2 = 3e-05
default_ro_fidelity = 0.95

def collectT1AndT2():
    data = []
    for i in range(len(T1s)):
        data.append(ss.runExperiments(T1s[i], T2s[i], default_ro_fidelity))
    with open("out/T1_T2", "w") as f:
        for num in data:
            f.write('%d\n' % num)

def collectT1():
    data = []
    for T1 in T1s:
        data.append(ss.runExperiments(T1, default_T2, default_ro_fidelity))
    with open("out/T1", "w") as f:
        for num in data:
            f.write('%d\n' % num)

def collectT2():
    data = []
    for T2 in T2s:
        data.append(ss.runExperiments(default_T1, T2, default_ro_fidelity))
    with open("out/T2", "w") as f:
        for num in data:
            f.write("%d\n" % num)

def collectROFidelity():
    data = []
    for ro_fidelity in ro_fidelities:
        data.append(ss.runExperiments(default_T1, default_T2, ro_fidelity))
    with open("out/RO", "w") as f:
        for num in data:
            f.write("%d\n" % num)


collectT1AndT2()
