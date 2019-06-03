import secret_sharing as ss

T1s = [(x/10.0 + 1) * 3e-06 for x in range(100)]
T2s = [(x/10.0 + 1) * 3e-06 for x in range(100)]
ro_fidelities = [(x + 1)/100.0 for x in range(100)]
q1times = [(x + 5) * 1e-08 for x in range(100)]
q2times = [(x + 1) * 1e-07 for x in range(100)]
# from the pyquil defaults
default_T1 = 3e-05
default_T2 = 3e-05
default_ro_fidelity = 1.0 
default_q1time = 5e-08
default_q2time = 1.5e-07

def collectT1AndT2():
    data = []
    for i in range(len(T1s)):
        data.append(ss.runExperiments(T1s[i], T2s[i], default_ro_fidelity, default_q1time, default_q2time))
    with open("out/T1_T2", "w") as f:
        for num in data:
            f.write('%d\n' % num)

def collectT1():
    data = []
    for T1 in T1s:
        data.append(ss.runExperiments(T1, default_T2, default_ro_fidelity, default_q1time, default_q2time))
    with open("out/T1", "w") as f:
        for num in data:
            f.write('%d\n' % num)

def collectT2():
    data = []
    for T2 in T2s:
        data.append(ss.runExperiments(default_T1, T2, default_ro_fidelity, default_q1time, default_q2time))
    with open("out/T2", "w") as f:
        for num in data:
            f.write("%d\n" % num)

def collectROFidelity():
    data = []
    for ro_fidelity in ro_fidelities:
        data.append(ss.runExperiments(default_T1, default_T2, ro_fidelity, default_q1time, default_q2time))
    with open("out/RO", "w") as f:
        for num in data:
            f.write("%d\n" % num)

def collectQ1Times():
    data = []
    for q1time in q1times:
        data.append(ss.runExperiments(default_T1, default_T2, default_ro_fidelity, q1time, default_q2time))
    with open("out/q1", "w") as f:
        for num in data:
            f.write("%d\n" % num)

def collectQ2Times():
    data = []
    for q2time in q2times:
        data.append(ss.runExperiments(default_T1, default_T2, default_ro_fidelity, default_q1time, q2time))
    with open("out/q2", "w") as f:
        for num in data:
            f.write("%d\n" % num)

def collectDefault():
    data = ss.runExperiments(default_T1, default_T2, default_ro_fidelity, default_q1time, default_q2time)
    with open("out/default", "w") as f:
        f.write("%d\n" % data)

def collectRoDefault():
    data = ss.runExperiments(default_T1, default_T2, 0.95, default_q1time, default_q2time)
    with open("out/default_ro", "w") as f:
        f.write("%d\n" % data)


collectRoDefault()
collectDefault()
collectQ2Times()
collectQ1Times()
collectT1AndT2()
collectROFidelity()
