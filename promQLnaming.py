import os
import time
from prometheus_client import start_http_server, Gauge, Enum
import requests
import json



mac_kpi_list = ['dl_aggr_tbs', 'ul_aggr_tbs', 'dl_aggr_bytes_sdus', 'ul_aggr_bytes_sdus', 'dl_curr_tbs', 'ul_curr_tbs', 'dl_sched_rb', 'ul_sched_rb', 'pusch_snr', 'pucch_snr', 'dl_bler', 'ul_bler', 'dl_num_harq', 'ul_num_harq', 'rnti', 'dl_aggr_prb', 'ul_aggr_prb', 'dl_aggr_sdus', 'ul_aggr_sdus', 'dl_aggr_retx_prb', 'ul_aggr_retx_prb', 'bsr', 'frame', 'slot', 'wb_cqi', 'dl_mcs1', 'ul_mcs1', 'dl_mcs2', 'ul_mcs2', 'phr']
rlc_kpi_list = ['txpdu_pkts', 'txpdu_bytes', 'txpdu_wt_ms', 'txpdu_dd_pkts', 'txpdu_dd_bytes', 'txpdu_retx_pkts', 'txpdu_retx_bytes', 'txpdu_segmented', 'txpdu_status_pkts', 'txpdu_status_bytes', 'txbuf_occ_bytes', 'txbuf_occ_pkts', 'rxpdu_pkts', 'rxpdu_bytes', 'rxpdu_dup_pkts', 'rxpdu_dup_bytes', 'rxpdu_dd_pkts', 'rxpdu_dd_bytes', 'rxpdu_ow_pkts', 'rxpdu_ow_bytes', 'rxpdu_status_pkts', 'rxpdu_status_bytes', 'rxbuf_occ_bytes', 'rxbuf_occ_pkts', 'txsdu_pkts', 'txsdu_bytes', 'rxsdu_pkts', 'rxsdu_bytes', 'rxsdu_dd_pkts', 'rxsdu_dd_bytes', 'rnti', 'mode', 'rbid']
pdcp_kpi_list = ['txpdu_pkts', 'txpdu_bytes', 'txpdu_sn', 'rxpdu_pkts', 'rxpdu_bytes', 'rxpdu_sn', 'rxpdu_oo_pkts', 'rxpdu_oo_bytes', 'rxpdu_dd_pkts', 'rxpdu_dd_bytes', 'rxpdu_ro_count', 'txsdu_pkts', 'txsdu_bytes', 'rxsdu_pkts', 'rxsdu_bytes', 'rnti', 'mode', 'rbid']
imsi_list = ["999700000060593", "999700000060590"]
layer_list = ["mac", "rlc", "pdcp"]


def is_item_at_end(item, my_list):
    return my_list.index(item) == len(my_list) - 1

for imsi in imsi_list:
    for layer in layer_list:
        print("{__name__=~\"", end="")
        for kpi in eval("{}_kpi_list".format(layer)):
            if(is_item_at_end(kpi, eval("{}_kpi_list".format(layer)))):
                print(kpi, imsi, layer, end="", sep="")
            else:
                print(kpi, imsi, layer, end="|", sep="")
            
        print("\"}")


