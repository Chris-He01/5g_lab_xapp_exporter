import xapp_sdk as ric
import time
import os
import pdb
import json

####################
#### MAC INDICATION CALLBACK
####################

#  MACCallback class is defined and derived from C++ class mac_cb
class MACCallback(ric.mac_cb):
    # Define Python class 'constructor'
    def __init__(self):
        # Call C++ base class constructor
        ric.mac_cb.__init__(self)
    # Override C++ method: virtual void handle(swig_mac_ind_msg_t a) = 0;
    def handle(self, ind):
        print("here1")
        slice_stats = {
            "dl_num_harq": {},
            "rnti": {},
            "dl_aggr_prb": {},
            "dl_mcs1": {},
            "dl_aggr_tbs": {},
            "dl_curr_tbs": {}
        }
        print("here2")
        # Print swig_mac_ind_msg_t
        t_now = time.time_ns() / 1000.0
        t_mac = ind.tstamp / 1.0
        t_diff = t_now - t_mac
        print('MAC Indication tstamp = ' + str(t_mac) + ' diff = ' + str(t_diff))
        print("Number of connected users: ", len(ind.ue_stats))
        for iter, item in enumerate(ind.ue_stats):
            print("-------------")
            #print("MAC UE rnti: ", item.rnti)
            try: 
                slice_stats["dl_num_harq"] = item.dl_num_harq
                slice_stats["rnti"] = item.rnti
                slice_stats["dl_aggr_prb"] = item.dl_aggr_prb
                slice_stats["dl_mcs1"] = item.dl_mcs1
                slice_stats["dl_aggr_tbs"] = item.dl_aggr_tbs
                slice_stats["dl_curr_tbs"] = item.dl_curr_tbs

            
            print("MAC dl_num_harq: ", item.dl_aggr_tbs)
            print("MAC rnti: ", item.rnti)
        
        stats_json = json.dumps(slice_stats)
        
        with open("rt_slice_stats.json", "w") as outfile:
            outfile.write(ind_json)
        
        time.sleep(2)
        print("===============================")

####################
####  GENERAL 
####################
print("ric is going to init")
ric.init()

print("ric did init")

conn = ric.conn_e2_nodes()
assert(len(conn) > 0)
for i in range(0, len(conn)):
    print("Global E2 Node [" + str(i) + "]: PLMN MCC = " + str(conn[i].id.plmn.mcc))
    print("Global E2 Node [" + str(i) + "]: PLMN MNC = " + str(conn[i].id.plmn.mnc))

####################
#### MAC INDICATION
####################

mac_hndlr = []
for i in range(0, len(conn)):
    mac_cb = MACCallback()
    hndlr = ric.report_mac_sm(conn[i].id, ric.Interval_ms_10, mac_cb)
    mac_hndlr.append(hndlr)     
    time.sleep(1)

time.sleep(5)
print("After subsription!")
time.sleep(60000)

for i in range(0, len(mac_hndlr)):
    ric.rm_report_mac_sm(mac_hndlr[i])

# for i in range(0, len(rlc_hndlr)):
#     ric.rm_report_rlc_sm(rlc_hndlr[i])

# for i in range(0, len(pdcp_hndlr)):
#     ric.rm_report_pdcp_sm(pdcp_hndlr[i])

# Avoid deadlock. ToDo revise architecture 
while ric.try_stop == 0:
    time.sleep(1)

print("Test finished")
