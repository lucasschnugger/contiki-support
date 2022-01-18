import csv
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
from pylab import plot, show, savefig, xlim, figure, ylim, legend, boxplot, setp, axes
from radar_factory import radar_factory


class Test:

    def __init__(self, row):
        self.seed = int(row['seed']) if 'seed' in row.keys() and row['seed'] != '' else None
        self.nodes = int(row['nodes']) if 'nodes' in row.keys() and row['nodes'] != '' else None
        self.hop_seq = int(row['hop_seq']) if 'hop_seq' in row.keys() and row['hop_seq'] != '' else None
        self.topology = row['topology'] if 'topology' in row.keys() and row['topology'] != '' else None
        self.tsch_ver = row['tsch_ver'] if 'tsch_ver' in row.keys() and row['tsch_ver'] != '' else None
        self.timeout = int(row['timeout']) if 'timeout' in row.keys() and row['timeout'] != '' else None
        self.net_est = float(row['net_est']) if 'net_est' in row.keys() and row['net_est'] != '' else None
        self.eb_first_time = float(row['eb_first_time']) if 'eb_first_time' in row.keys() and row['eb_first_time'] != '' else None
        self.join_time = float(row['join_time']) if 'join_time' in row.keys() and row['join_time'] != '' else None
        self.found_nodes = int(row['found_nodes']) if 'found_nodes' in row.keys() and row['found_nodes'] != '' else None
        self.assoc_by_timeout = bool(row['assoc_by_timeout']) if 'assoc_by_timeout' in row.keys() and row['assoc_by_timeout'] != '' else None
        self.power_time = float(row['pw_time']) if 'pw_time' in row.keys() and row['pw_time'] != '' else None
        self.radio_on_time = float(row['radio_on_time']) if 'radio_on_time' in row.keys() and row['radio_on_time'] != '' else None
        self.radio_on_pct = float(row['radio_on_pct']) if 'radio_on_pct' in row.keys() and row['radio_on_pct'] != '' else None
        self.radio_tx_time = float(row['radio_tx_time']) if 'radio_tx_time' in row.keys() and row['radio_tx_time'] != '' else None
        self.radio_tx_pct = float(row['radio_tx_pct']) if 'radio_tx_pct' in row.keys() and row['radio_tx_pct'] != '' else None
        self.radio_rx_time = float(row['radio_rx_time']) if 'radio_rx_time' in row.keys() and row['radio_rx_time'] != '' else None
        self.radio_rx_pct = float(row['radio_rx_pct']) if 'radio_rx_pct' in row.keys() and row['radio_rx_pct'] != '' else None
        self.radio_int_time = float(row['radio_int_time']) if 'radio_int_time' in row.keys() and row['radio_int_time'] != '' else None
        self.radio_int_pct = float(row['radio_int_pct']) if 'radio_int_pct' in row.keys() and row['radio_int_pct'] != '' else None
        self.rejoin_time = float(row['rejoin_time']) if 'rejoin_time' in row.keys() and row['rejoin_time'] != '' else None
        self.rejoin_duration = float(row['rejoin_duration']) if 'rejoin_duration' in row.keys() and row['rejoin_duration'] != '' else None
        self.rows = []

    def add_row(self, row):
        self.rows.append(row)

    def different_test(self, row):
        compare_test = Test(row)
        if(self.nodes != compare_test.nodes):
            return True
        if(self.topology != compare_test.topology):
            return True
        if(self.tsch_ver != compare_test.tsch_ver):
            return True
        if(self.timeout != compare_test.timeout):
            return True
        if(self.hop_seq != compare_test.hop_seq):
            return True
        return False


def generate_bar_compare_custom_and_classic_jointime_after_first_EB(tests, title, ax):
    custom_parents_considered = [np.mean([float(i['join_time'])-float(i['eb_first_time']) for i in o.rows]) for o in tests if o.tsch_ver == "custom"]
    classic_parent_considered = [np.mean([float(i['join_time'])-float(i['eb_first_time']) for i in o.rows]) for o in tests if o.tsch_ver == "classic"]
    custom_parents_considered = np.round(custom_parents_considered, 1)
    classic_parent_considered = np.round(classic_parent_considered, 1)

    x = np.arange(len(custom_parents_considered))
    labels = [o.nodes-1 for o in tests if o.tsch_ver == "custom"]

    width = 0.2
    cust_bar = ax.bar(x-width/2, custom_parents_considered, width, label="Custom")
    clas_bar = ax.bar(x+width/2, classic_parent_considered, width, label="Classic")

    ax.set_xlabel('Possible parents')
    ax.set_ylabel('Join time (s)')
    ax.set_ylim([0, max(classic_parent_considered)*1.3])
    ax.set_xticks(x, labels)
    ax.set_title(title)
    ax.legend()

    ax.bar_label(cust_bar, padding=3)
    ax.bar_label(clas_bar, padding=3)


def generate_bar_compare_custom_and_classic_jointime(tests, title, ax):
    custom_parents_considered = [np.mean([float(i['join_time'])-180 for i in o.rows]) for o in tests if o.tsch_ver == "custom"]
    classic_parent_considered = [np.mean([float(i['join_time'])-180 for i in o.rows]) for o in tests if o.tsch_ver == "classic"]

    custom_first_eb_time = [np.mean([float(i['eb_first_time'])-180 for i in o.rows]) for o in tests if o.tsch_ver == "custom"]
    classic_first_eb_time = [np.mean([float(i['eb_first_time'])-180 for i in o.rows]) for o in tests if o.tsch_ver == "classic"]

    custom_parents_considered = np.round(custom_parents_considered, 1)
    classic_parent_considered = np.round(classic_parent_considered, 1)

    custom_first_eb_time = np.round(custom_first_eb_time, 1)
    classic_first_eb_time = np.round(classic_first_eb_time, 1)

    x = np.arange(len(custom_parents_considered))
    labels = [o.nodes-1 for o in tests if o.tsch_ver == "custom"]

    width = 0.2
    cust_bar = ax.bar(x-width/2, custom_parents_considered, width, label="Custom v. join", edgecolor="white")
    clas_bar = ax.bar(x+width/2, classic_parent_considered, width, label="Classic v. join", edgecolor="white")
    cust_feb_bar = ax.bar(x-width/2, custom_first_eb_time, width, label="First EB", color="dimgray", edgecolor="white")
    clas_feb_bar = ax.bar(x+width/2, classic_first_eb_time, width, color="dimgray", edgecolor="white", tick_label="test")

    ax.set_xlabel('Possible parents')
    ax.set_ylabel('Time (s)')
    ax.set_ylim([0, max(classic_parent_considered)*1.3])

    ax.set_xticks(x, labels)
    ax.set_title(title)
    ax.legend()

    autolabel(cust_feb_bar)
    autolabel(clas_feb_bar)

    ax.bar_label(cust_bar, padding=3)
    ax.bar_label(clas_bar, padding=3)

    #ax.bar_label(cust_feb_bar, padding=3)
    #ax.bar_label(clas_feb_bar, padding=3)

def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2.,height-10,
                '%.1f' % float(height),
                ha='center', va='bottom', color='white')

def generate_line_compare_custom_and_classic_jointime(tests, title, ax):
    custom_parents_considered = [np.mean([float(i['join_time'])-180 for i in o.rows]) for o in tests if o.tsch_ver == "custom"]
    classic_parent_considered = [np.mean([float(i['join_time'])-180 for i in o.rows]) for o in tests if o.tsch_ver == "classic"]
    custom_parents_considered = np.round(custom_parents_considered, 1)
    classic_parent_considered = np.round(classic_parent_considered, 1)

    x = np.arange(len(custom_parents_considered))
    labels = [o.nodes-1 for o in tests if o.tsch_ver == "custom"]

    ax.plot(x, custom_parents_considered, label="Custom")
    ax.plot(x, classic_parent_considered, label="Classic")

    ax.set_xlabel('Possible parents')
    ax.set_ylabel('Join time (s)')
    ax.set_ylim([0, max(classic_parent_considered) * 1.3])
    ax.set_xticks(x, labels)
    ax.set_title(title)
    ax.legend()


def set_box_color(bp, color):
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['caps'], color=color)
    plt.setp(bp['medians'], color=color)

def generate_box_compare_custom_and_classic_jointime(tests, title, ax):
    custom_parents_considered = [[float(i['join_time']) - 180 for i in o.rows] for o in tests if o.tsch_ver == "custom"]
    classic_parent_considered = [[float(i['join_time']) - 180 for i in o.rows] for o in tests if o.tsch_ver == "classic"]
    custom_parents_considered = np.round(custom_parents_considered, 1)
    classic_parent_considered = np.round(classic_parent_considered, 1)

    inv_cus = custom_parents_considered.tolist()
    inv_clas = classic_parent_considered.tolist()

    x = np.arange(len(classic_parent_considered))
    labels = [o.nodes - 1 for o in tests if o.tsch_ver == "custom"]

    bpl_pos = np.array(range(len(inv_cus))) * 2.0 - 0.22
    bpr_pos = np.array(range(len(inv_clas))) * 2.0 + 0.22
    bpl = plt.boxplot(inv_cus, positions=bpl_pos, sym='', widths=0.4)
    bpr = plt.boxplot(inv_clas, positions=bpr_pos, sym='', widths=0.4)
    set_box_color(bpl, 'tab:blue')
    set_box_color(bpr, 'tab:orange')

    # draw temporary red and blue lines and use them to create a legend
    plt.plot([], c='tab:blue', label='Custom')
    plt.plot([], c='tab:orange', label='Classic')

    ax.set_xlabel('Possible parents')
    ax.set_ylabel('Join time (s)')

    plt.legend()

    plt.xticks(range(0, len(labels) * 2, 2), labels)
    plt.xlim(-2, len(labels) * 2)
    plt.ylim(0, 450)
    plt.tight_layout()

def generate_bar_compare_custom_and_classic_timeout(tests, title, ax):
    custom_parents_considered = [np.mean([int(i['found_nodes']) for i in o.rows]) for o in tests if o.tsch_ver == "custom"]
    classic_parent_considered = [np.mean([int(i['found_nodes']) for i in o.rows]) for o in tests if o.tsch_ver == "classic"]
    custom_parents_considered = np.round(custom_parents_considered, 1)
    classic_parent_considered = np.round(classic_parent_considered, 1)

    x = np.arange(len(custom_parents_considered))
    labels = [o.timeout for o in tests if o.tsch_ver == "custom"]

    width = 0.2
    cust_bar = ax.bar(x-width/2, custom_parents_considered, width, label="Custom")
    clas_bar = ax.bar(x+width/2, classic_parent_considered, width, label="Classic")

    ax.set_xlabel('Timeout (s)')
    ax.set_ylabel('Parents considered')
    ax.set_ylim([0, max(custom_parents_considered)*1.3])
    ax.set_xticks(x, labels)
    ax.set_title(title)
    ax.legend()

    ax.bar_label(cust_bar, padding=3)
    ax.bar_label(clas_bar, padding=3)


def generate_bar_compare_custom_and_classic_channel(tests, title, ax):
    tests.sort(key=lambda x: x.hop_seq)
    custom_parents_considered = [np.mean([int(i['found_nodes']) for i in o.rows]) for o in tests if o.tsch_ver == "custom"]
    classic_parent_considered = [np.mean([int(i['found_nodes']) for i in o.rows]) for o in tests if o.tsch_ver == "classic"]
    custom_parents_considered = np.round(custom_parents_considered, 1)
    classic_parent_considered = np.round(classic_parent_considered, 1)

    x = np.arange(len(custom_parents_considered))
    labels = [o.hop_seq for o in tests if o.tsch_ver == "custom"]

    width = 0.2
    cust_bar = ax.bar(x-width/2, custom_parents_considered, width, label="Custom")
    clas_bar = ax.bar(x+width/2, classic_parent_considered, width, label="Classic")

    ax.set_xlabel('Number of channels')
    ax.set_ylabel('Parents considered')
    ax.set_ylim([1, max(custom_parents_considered)*1.3])
    ax.set_xticks(x, labels)
    ax.set_title(title)
    ax.legend()

    ax.bar_label(cust_bar, padding=3)
    ax.bar_label(clas_bar, padding=3)

def generate_bar_compare_custom_and_classic_power_consumption(tests, title, ax):
    custom_parents_considered = [np.mean([float(i['pw_time'])*float(i['radio_on_pct'])/100 for i in o.rows]) for o in tests if o.tsch_ver == "custom"]
    classic_parent_considered = [np.mean([float(i['pw_time'])*float(i['radio_on_pct'])/100 for i in o.rows]) for o in tests if o.tsch_ver == "classic"]
    custom_parents_considered = np.round(custom_parents_considered, 1)
    classic_parent_considered = np.round(classic_parent_considered, 1)

    x = np.arange(len(custom_parents_considered))
    labels = [o.nodes-1 for o in tests if o.tsch_ver == "custom"]

    width = 0.2
    cust_bar = ax.bar(x-width/2, custom_parents_considered, width, label="Custom")
    clas_bar = ax.bar(x+width/2, classic_parent_considered, width, label="Classic")

    ax.set_xlabel('Possible parents')
    ax.set_ylabel('Radio ON time (s)')
    ax.set_ylim([0, max(classic_parent_considered)*1.3])
    ax.set_xticks(x, labels)
    ax.set_title(title)
    ax.legend()

    ax.bar_label(cust_bar, padding=3)
    ax.bar_label(clas_bar, padding=3)

def generate_radar_compare_solutions():
    N = 5 # properties in radar chart
    factory = radar_factory(N, frame="polygon")

    prop_labels = ['Versatility', 'Communication downtime', 'Data throughput', 'Energy efficiency', 'Feasibility']
    data = [
        ("", [
            # Values correspond to properties as indexed in prop_labels
            [2, 3, 5, 1, 3],  # EB Channel Prediction --> Scheduling
            [1, 4, 2, 5, 2],  # EB Channel Prediction --> Shorter Timeout Periods
            [3, 2, 4, 4, 1],  # 2D Triangulation
            [4, 5, 2, 3, 5],  # First Join then Evaluate
            [1, 3, 3, 3, 5]  # Fixed EB Broadcast Channel
        ])
    ]

    fig, ax = plt.subplots(figsize=(10,10), nrows=1, ncols=1, subplot_kw=dict(projection="radar"))
    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=5, bottom=0)
    colors = ['b', 'r', 'g', 'm', 'y']
    title = data[0][0]
    case_data = data[0][1]

    ax.set_rgrids([0, 1, 2, 3, 4, 5], angle=350)
    ax.set_title(title, weight="bold", size="medium", position=(0.5, 1.1), horizontalalignment="center", verticalalignment="center")
    for d, color in zip(case_data, colors):
        ax.plot(factory, d, color=color)
        ax.fill(factory, d, facecolor=color, alpha=0.10)
    ax.set_varlabels(prop_labels)

    # add legend
    legend_labels = (
        "EB Channel Prediction --> Scheduling",
        "EB Channel Prediction --> Shorter Timeout Periods",
        "2D Triangulation",
        "First Join then Evaluate",
        "Fixed EB Broadcast Channel"
    )
    legend = ax.legend(legend_labels, loc=(.65, .95), labelspacing=0.1, fontsize="small")

    fig.text(0.5, 0.965, 'Comparison of Solution qualities',
             horizontalalignment='center', color='black', weight='bold',
             size='large')

    plt.show()

def generate_radar_solutions():
    N = 5  # properties in radar chart
    factory = radar_factory(N, frame="polygon")

    prop_labels = ['Communication downtime', 'Versatility', 'Data throughput', 'Energy efficiency', 'Feasibility']
    data = [
        # Values correspond to properties as indexed in prop_labels
        ("EB Channel Prediction w/scheduling", [2, 3, 5, 1, 3]),
        ("EB Channel Prediction w/Shorter Timeout Periods", [1, 4, 2, 5, 2]),
        ("2D Triangulation", [3, 2, 4, 4, 1]),
        ("Join on 1st EB then Evaluate", [4, 5, 2, 3, 5]),
        ("Fixed EB Broadcast Channel", [1, 3, 3, 3, 5])
    ]

    fig, axs = plt.subplots(figsize=(10, 10), nrows=2, ncols=2, subplot_kw=dict(projection="radar"))
    fig.subplots_adjust(wspace=0.25, hspace=0.5, top=0.85, bottom=0.05)
    fig.delaxes(axs[2][1])
    colors = ['b', 'r', 'g', 'm', 'y']
    title = data[0][0]

    for index, ax in enumerate(axs.flat, start=0):
        if (index >= len(colors)):
            continue
        ax.set_ylim(0, 6.5)
        color = colors[index]
        title = data[index][0]
        sol_data = data[index][1]
        ax.set_rgrids([1, 2, 3, 4, 5], angle=0)
        ax.set_title(title, weight="bold", size="medium", position=(0.5, 1.1), horizontalalignment="center",
                     verticalalignment="center", fontdict={'color': color}, pad=15)
        ax.plot(factory, sol_data, color=color)
        ax.fill(factory, sol_data, facecolor=color, alpha=0.25)
        ax.set_varlabels(prop_labels)

    fig.text(0.5, 0.965, 'Comparison of solutions',
             horizontalalignment='center', color='black', weight='bold',
             size='x-large')

    plt.show()
    fig.savefig(f"plots/radar.svg", bbox_inches="tight")

def generate_bar_compare_custom_and_classic_rejoin():
    testsclassic = []
    testscustom = []
    with open("results/results-join-power.csv") as csv_file:
        csv_data = csv.DictReader(csv_file)
        current_test = 0
        for row in csv_data:
            if row['tsch_ver'] == "custom":
                continue
            if(current_test == 0 or current_test.different_test(row)):
                test = Test(row)
                testsclassic.append(test)
                current_test = test

            testsclassic[len(testsclassic) - 1].add_row(row)

    with open("results/rejoin-data.csv") as csv_file:
        csv_data = csv.DictReader(csv_file)
        current_test = 0
        for row in csv_data:
            if(current_test == 0 or current_test.different_test(row)):
                test = Test(row)
                testscustom.append(test)
                current_test = test

            testscustom[len(testscustom) - 1].add_row(row)

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 10))
    plt.suptitle("Comparison of average re-join time in networks with various possible parents", fontsize = 16)
    custom_parents_considered = [np.mean([float(i['rejoin_duration']) for i in o.rows]) for o in testscustom if o.tsch_ver == "rejoin"]
    classic_parent_considered = [np.mean([float(i['join_time'])-180 for i in o.rows]) for o in testsclassic if o.tsch_ver == "classic"]
    custom_parents_considered = np.round(custom_parents_considered, 1)
    classic_parent_considered = np.round(classic_parent_considered, 1)

    x = np.arange(len(custom_parents_considered))
    labels = [o.nodes-1 for o in tests if o.tsch_ver == "custom"]

    width = 0.2
    cust_bar = ax.bar(x-width/2, custom_parents_considered, width, label="Custom")
    clas_bar = ax.bar(x+width/2, classic_parent_considered, width, label="Classic")

    ax.set_xlabel('Possible parents')
    ax.set_ylabel('Time (s)')
    ax.set_ylim([0, max(classic_parent_considered)*1.3])
    ax.set_xticks(x, labels)
    ax.set_title("")
    ax.legend()

    ax.bar_label(cust_bar, padding=3)
    ax.bar_label(clas_bar, padding=3)
    plt.show()
    fig.savefig(f"plots/test.svg", bbox_inches="tight")


tests = []

with open("results/results-join-power.csv") as csv_file:
    csv_data = csv.DictReader(csv_file)
    current_test = 0
    for row in csv_data:
        if(current_test == 0 or current_test.different_test(row)):
            test = Test(row)
            tests.append(test)
            current_test = test

        tests[len(tests) - 1].add_row(row)

    # for test in tests:
    #     print("rows: " + str(len(test.rows))
    #           + ". nodes: " + test.nodes
    #           + ". topology: " + test.topology
    #           + ". tsch_version: " + test.tsch_ver
    #           + ". timeout: " + test.timeout)

    nodes_4_tests = [o for o in tests if int(o.nodes) == 4]
    nodes_5_tests = [o for o in tests if int(o.nodes) == 5]
    nodes_6_tests = [o for o in tests if int(o.nodes) == 6]
    nodes_7_tests = [o for o in tests if int(o.nodes) == 7]
    nodes_8_tests = [o for o in tests if int(o.nodes) == 8]
    nodes_9_tests = [o for o in tests if int(o.nodes) == 9]

    #fig, ax = plt.subplots(nrows=1, ncols=1,figsize=(20,10))
    #plt.suptitle("Comparison of average join time in networks with various possible parents including average first EB time", fontsize = 16)

    # generate_box_compare_custom_and_classic_jointime(tests, "", ax)
    #generate_box_compare_custom_and_classic_jointime(tests, "", ax)
    # generate_line_compare_custom_and_classic_jointime(tests, "", ax)
    #generate_bar_compare_custom_and_classic_jointime(tests, "", ax)
    generate_bar_compare_custom_and_classic_rejoin()
    # generate_bar_compare_custom_and_classic_power_consumption(tests, "", ax)
    #generate_radar_solutions()
    # generate_radar_compare_solutions()

    #generate_bar_compare_custom_and_classic_jointime(nodes_5_tests, "Seconds", ax[0][1])
    #generate_bar_compare_custom_and_classic_jointime(nodes_6_tests, "Seconds", ax[0][2])
    #generate_bar_compare_custom_and_classic_jointime(nodes_7_tests, "Seconds", ax[1][0])
    #generate_bar_compare_custom_and_classic_jointime(nodes_8_tests, "Seconds", ax[1][1])
    #generate_bar_compare_custom_and_classic_jointime(nodes_9_tests, "Seconds", ax[1][2])

    # plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.3)
    #plt.show()
    #fig.savefig(f"plots/test.svg", bbox_inches="tight")
