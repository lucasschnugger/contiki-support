TIMEOUT(600000, log.log("\nSIMULATION ENDED BY TIMEOUT\n")); // End simulation after 600,000 ms (10 min.)

let motes = sim.getMotes();
let mote_count = motes.length;
let network_size = 0;
let network_established_time;
let first_eb_time;
while(1){
    // time; time of output message
    // mote; current mote
    // id; id of current mote
    // msg; current output message from mote

    // if output message contains results from simulation
    if (msg.contains("SIM:")){
        if (msg.contains("disassociated")){ // if mote disassociated
            network_size--;
        }else if(msg.contains("associated")){ // if mote associated
            network_size++;
            if (network_size == mote_count-1){ // if all but one mote associated
                network_established_time = time;
                log.log(time + ": " + " Network created with " + network_size + " motes.\n");
            }
        }

        if (msg.contains("discovered motes")){ // if a mote associated, how many motes were discovered
            let msgTrimmed = msg.split("SIM:")[1];
            let reg = new RegExp(".*(\\d).*(\\d).*");
            let matches = reg.exec(msgTrimmed);
            let moteId = parseInt(matches[1]);
            let discoveredMotes = parseInt(matches[2]);
            log.log(time + ": Mote " + moteId + " discovered " + discoveredMotes + " motes before associating.\n");
            if(moteId == mote_count){ //Always highest ID mote joining last
                log.log("Network established time: "+network_established_time+
                    ". First EB time: "+first_eb_time+
                    ". Join time: " + time +
                    ". Parents considered: " + discoveredMotes +".\n"
                );
                log.testOK();
            }
        }

        if (msg.contains("discovered EB")){
            let msgTrimmed = msg.split("SIM:")[1];
            let reg = new RegExp(".*(\\d).*(\\d).*(\\d).*");
            let matches = reg.exec(msgTrimmed);
            let moteId = parseInt(matches[1]);
            let discoveredMotes = parseInt(matches[2]);
            let ebSrcMoteId = parseInt(matches[3]);
            if (discoveredMotes == 1){
                log.log(time + ": " + "Mote " + moteId + " found first EB from mote " + ebSrcMoteId + ".\n");
                if(moteId == mote_count){
                    first_eb_time = time;
                }
            }
        }
    }
    YIELD(); // wait for next mote output message
}

log.testOK();
