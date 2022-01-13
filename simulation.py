import os, time, shutil, random
from xml.etree import cElementTree as ET


def run_test(cooja, dir, test, seed):
    # run test simulation with seed
    command = f"java -jar {cooja} -nogui={dir}{test} -random-seed={seed}"
    os.system(command)


def remove_command_in_test(dir, test):
    file = f"{dir}{test}"
    root = ET.parse(file)
    for element in root.iter():
        for subelement in element:
            if subelement.tag == "commands":
                element.remove(subelement)
    root.write(file)


def update_firmware_in_test(dir, test, firmware):
    file = f"{dir}{test}"
    root = ET.parse(file)
    for element in root.iter():
        for subelement in element:
            if subelement.tag == "firmware":
                subelement.text = f"[CONTIKI_DIR]/examples/6tisch/simple-node/{firmware}"
    root.write(file)


def add_scriptrunner_in_test(dir, test):
    file = f"{dir}{test}"
    scriptrunner = ""
    if test.startswith("join-"):
        scriptrunner = open(f"{scripts_dir}join.js").read()
    elif test.startswith("create-"):
        scriptrunner = open(f"{scripts_dir}create.js").read()
    root = ET.parse(file)
    for element in root.iter():
        if element.tag == "simconf":
            plugin = ET.Element("plugin")
            plugin.text = "org.contikios.cooja.plugins.ScriptRunner"
            conf = ET.Element("plugin_config")
            script = ET.Element("script")
            script.text = scriptrunner
            active = ET.Element("active")
            active.text = "true"
            conf.append(script)
            conf.append(active)
            plugin.append(conf)
            element.append(plugin)
    root.write(file)


def add_mobility_in_test(dir, test):
    file = f"{dir}{test}"
    root = ET.parse(file)
    for element in root.iter():
        if element.tag == "simconf":
            plugin = ET.Element("plugin")
            plugin.text = "Mobility"
            conf = ET.Element("plugin_config")
            positions = ET.Element("positions")
            positions.set("EXPORT", "copy")
            positions.text = f"[CONTIKI_DIR]/examples/6tisch/simple-node/simulations/positions/{test.replace('.csc', '.dat')}"
            conf.append(positions)
            plugin.append(conf)
            element.append(plugin)
    root.write(file)


def check_if_test_successful(test_output_file_path):
    f = open(test_output_file_path, "r")
    test_output = f.read()
    if("TEST OK" not in test_output):
        print("##### Test failed: 'TEST OK' not found  #####")
        return False
    if("Network created with " not in test_output):
        print("##### Test failed: network not established  #####")
        return False
    if("SIM: Node left network" in test_output):
        print("##### Test failed: Node died #####")
        return False

    network_established_time = float(test_output.split("Network established time: ")[1].split(". First")[0])
    first_eb_time = float(test_output.split("First EB time: ")[1].split(". Join")[0])
    join_time = float(test_output.split("Join time:")[1].split(". Parents")[0])
    parents_considered = int(test_output.split("Parents considered: ")[1].split(".\n")[0])

    if join_time >= network_established_time: #if joining EB joins before network is completely established
        print("##### Test failed: Joining node finishes network #####")
        return False

    return True

if os.path.isdir("/home/user/"):
    cooja_jar = "/home/user/contiki-ng/tools/cooja/dist/cooja.jar"
    run_dir = "/home/user/contiki-ng/examples/6tisch/simple-node/"
    sim_dir = "/home/user/contiki-ng/examples/6tisch/simple-node/simulations/"
    tests_dir = "/home/user/contiki-ng/examples/6tisch/simple-node/simulations/tests/"
    scripts_dir = "/home/user/contiki-ng/examples/6tisch/simple-node/simulations/scriptrunners/"
    pos_dir = "/home/user/contiki-ng/examples/6tisch/simple-node/simulations/positions/"
    log_dir = "/home/user/contiki-ng/examples/6tisch/simple-node/simulations/logs/"
if not os.path.isdir(tests_dir):
    os.mkdir(tests_dir)
if not os.path.isdir(scripts_dir):
    os.mkdir(scripts_dir)
if not os.path.isdir(pos_dir):
    os.mkdir(pos_dir)
if not os.path.isdir(log_dir):
    os.mkdir(log_dir)

seeds = [15557,65890,237601,268521,537634,571714,881378,928542,963159,978437]
# seeds = random.sample(range(0,999999), 10) # 10 random seeds
seeds.sort()
firmwares = ["node-025ebs.z1", "node-05ebs.z1", "node-classic-025ebs.z1", "node-classic-05ebs.z1"]
tests = [f for f in os.listdir(tests_dir) if os.path.isfile(f"{tests_dir}{f}")]
tests.sort()

print("")
print(f"Running tests {tests}.")
print(f"Running tests on firmwares {firmwares}.")
print(f"Running tests on seeds {seeds}.")

os.chdir(run_dir)  # change working directory to run_dir

for test in tests:  # run each test from tests_dir

    for seed in seeds:  # run test with each seed

        for firmware in firmwares:  # run test with every firmware
            shutil.copy(f"{tests_dir}{test}", f"{run_dir}{test}")  # copy test to run_dir
            remove_command_in_test(run_dir, test)  # remove commands in simulation test file
            update_firmware_in_test(run_dir, test, firmware)  # change firmware in file
            add_mobility_in_test(run_dir, test)
            add_scriptrunner_in_test(run_dir, test)
            print(f"\n\n ########### Now running test '{test}' with firmware '{firmware}' and seed '{seed}' ##############\n")
            run_test(cooja_jar, run_dir, test, seed)  # run simulation with seed
            local_seed = seed
            while not check_if_test_successful(f"{run_dir}COOJA.testlog"):  # evaluate if test is OK
                local_seed = random.randint(0,999999)
                run_test(cooja_jar, run_dir, test, local_seed)
            os.rename(f"{run_dir}COOJA.testlog", f"{log_dir}{test.split('.')[0]}_{firmware.split('.')[0]}_{local_seed}.testlog")  # move simulation result log
            os.remove(f"{run_dir}{test}")  # delete test from run_dir
            time.sleep(1)
