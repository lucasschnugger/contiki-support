import shutil
import os
import time 
from file_utils import replace_string_in_file

if os.path.isdir("/home/thanasis/"):
    contiki_dir = "/home/thanasis/repos/contiki-ng/"
    file_dir = "/home/thanasis/repos/contiki-ng/logs/"
    stats_dir = "/home/thanasis/repos/contiki-ng/logs/stats/"
    tsch_dir = "/home/thanasis/repos/contiki-ng/os/net/mac/tsch/"
    build_dir = "/home/thanasis/repos/contiki-ng/examples/6tisch/simple-node/build/"
else: 
    contiki_dir = "{}/contiki-ng/".format(os.getenv('HOME'))
    file_dir = contiki_dir + "logs/"
    stats_dir = contiki_dir + "logs/stats/"
    tsch_dir = contiki_dir + "os/net/mac/tsch/"
    build_dir = contiki_dir + "examples/6tisch/simple-node/build/"
if not os.path.isdir(file_dir):
    os.mkdir(file_dir)
    os.mkdir(stats_dir)
    
# seeds = []
seeds = [0, 1, 10, 20, 35, 127, 304, 856, 1000, 123456]
seeds += [715, 5874, 8128, 42069, 67234, 80085, 84123, 98989, 99999, 933933]
seeds += [222, 420, 5234, 6969, 7945]
seeds.sort()
# seeds = [123456]
algorithms = ['calculate_channel']
# algorithms = ['calculate_channel', 'default']
schedules = ['minimal']
# schedules = ['minimal', 'orchestra']
# guard_times = [1100, 2200, 3300]

for schedule in schedules: 

    if schedule == 'orchestra':
        replace_string_in_file(build_dir + "../Makefile", 'MAKE_WITH_ORCHESTRA', 1)
    elif schedule == 'minimal':
        replace_string_in_file(build_dir + "../Makefile", 'MAKE_WITH_ORCHESTRA', 0)

    for algorithm in algorithms:

        # clean previous mote built and replace tsch.c with algorithm (not needed because cooja cleans the build on its own now)
        # if os.path.isdir(build_dir):
        #     shutil.rmtree(build_dir)
        # os.remove(tsch_dir + 'tsch.c')
        
        shutil.copy(build_dir + '../0tsch_' + algorithm + '.c', tsch_dir + 'tsch.c')
        for seed in seeds:
            if not os.path.isdir(file_dir + "seed:" + str(seed)):
                os.mkdir(file_dir + "/seed:" + str(seed) + "/")
            if not os.path.isdir(file_dir + "seed:" + str(seed) + "/" + schedule):
                os.mkdir(file_dir + "/seed:" + str(seed) + "/" + schedule + "/")
            else:
                delete_previous_results = "find " + file_dir + " -name 'Best result*' -type f -delete"
                os.system(delete_previous_results)

            print("\n ########### Now running simulation with algorithm " + algorithm + ", schedule: " + schedule + " and random seed: " + str(seed) + " ##############\n")
            command = "java -jar ~/contiki-ng/tools/cooja/dist/cooja.jar -nogui=examples/6tisch/simple-node/rpl-tsch-cooja-6-star.csc -random-seed={}".format(seed)
            os.system(command)
            shutil.copy(contiki_dir + "COOJA.testlog", file_dir + "seed:" + str(seed) + "/" + schedule +
                        "/6-star-seed:" + str(seed) + "-" + algorithm + "-" + schedule + ".testlog")   
            
            time.sleep(1) 
            
