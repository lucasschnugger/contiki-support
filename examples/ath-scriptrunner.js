TIMEOUT(680000, log.log("last msg: " + msg + "\n")); /* milliseconds. print last msg at timeout */

var mobile_node_participation = 30000000;
var mobile_node_rejoin = 20000000;

var association_time = [];
var disassociation_time = [];
var connection_status = [];

motes = sim.getMotes();


for(var i=1; i &lt; motes.length; i++) {
    association_time.push(-1);
    disassociation_time.push(-1);
    connection_status.push(-1);
}

while(1) {
    m = motes[id-1];

    if(msg.contains("association done")) {
        association_time[id-2] = time;
        connection_status[id-2] = 1;
//         log.log("ID: " + id + ": Association done at: " + time + "\n");
    }
    if(association_time[id-2] &gt; -1 &amp;&amp; (time - association_time[id-2] &gt; mobile_node_participation)) {
	    var x = m.getInterfaces().getPosition().getXCoordinate();
        var y = m.getInterfaces().getPosition().getYCoordinate();
        m.getInterfaces().getPosition().setCoordinates(x+150, y, 0);
        association_time[id-2] = -1;
    }
    if(msg.contains("leaving the network, stats")) {
        disassociation_time[id-2] = time;
        connection_status[id-2] = -1;
//         log.log("ID: " + id + ": Left the Network at: " + time + "\n");
    }
    if(disassociation_time[id-2] &gt; -1 &amp;&amp; (time - disassociation_time[id-2] &gt; mobile_node_rejoin)) {
	    var x = m.getInterfaces().getPosition().getXCoordinate();
        var y = m.getInterfaces().getPosition().getYCoordinate();
        m.getInterfaces().getPosition().setCoordinates(x-150, y, 0);
        disassociation_time[id-2] = -1;
    }
    if(msg.contains("bc-1") &amp;&amp; id == 1) {
//         log.log("----------------------------------------------------\n");
        var true_channel = motes[0].getInterfaces().getRadio().getChannel();
//         log.log("true_channel: " + true_channel + "\n");
        for(var i=1; i&lt;motes.length; i++) {
            if(connection_status[i-1] == -1 &amp;&amp; motes[i].getInterfaces().getPosition().getDistanceTo(motes[0]) &lt;= 50) {
//                 log.log("Mote " + (i+1) + " in range and scanning on channel: " + motes[i].getInterfaces().getRadio().getChannel() + "\n");
            }
        }
//         log.log("----------------------------------------------------\n");
    }
    log.log(sim.getSimulationTimeMillis() + "\t ID:" + id + "\t" + msg + "\n");
	YIELD(); /* wait for another mote output */
}

log.testOK(); /* Report test success and quit */
//log.testFailed(); /* Report test failure and quit */