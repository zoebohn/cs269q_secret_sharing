import matplotlib
import matplotlib.pyplot as plt

T1s = [(x + 1) for x in range(10)]
T2s = [(x + 1) for x in range(10)]
ro_fidelities = [(x + 1)/10.0 for x in range(1000)]

def plotT1AndT2():
    y = []
    with open("out/T1_T2", "r") as f:
        lines = f.readlines()
        for line in lines:
            y.append(int(line))

    plt.scatter(T1s, y)
    plt.title("Failure Rate of Quantum Secret Sharing with Noise")
    plt.xlabel("T1 and T2 values (us)")
    plt.ylabel("Number of failures over 1,000 trials")
    plt.xticks(T1s)
    plt.savefig("figs/T1_T2")
    plt.clf()

def plotROFidelity():
    y = []
    with open("out/RO", "r") as f:
        lines = f.readlines()
        for line in lines:
            y.append(int(line))

    plt.scatter(ro_fidelities, y)
    plt.title("Failure Rate of Quantum Secret Sharing with Noise (Read-out fidelity)")
    plt.xlabel("Readout Fidelity (%)")
    plt.ylabel("Number of failures over 1,000 trials")
    plt.xticks([(x + 1) * 10 for x in range(10)])
    plt.savefig("figs/RO")
    plt.clf()

plotT1AndT2()
plotROFidelity()