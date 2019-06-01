import matplotlib
import matplotlib.pyplot as plt

T1s = [(x + 1) for x in range(10)]
T2s = [(x + 1) for x in range(10)]
ro_fidelities = [(x + 1)/1000.0 for x in range(1000)]

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

plotT1AndT2()
