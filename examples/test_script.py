import shutil
import os
import time 
# seed = list(range(500000, 500020,1))
seed = "123456"
alpha = [0.25, 0.5, 0.75]
RSSI_high = [-90, -85,-80,-75, -70, -65]
RSSI_low = [-85, -80, -75, -70, -65, -60]

s1 = "return (0.25 * rssi) + (1- 0.25) * EWMA;"
s2 = "if (rssi_ewma <= -90 && child){"
s3 = "if (rssi_ewma >= -85 && speed_change){"


for rssi_value_high,rssi_value_low in zip(RSSI_high,RSSI_low):
	for a in alpha:
		fin = open("node.c", "rt")
		
		data = fin.read()
		#replace all occurrences of the required string
		data = data.replace(s1, "return ("+str(a)+" * rssi) + (1-"+str(a)+") * EWMA;")
		s1 = "return ("+str(a)+" * rssi) + (1-"+str(a)+") * EWMA;"

		data = data.replace(s2, "if (rssi_ewma <= " +str(rssi_value_high) +" && child){")
		s2 = "if (rssi_ewma <= " +str(rssi_value_high) +" && child){" 

		data = data.replace(s3, "if (rssi_ewma >= " +str(rssi_value_low) +" && speed_change){")
		s3 = "if (rssi_ewma >= " +str(rssi_value_low) +" && speed_change){"

		#close the input file
		fin.close()
		#open the input file in write mode
		fin = open("node.c", "wt")
		#overrite the input file with the resulting data
		fin.write(data)
		#close the file
		fin.close()

		print("\n ########### Now running simulation with alpha " + str(a) + ", RSSI_high, RSSI_low: " + str(rssi_value_high) +","+ str(rssi_value_low) + " and random seed: "+ str(seed)  + " ##############\n")
		command = "java -jar ../../../../tools/cooja/dist/cooja.jar -nogui=dynamic_speed_light_z1_case1_packet_rate_LogisticLoss.csc -random-seed="+seed
		os.system(command)
		shutil.copy("COOJA.testlog", "../../../logs/LogisticLoss_fixed_speed/" + "alpha:" + str(a) + ", RSSI_high, RSSI_low: " + str(rssi_value_high) +","+ str(rssi_value_low) + " seed: "+ seed  +"[2,3]_manual_packet_rate_LogisticLoss_steep_accelerate.testlog")
		# shutil.copy("COOJA.testlog", "../../../logs/LogisticLoss_fixed_speed/" + "Active Connectivity Deactivated[1,3]_manual_packet_rate_LogisticLoss.testlog")
		time.sleep(1) 

