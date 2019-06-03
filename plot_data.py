import matplotlib
import matplotlib.pyplot as plt
import brewer2mpl

T1s = [(x/10.0 + 1) * 3 for x in range(100)]
T2s = [(x/10.0 + 1) * 3 for x in range(100)]
ro_fidelities = [(x + 1) for x in range(100)]
q1times = [(x + 5) * 10 for x in range(100)]
q2times = [(x + 1) / 10.0 for x in range(100)]

default_T1 = 30
default_T2 = 30
default_ro_fidelity = 95
default_q1time = 50
default_q2time = 0.15

bmap1 = brewer2mpl.get_map('Set1', 'Qualitative', 7)
bmap2 = brewer2mpl.get_map('Dark2', 'Qualitative', 7)
hash_colors = bmap1.mpl_colors
mix_colors = bmap2.mpl_colors

def getDefault():
    with open("out/default", "r") as f:
        lines = f.readlines()
        return int(lines[0]) / 10.0

def plotT1AndT2():
    y = []
    with open("out/T1_T2", "r") as f:
        lines = f.readlines()
        for line in lines:
            y.append(int(line) / 10.0)

    default = getDefault()

    plt.scatter(T1s, y, color=mix_colors[1])
    plt.scatter([default_T1], [default], marker='*', color=mix_colors[0], s=400)
    plt.title("Effect of T1 and T2 Values on Failure Rate")
    plt.xlabel("T1 and T2 values (us)")
    plt.ylabel("Failure rate (%)")
    plt.xticks([(x * 5) for x in range(7)])
    plt.savefig("figs/T1_T2")
    plt.clf()

def plotROFidelity():
    y = []
    with open("out/RO", "r") as f:
        lines = f.readlines()
        for line in lines:
            y.append(int(line) / 10.0)

    default = 0
    with open("out/default_ro", "r") as f:
        lines = f.readlines()
        default = int(lines[0]) / 10.0


    plt.scatter(ro_fidelities, y, color=mix_colors[2])
    plt.scatter([default_ro_fidelity], [default], marker='*', color=mix_colors[0], s=400)
    plt.title("Effect of Readout-Fidelity on Failure Rate")
    plt.xlabel("Readout fidelity (%)")
    plt.ylabel("Failure rate (%)")
    plt.xticks([(x) * 10 for x in range(11)])
    plt.savefig("figs/RO")
    plt.clf()

def plotQ1Times():
    y = []
    with open("out/Q1", "r") as f:
        lines = f.readlines()
        for line in lines:
            y.append(int(line) / 10.0)
    default = getDefault()

    plt.scatter(q1times, y, color=mix_colors[5])
    plt.scatter([default_q1time], [default], marker='*', color=mix_colors[0], s=400)
    plt.title("Effect of 1-qubit Gate Times on Failure Rate")
    plt.xlabel("1-qubit Gate Times (ns)")
    plt.ylabel("Failure rate (%)")
    plt.xticks([x * 100 for x in range(11)])
    plt.savefig("figs/Q1")
    plt.clf()

def plotQ2Times():
    y = []
    with open("out/Q2", "r") as f:
        lines = f.readlines()
        for line in lines:
            y.append(int(line) / 10.0)
    default = getDefault()

    plt.scatter(q2times, y, color=mix_colors[3])
    plt.scatter([default_q2time], [default], color=mix_colors[0], marker='*', s=400)
    plt.title("Effect of 2-qubit Gate Times on Failure Rate")
    plt.xlabel("2-qubit Gate Times (us)")
    plt.ylabel("Failure rate (%)")
    plt.xticks(range(11))
    plt.savefig("figs/Q2")
    plt.clf()

font = {'size': 14}
matplotlib.rc('font', **font)
plotT1AndT2()
plotROFidelity()
plotQ1Times()
plotQ2Times()
