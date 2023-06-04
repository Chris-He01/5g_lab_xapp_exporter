#!/usr/local/bin/python
"""Application exporter"""

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

def val_imsi(imsi):
    if imsi == 93:
        return 999700000060593
    elif imsi == 90:
        return 999700000060590
    else:
        return 0

class AppMetrics:
    """
    Representation of Prometheus metrics and loop to fetch and transform
    application metrics into Prometheus metrics.
    """

    def __init__(self, app_port=8083, polling_interval_seconds=5):
        self.app_port = app_port
        self.polling_interval_seconds = polling_interval_seconds

        
        for imsi in imsi_list: 
            for layer in layer_list:
                for kpi in eval(str(layer + "_kpi_list")):
                    # setattr(self, eval("{}*{}+{}".format(kpi, "93", "mac")), Gauge(eval("{}*{}+{}".format(kpi, "93", "mac")), "var"), 0, )
                    #setattr(self, eval("{}*{}+{}".format(kpi, "93", "mac")), Gauge(str(kpi), "93", None, "mac"))
                    ####print( "{}_{}_{}".format(kpi, imsi, layer))
                    setattr(self, "{}_{}_{}".format(kpi, imsi, layer), Gauge(str(kpi + imsi+layer), "{}-{}-{}".format(imsi, layer, kpi)))
        
        #https://github.com/prometheus/client_python/blob/39a62af56b245562d339bf8d032269f087a21a2a/prometheus_client/metrics.py#L311
        # Prometheus metrics to collect
        # self.ue_num = Gauge("ue_num", "number of UEs")
        # self.slice_num = Gauge("slice_num", "number slicing")
        # self.slice_algo = Enum("slice_algo", "slicing algorithm ", states=["STATIC", "DY"])

        # self.dl_num_harq_93_one = Gauge("dl_num_harq_93_one", "dl_num_harq")
        # self.rnti_93_one = Gauge("rnti_93_one", "rnti")
        # self.dl_aggr_prb_93_one = Gauge("dl_aggr_prb_93_one", "dl_aggr_prb")
        # self.dl_mcs1_93_one = Gauge("dl_mcs1_93_one", "dl_mcs1 ")
        # self.dl_aggr_tbs_93_one = Gauge("dl_aggr_tbs_93_one", "dl_aggr_tbs")
        # self.dl_curr_tbs_93_one = Gauge("dl_curr_tbs_93_one", "dl_curr_tbs")

        # self.dl_aggr_sdus_93_one = Gauge("dl_aggr_sdus_93_one", "dl_aggr_sdus")
        # self.wb_cqi_93_one = Gauge("wb_cqi_93_one", "wb_cqi")
        # self.rbid_93_one = Gauge("rbid_93_one", "rbid")
        # self.pdcp_txpdu_pkts_93_one = Gauge("pdcp_txpdu_pkts_93_one", "pdcp_txpdu_pkts")
        # self.pdcp_rxpdu_pkts_93_one = Gauge("pdcp_rxpdu_pkts_93_one", "pdcp_rxpdu_pkts")



        # self.dl_num_harq_90_pix = Gauge("dl_num_harq_90_pix", "dl_num_harq")
        # self.rnti_90_pix = Gauge("rnti_90_pix", "rnti")
        # self.dl_aggr_prb_90_pix = Gauge("dl_aggr_prb_90_pix", "dl_aggr_prb")
        # self.dl_mcs1_90_pix = Gauge("dl_mcs1_90_pix", "dl_mcs1 ")
        # self.dl_aggr_tbs_90_pix = Gauge("dl_aggr_tbs_90_pix", "dl_aggr_tbs")
        # self.dl_curr_tbs_90_pix = Gauge("dl_curr_tbs_90_pix", "dl_curr_tbs")

        # self.dl_aggr_sdus_90_pix = Gauge("dl_aggr_sdus_90_pix", "dl_aggr_sdus")
        # self.wb_cqi_90_pix = Gauge("wb_cqi_90_pix", "wb_cqi")
        # self.rbid_90_pix = Gauge("rbid_90_pix", "rbid")
        # self.pdcp_txpdu_pkts_90_pix = Gauge("pdcp_txpdu_pkts_90_pix", "pdcp_txpdu_pkts")
        # self.pdcp_rxpdu_pkts_90_pix = Gauge("pdcp_rxpdu_pkts_90_pix", "pdcp_rxpdu_pkts")



    def run_metrics_loop(self):
        """Metrics fetching loop"""
        while True:
            self.fetch()
            ##print("here")
            time.sleep(self.polling_interval_seconds)

    def fetch(self):
        """
        Get metrics from application and refresh Prometheus metrics with
        new values.
        """

        # Fetch raw status data from the application
        resp = requests.get('http://129.97.168.82:8083/uploadfiles')
        #print(resp)
        status_data = resp.json()
        ##print(type(status_data))
        ##print(list(self.__dict__))
        for item in list(self.__dict__.items()):
            try:
               ## print("============")
               ## print(item[1]._documentation.split("-")[0])
                ##print(item[1]._documentation.split("-")[1])
                ##print(item[1]._documentation.split("-")[2])
                ##print("next is act")
                ##print(status_data["data_in_file"][item[1]._documentation.split("-")[0]][item[1]._documentation.split("-")[1]][item[1]._documentation.split("-")[2]])
                ##print("==================")

                item[1].set(status_data["data_in_file"][item[1]._documentation.split("-")[0]][item[1]._documentation.split("-")[1]][item[1]._documentation.split("-")[2]])
            except Exception as e:
                print("error: " + str(e))


        # for attr in self:
        #         print(attr.name)
        #         print(attr.documentation)
        #         print(attr.namespace)
        #         print(attr.subsystem)
        

        # for imsi in imsi_list: 
        #     for layer in layer_list:
        #         for kpi in str(layer + "_kpi_list"):
        #             try:
        #                 # setattr(self, eval("{}*{}+{}".format(kpi, "93", "mac")), Gauge(eval("{}*{}+{}".format(kpi, "93", "mac")), "var"), 0, )
        #                 #setattr(self, eval("{}*{}+{}".format(kpi, "93", "mac")), Gauge(str(kpi), "93", None, "mac"))

        #                 setattr(self, eval("{}_{}_{}".format(kpi, imsi, layer)), Gauge(str(kpi), imsi, list(), layer))

        #     for attr in self:
        #         print(attr.name)
        #         print(attr.documentation)
        #         print(attr.namespace)
        #         print(attr.subsystem)
                
                # name = nameof(attr)
                # attr.set(status_data["data_in_file"][eval(val_imsi(str(attr)))])
        
            # Update Prometheus metrics with application metrics
            # self.dl_num_harq_93_one.set(status_data["data_in_file"]["999700000060593"]["dl_num_harq"])
            # self.rnti_93_one.set(status_data["data_in_file"]["999700000060593"]["rnti"])
            # # self.total_uptime.set(status_data["data_in_file"]["total_uptime"])
            # self.dl_aggr_prb_93_one.set(status_data["data_in_file"]["999700000060593"]["dl_aggr_prb"])
            # self.dl_mcs1_93_one.set(status_data["data_in_file"]["999700000060593"]["dl_mcs1"])
            # self.dl_aggr_tbs_93_one.set(status_data["data_in_file"]["999700000060593"]["dl_aggr_tbs"])
            # self.dl_curr_tbs_93_one.set(status_data["data_in_file"]["999700000060593"]["dl_curr_tbs"])

            # self.dl_aggr_sdus_93_one.set(status_data["data_in_file"]["999700000060593"]["dl_aggr_sdus"])
            # self.wb_cqi_93_one.set(status_data["data_in_file"]["999700000060593"]["wb_cqi"])
            # self.rbid_93_one.set(status_data["data_in_file"]["999700000060593"]["rbid"])
            # self.pdcp_txpdu_pkts_93_one.set(status_data["data_in_file"]["999700000060593"]["pdcp_txpdu_pkts"])
            # self.pdcp_rxpdu_pkts_93_one.set(status_data["data_in_file"]["999700000060593"]["pdcp_rxpdu_pkts"])

            
            
            
            # self.dl_num_harq_90_pix.set(status_data["data_in_file"]["999700000060590"]["dl_num_harq"])
            # self.rnti_90_pix.set(status_data["data_in_file"]["999700000060590"]["rnti"])
            # # self.total_uptime.set(status_data["data_in_file"]["total_uptime"])
            # self.dl_aggr_prb_90_pix.set(status_data["data_in_file"]["999700000060590"]["dl_aggr_prb"])
            # self.dl_mcs1_90_pix.set(status_data["data_in_file"]["999700000060590"]["dl_mcs1"])
            # self.dl_aggr_tbs_90_pix.set(status_data["data_in_file"]["999700000060590"]["dl_aggr_tbs"])
            # self.dl_curr_tbs_90_pix.set(status_data["data_in_file"]["999700000060590"]["dl_curr_tbs"])
            
            # self.dl_aggr_sdus_90_pix.set(status_data["data_in_file"]["999700000060590"]["dl_aggr_sdus"])
            # self.wb_cqi_90_pix.set(status_data["data_in_file"]["999700000060590"]["wb_cqi"])
            # self.rbid_90_pix.set(status_data["data_in_file"]["999700000060590"]["rbid"])
            # self.pdcp_txpdu_pkts_90_pix.set(status_data["data_in_file"]["999700000060590"]["pdcp_txpdu_pkts"])
            # self.pdcp_rxpdu_pkts_90_pix.set(status_data["data_in_file"]["999700000060590"]["pdcp_rxpdu_pkts"])


        # self.dl_num_harq = Gauge("dl_num_harq", "dl_num_harq")
        # self.rnti = Gauge("rnti", "rnti")
        # self.dl_aggr_prb = Gauge("dl_aggr_prb", "dl_aggr_prb")
        # self.dl_mcs1 = Gauge("dl_mcs1", "dl_mcs1 ")
        # self.dl_aggr_tbs = Gauge("dl_aggr_tbs", "dl_aggr_tbs")
        # self.dl_curr_tbs = Gauge("dl_curr_tbs", "dl_curr_tbs")

def main():
    """Main entry point"""

    polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "5"))
    app_port = int(os.getenv("APP_PORT", "8083"))
    exporter_port = int(os.getenv("EXPORTER_PORT", "9092"))

    app_metrics = AppMetrics(
        app_port=app_port,
        polling_interval_seconds=polling_interval_seconds
    )
    start_http_server(exporter_port)
    app_metrics.run_metrics_loop()

if __name__ == "__main__":
    main()