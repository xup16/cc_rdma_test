import itertools
import math
from paper_plots import *
# Experiments to run and analyze
# Go to end of file to fill in experiments 
SHORTNAMES = {
    "CLIENT_NODE_CNT" : "CN",
    "CLIENT_THREAD_CNT" : "CT",
    "CLIENT_REM_THREAD_CNT" : "CRT",
    "CLIENT_SEND_THREAD_CNT" : "CST",
    "NODE_CNT" : "N",
    "THREAD_CNT" : "T",
    "REM_THREAD_CNT" : "RT",
    "SEND_THREAD_CNT" : "ST",
    "CC_ALG" : "",
    "WORKLOAD" : "",
    "MAX_TXN_PER_PART" : "TXNS",
    "MAX_TXN_IN_FLIGHT" : "TIF",
    "PART_PER_TXN" : "PPT",
    "TUP_READ_PERC" : "TRD",
    "TUP_WRITE_PERC" : "TWR",
    "TXN_READ_PERC" : "RD",
    "TXN_WRITE_PERC" : "WR",
    "ZIPF_THETA" : "SKEW",
    "MSG_TIME_LIMIT" : "BT",
    "MSG_SIZE_MAX" : "BS",
    "DATA_PERC":"D",
    "ACCESS_PERC":"A",
    "PERC_PAYMENT":"PP",
    "MPR":"MPR",
    "REQ_PER_QUERY": "RPQ",
    "MODE":"",
    "PRIORITY":"",
    "ABORT_PENALTY":"PENALTY",
    "STRICT_PPT":"SPPT",
    "NETWORK_DELAY":"NDLY",
    "REPLICA_CNT":"RN",
    "SYNTH_TABLE_SIZE":"TBL",
    "ISOLATION_LEVEL":"LVL",
    "YCSB_ABORT_MODE":"ABRTMODE",
}

#config_names=["CLIENT_NODE_CNT","NODE_CNT","MAX_TXN_PER_PART","WORKLOAD","CC_ALG","MPR","CLIENT_THREAD_CNT","CLIENT_REM_THREAD_CNT","CLIENT_SEND_THREAD_CNT","THREAD_CNT","REM_THREAD_CNT","SEND_THREAD_CNT","MAX_TXN_IN_FLIGHT","ZIPF_THETA","TXN_WRITE_PERC","TUP_WRITE_PERC","PART_PER_TXN","PART_CNT","MSG_TIME_LIMIT","MSG_SIZE_MAX","MODE","DATA_PERC","ACCESS_PERC","REQ_PER_QUERY"]
fmt_title=["NODE_CNT","CC_ALG","ACCESS_PERC","TXN_WRITE_PERC","PERC_PAYMENT","MPR","MODE","MAX_TXN_IN_FLIGHT","SEND_THREAD_CNT","REM_THREAD_CNT","THREAD_CNT","TXN_WRITE_PERC","TUP_WRITE_PERC","ZIPF_THETA"]

##############################
# VLDB PAPER PLOTS
##############################

def ycsb_scaling():
    wl = 'YCSB'
    nnodes = [1,2,4,8,16]#,32,48,64]
    algos=['NO_WAIT','WAIT_DIE','MVCC','MAAT','CALVIN','TIMESTAMP']
    base_table_size=2097152*8
    txn_write_perc = [0.5,1.0]
    tup_write_perc = [0.5]
    load = [10000]
    tcnt = [4]
    skew = [0.0,0.6,0.7]
    fmt = ["WORKLOAD","NODE_CNT","CC_ALG","SYNTH_TABLE_SIZE","TUP_WRITE_PERC","TXN_WRITE_PERC","MAX_TXN_IN_FLIGHT","ZIPF_THETA","THREAD_CNT"]
    exp = [[wl,n,algo,base_table_size*n,tup_wr_perc,txn_wr_perc,ld,sk,thr] for thr,txn_wr_perc,tup_wr_perc,sk,ld,n,algo in itertools.product(tcnt,txn_write_perc,tup_write_perc,skew,load,nnodes,algos)]
    txn_write_perc = [0.0]
    skew = [0.0]
    exp = exp + [[wl,n,algo,base_table_size*n,tup_wr_perc,txn_wr_perc,ld,sk,thr] for thr,txn_wr_perc,tup_wr_perc,sk,ld,n,algo in itertools.product(tcnt,txn_write_perc,tup_write_perc,skew,load,nnodes,algos)]
    return fmt,exp

def ycsb_skew():
    wl = 'YCSB'
    nnodes = [16]
    algos=['NO_WAIT','WAIT_DIE','MVCC','MAAT','CALVIN','TIMESTAMP']
    base_table_size=2097152*8
    txn_write_perc = [0.5,1.0]
    tup_write_perc = [0.5]
    load = [10000]
    tcnt = [4]
    skew = [0.0,0.25,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.9]
    fmt = ["WORKLOAD","NODE_CNT","CC_ALG","SYNTH_TABLE_SIZE","TUP_WRITE_PERC","TXN_WRITE_PERC","MAX_TXN_IN_FLIGHT","ZIPF_THETA","THREAD_CNT"]
    exp = [[wl,n,algo,base_table_size*n,tup_wr_perc,txn_wr_perc,ld,sk,thr] for thr,txn_wr_perc,tup_wr_perc,ld,n,sk,algo in itertools.product(tcnt,txn_write_perc,tup_write_perc,load,nnodes,skew,algos)]
    return fmt,exp


def isolation_levels():
    wl = 'YCSB'
    nnodes = [1,2,4,8,16]#,32,48]
    algos=['NO_WAIT','WAIT_DIE','MVCC','MAAT','CALVIN','TIMESTAMP']
    levels=["READ_UNCOMMITTED","READ_COMMITTED","SERIALIZABLE"]
    base_table_size=2097152*8
    load = [10000]
    txn_write_perc = [0.5,1.0]
    tup_write_perc = [0.5]
    skew = [0.6,0.7]
    fmt = ["WORKLOAD","NODE_CNT","CC_ALG","SYNTH_TABLE_SIZE","TUP_WRITE_PERC","TXN_WRITE_PERC","ISOLATION_LEVEL","MAX_TXN_IN_FLIGHT","ZIPF_THETA"]
    exp = [[wl,n,algo,base_table_size*n,tup_wr_perc,txn_wr_perc,level,ld,sk] for txn_wr_perc,tup_wr_perc,algo,sk,ld,n,level in itertools.product(txn_write_perc,tup_write_perc,algos,skew,load,nnodes,levels)]
    return fmt,exp

def ycsb_partitions():
    wl = 'YCSB'
    nnodes = [16]
    algos=['NO_WAIT','WAIT_DIE','MVCC','MAAT','CALVIN','TIMESTAMP']
    load = [10000]
    nparts = [1,2,4,6,8,10,12,14,16]
    base_table_size=2097152*8
    txn_write_perc = [0.5,1.0]
    tup_write_perc = [0.5]
    tcnt = [4]
    skew = [0.0,0.6,0.7]
#    recv = [2,4]
    rpq =  16
    fmt = ["WORKLOAD","REQ_PER_QUERY","PART_PER_TXN","NODE_CNT","CC_ALG","SYNTH_TABLE_SIZE","TUP_WRITE_PERC","TXN_WRITE_PERC","MAX_TXN_IN_FLIGHT","ZIPF_THETA","THREAD_CNT","STRICT_PPT"]
    exp = [[wl,rpq,p,n,algo,base_table_size*n,tup_wr_perc,txn_wr_perc,ld,sk,thr,1] for thr,txn_wr_perc,tup_wr_perc,algo,sk,ld,n,p in itertools.product(tcnt,txn_write_perc,tup_write_perc,algos,skew,load,nnodes,nparts)]
    txn_write_perc = [0.0]
    skew = [0.0]
    exp = exp + [[wl,rpq,p,n,algo,base_table_size*n,tup_wr_perc,txn_wr_perc,ld,sk,thr,1] for thr,txn_wr_perc,tup_wr_perc,algo,sk,ld,n,p in itertools.product(tcnt,txn_write_perc,tup_write_perc,algos,skew,load,nnodes,nparts)]
    return fmt,exp

def tpcc_scaling():
    wl = 'TPCC'
    nnodes = [1,2,4,8,16]#,16,32,64]
    nalgos=['NO_WAIT','WAIT_DIE','MAAT','MVCC','TIMESTAMP','CALVIN']
    npercpay=[0.0,0.5,1.0]
    wh=128
    fmt = ["WORKLOAD","NODE_CNT","CC_ALG","PERC_PAYMENT","NUM_WH"]
    exp = [[wl,n,cc,pp,wh] for pp,n,cc in itertools.product(npercpay,nnodes,nalgos)]
    exp = exp + [[wl,n,cc,pp,wh*n] for pp,n,cc in itertools.product(npercpay,nnodes,nalgos)]
    wh=256
    exp = exp + [[wl,n,cc,pp,wh] for pp,n,cc in itertools.product(npercpay,nnodes,nalgos)]
    wh=4
    exp = exp + [[wl,n,cc,pp,wh*n] for pp,n,cc in itertools.product(npercpay,nnodes,nalgos)]
    return fmt,exp


##############################
# END VLDB PAPER PLOTS
##############################

def ycsb_scaling_plot(summary,summary_client):
    from helper import plot_prep
    from plot_helper import tput,time_breakdown
    nfmt,nexp = ycsb_scaling()
    x_name="NODE_CNT"
    v_name="CC_ALG"
#    tput_setup(summary,summary_client,nfmt,nexp,x_name,v_name)
    skew = [0.6,0.7,0.75,0.8,0.85,0.9]
    skew = [0.6,0.7]
    txn_write_perc = [0.5,0.75,1.0]
    txn_write_perc = [0.5,1.0]
    for sk,wr in itertools.product(skew,txn_write_perc):
        const={"ZIPF_THETA":sk,"TXN_WRITE_PERC":wr}
        title = ""
        for c in const.keys():
            title += "{} {},".format(SHORTNAMES[c],const[c])
        x_vals,v_vals,fmt,exp,lst = plot_prep(nexp,nfmt,x_name,v_name,constants=const)
        tput(x_vals,v_vals,summary,summary_client,cfg_fmt=fmt,cfg=list(exp),xname=x_name,vname=v_name,xlab="Server Count",new_cfgs=lst,ylimit=140,logscalex=False,title=title)
#        for x in x_vals:
#            const[x_name] = x
#            title2 = title + "{} {},".format(SHORTNAMES[x_name],const[x_name])
#            v_vals,tmp,fmt,exp,lst = plot_prep(nexp,nfmt,v_name,'',constants=const)
#            time_breakdown(v_vals,summary,cfg_fmt=fmt,cfg=list(exp),xname=v_name,new_cfgs=lst,title=title2)
#    breakdown_setup(summary,nfmt,nexp,x_name)

def ycsb_skew_plot(summary,summary_client):
    from helper import plot_prep
    from plot_helper import tput,time_breakdown
    nfmt,nexp = ycsb_skew()
    x_name="ZIPF_THETA"
    v_name="CC_ALG"
#    tput_setup(summary,summary_client,nfmt,nexp,x_name,v_name)
    txn_write_perc = [0.5,0.75,1.0]
    for wr in txn_write_perc:#itertools.product(skew,txn_write_perc):
        const={"TXN_WRITE_PERC":wr}
        title = ""
        for c in const.keys():
            title += "{} {},".format(SHORTNAMES[c],const[c])
        x_vals,v_vals,fmt,exp,lst = plot_prep(nexp,nfmt,x_name,v_name,constants=const)
        tput(x_vals,v_vals,summary,summary_client,cfg_fmt=fmt,cfg=list(exp),xname=x_name,vname=v_name,xlab="Server Count",new_cfgs=lst,ylimit=140,logscalex=False,title=title)

def ycsb_load():
    wl = 'YCSB'
    algos=['NO_WAIT']
    algos=['NO_WAIT','WAIT_DIE','MVCC','MAAT']
    algos=['NO_WAIT','WAIT_DIE','MAAT']
    load = [10000]
    base_table_size=2097152*8
    txn_write_perc = [0.5]
    tup_write_perc = [0.5]
    nnodes = [8]
    tcnt = [4]
    skew = [0.3,0.6,0.7]
#    recv = [2,4]
    rpq =  8 
#    fmt = ["WORKLOAD","NODE_CNT","CC_ALG","SYNTH_TABLE_SIZE","TUP_WRITE_PERC","TXN_WRITE_PERC","MAX_TXN_IN_FLIGHT","ZIPF_THETA","REM_THREAD_CNT"]
#    exp = [[wl,n,algo,base_table_size*n,tup_wr_perc,txn_wr_perc,ld,sk,rcv] for rcv,txn_wr_perc,tup_wr_perc,algo,sk,ld,n in itertools.product(recv,txn_write_perc,tup_write_perc,algos,skew,load,nnodes)]
    fmt = ["WORKLOAD","NODE_CNT","CC_ALG","SYNTH_TABLE_SIZE","TUP_WRITE_PERC","TXN_WRITE_PERC","MAX_TXN_IN_FLIGHT","ZIPF_THETA","THREAD_CNT","YCSB_ABORT_MODE"]
    exp = [[wl,n,algo,base_table_size*n,tup_wr_perc,txn_wr_perc,ld,sk,thr,'false'] for thr,txn_wr_perc,tup_wr_perc,algo,sk,ld,n in itertools.product(tcnt,txn_write_perc,tup_write_perc,algos,skew,load,nnodes)]
    return fmt,exp


def ycsb_load_plot(summary,summary_client):
    from helper import plot_prep
    from plot_helper import tput
    nfmt,nexp = ycsb_load()
    v_name="NODE_CNT"
    x_name="MAX_TXN_IN_FLIGHT"
#    tput_setup(summary,summary_client,nfmt,nexp,x_name,v_name)
    txn_write_perc = [0.01,0.1,0.2,0.5,1.0]
    txn_write_perc = [0.0,0.5]
    skew = [0.0,0.3,0.6,0.9]
    skew = [0.6]
    tcnt = [4]
    for wr,sk,thr in itertools.product(txn_write_perc,skew,tcnt):
        const={"TXN_WRITE_PERC":wr,"ZIPF_THETA":sk,"THREAD_CNT":thr}
        title = ""
        for c in const.keys():
            title += "{} {},".format(SHORTNAMES[c],const[c])
        x_vals,v_vals,fmt,exp,lst = plot_prep(nexp,nfmt,x_name,v_name,constants=const)
        tput(x_vals,v_vals,summary,summary_client,cfg_fmt=fmt,cfg=list(exp),xname=x_name,vname=v_name,xlab="Open Client Connections",new_cfgs=lst,ylimit=0.14,logscalex=False,title=title)


def isolation_levels_plot(summary,summary_client):
    from helper import plot_prep
    from plot_helper import tput
    nfmt,nexp = isolation_levels()
    x_name="NODE_CNT"
    v_name="ISOLATION_LEVEL"
#    tput_setup(summary,summary_client,nfmt,nexp,x_name,v_name)
    txn_write_perc = [0.1,0.2,0.5,1.0]
    skew = [0.0,0.3,0.6]
    for wr,sk in itertools.product(txn_write_perc,skew):
        const={"TXN_WRITE_PERC":wr,"ZIPF_THETA":sk,"TUP_WRITE_PERC":1.0}
        title = ""
        for c in const.keys():
            title += "{} {},".format(SHORTNAMES[c],const[c])
        x_vals,v_vals,fmt,exp,lst = plot_prep(nexp,nfmt,x_name,v_name,constants=const)
        tput(x_vals,v_vals,summary,summary_client,cfg_fmt=fmt,cfg=list(exp),xname=x_name,vname=v_name,xlab="Server Count",new_cfgs=lst,ylimit=0.14,logscalex=False,title=title,name='')



def tpcc_scaling_whset():
    wl = 'TPCC'
    nnodes = [1,2,4,8]#,16,32,64]
    nalgos=['NO_WAIT','WAIT_DIE','OCC','MVCC','TIMESTAMP','CALVIN']
    nalgos=['NO_WAIT','WAIT_DIE','OCC','MAAT']
    npercpay=[0.0,1.0]
    wh=128
    fmt = ["WORKLOAD","NODE_CNT","CC_ALG","PERC_PAYMENT","NUM_WH"]
    exp = [[wl,n,cc,pp,wh] for pp,n,cc in itertools.product(npercpay,nnodes,nalgos)]
    exp = exp + [[wl,n,cc,pp,wh*n] for pp,n,cc in itertools.product(npercpay,nnodes,nalgos)]
    return fmt,exp
##############################
##############################

def replica_test():
    wl = 'YCSB'
    nnodes = [1,2]
    nrepl = [0,1]
    nwr = [0.2]
    nalgos=['NO_WAIT']
    fmt = ["WORKLOAD","NODE_CNT","CC_ALG","TUP_WRITE_PERC","MAX_TXN_IN_FLIGHT","REPLICA_CNT","LOGGING"]
    exp = [[wl,n,cc,wr,1000,repl,"true"] for n,cc,wr,repl in itertools.product(nnodes,nalgos,nwr,nrepl)]
    exp += [[wl,n,cc,wr,1000,0,"false"] for n,cc,wr in itertools.product(nnodes,nalgos,nwr)]
    return fmt,exp


def malviya():
    wl = 'YCSB'
    nnodes = [1]
    nrepl = [0,1]
    nwr = [0.2]
    nalgos=['NO_WAIT']
    ntif = [5000,10000,25000,50000,100000,150000,200000,250000,300000,350000]
    nload=[]
    fmt = ["WORKLOAD","NODE_CNT","CC_ALG","PART_PER_TXN","TUP_WRITE_PERC","MAX_TXN_IN_FLIGHT","REPLICA_CNT","MAX_TXN_IN_FLIGHT","LOGGING"]
    exp = [[wl,n,cc,2,wr,1000,repl,tif,"true"] for n,cc,wr,repl,tif in itertools.product(nnodes,nalgos,nwr,nrepl,ntif)]
    exp += [[wl,n,cc,2,wr,1000,0,tif,"false"] for n,cc,wr,tif in itertools.product(nnodes,nalgos,nwr,ntif)]
    return fmt,exp

def malviya_plot(summary,summary_client):
    nfmt,nexp = malviya()
    x_name = "MAX_TXN_IN_FLIGHT"
    v_name = "REPLICA_CNT"
    tput_setup(summary,summary_client,nfmt,nexp,x_name,v_name)
    v_name = "LOGGING"
    tput_setup(summary,summary_client,nfmt,nexp,x_name,v_name)

def test():
    wl = 'YCSB'
    nnodes = [1,2,4]
    nnodes = [1]
    nnodes = [2]
    ntif = [10000]
    nwr = [0.0,0.25,0.5,0.75,1.0] # TXN_WRITE_PERC
    nwr = [0.0,0.5,1.0] # TXN_WRITE_PERC
    nwr = [0.5] # TXN_WRITE_PERC
    nwr = [0.5,1.0] # TXN_WRITE_PERC
    nwr2 = [0.5] # TUP_WRITE_PERC 
    nalgos=['CALVIN','NO_WAIT']
    nmodes=['true']
    nmodes=['true','false']
    noutthr=[4]
    ninthr=[4]
#    noutthr=[1,2,3]
    nskew = [0.0,0.3,0.6,0.7,0.75,0.8,0.85,0.9]
    nskew = [0.6]
    nskew = [0.6,0.7]
    nworkthr=[4]
    base_table_size=2097152*8
#    nworkthr=[3]
#    nalgos=['MVCC','TIMESTAMP','CALVIN']
#    nnodes = [2]
#    nalgos=['OCC']
    fmt = ["WORKLOAD","NODE_CNT","CC_ALG","TXN_WRITE_PERC","TUP_WRITE_PERC","MAX_TXN_IN_FLIGHT","SEND_THREAD_CNT","REM_THREAD_CNT","THREAD_CNT","SYNTH_TABLE_SIZE","YCSB_ABORT_MODE","ZIPF_THETA"]
    exp = [[wl,n,cc,wr,wr2,tif,outthr,inthr,workthr,base_table_size * n,mode,skew] for mode,cc,wr,wr2,tif,outthr,inthr,workthr,skew,n in itertools.product(nmodes,nalgos,nwr,nwr2,ntif,noutthr,ninthr,nworkthr,nskew,nnodes)]
#    fmt = ["WORKLOAD","NODE_CNT","CC_ALG","TXN_WRITE_PERC","TUP_WRITE_PERC","MAX_TXN_IN_FLIGHT","THREAD_CNT","PART_PER_TXN"]
#    exp = [[wl,n,cc,wr,wr2,tif,workthr,1] for n,cc,wr,wr2,tif,workthr in itertools.product(nnodes,nalgos,nwr,nwr2,ntif,nworkthr)]
#    fmt = ["WORKLOAD","NODE_CNT","CC_ALG","TXN_WRITE_PERC","TUP_WRITE_PERC","MAX_TXN_IN_FLIGHT"]
#    exp = [[wl,n,cc,wr,wr2,tif] for n,cc,wr,wr2,tif in itertools.product(nnodes,nalgos,nwr,nwr2,ntif)]

    return fmt,exp

def test2():
    nnodes = [1,2,4]
    nwr = [0.2]
    nalgos=['NO_WAIT','WAIT_DIE','MAAT','OCC']
#    nalgos=['MVCC','TIMESTAMP','CALVIN']
#    nnodes = [2]
#    nalgos=['OCC']

    wl = 'TPCC'
    fmt = ["WORKLOAD","NODE_CNT","CC_ALG","TUP_WRITE_PERC","MAX_TXN_IN_FLIGHT","NUM_WH","PERC_PAYMENT"]
    exp = [[wl,n,cc,wr,10000,128,1.0] for n,cc,wr in itertools.product(nnodes,nalgos,nwr)]
    return fmt,exp


def test_plot(summary,summary_client):
    from helper import plot_prep
    from plot_helper import tput,time_breakdown
    nfmt,nexp = test()
    x_name = "CC_ALG"
    x_name = "NODE_CNT"
    v_name = "TXN_WRITE_PERC"
    v_name = "CC_ALG"
#    tput_setup(summary,summary_client,nfmt,nexp,x_name,v_name)
#    skew = [0.6,0.7]
#    txn_write_perc = [0.5,1.0]
    txn_write_perc = [0.0,0.25,0.5,0.75,1.0] # TXN_WRITE_PERC
    txn_write_perc = [0.0,0.5,1.0] # TXN_WRITE_PERC
    txn_write_perc = [0.5] # TXN_WRITE_PERC
    skew = [0.6]
    skew = [0.6,0.7]
    nmodes=['true']
    nmodes=['true','false']
    title = ""
    const={}
#    x_vals,v_vals,fmt,exp,lst = plot_prep(nexp,nfmt,x_name,v_name,constants=const)
#    tput(x_vals,v_vals,summary,summary_client,cfg_fmt=fmt,cfg=list(exp),xname=x_name,vname=v_name,xlab="Server Count",new_cfgs=lst,ylimit=140,logscalex=False,title=title)
#    for sk,mode in itertools.product(skew,nmodes):
    for sk,mode,wr in itertools.product(skew,nmodes,txn_write_perc):
        const={"ZIPF_THETA":sk,"YCSB_ABORT_MODE":mode,"TXN_WRITE_PERC":wr}
        title = ""
        for c in const.keys():
            title += "{} {},".format(SHORTNAMES[c],const[c])
        x_vals,v_vals,fmt,exp,lst = plot_prep(nexp,nfmt,x_name,v_name,constants=const)
        tput(x_vals,v_vals,summary,summary_client,cfg_fmt=fmt,cfg=list(exp),xname=x_name,vname=v_name,xlab="Server Count",new_cfgs=lst,ylimit=140,logscalex=False,title=title)

def test2_plot(summary,summary_client):
    nfmt,nexp = test2()
    x_name = "NODE_CNT"
    v_name = "CC_ALG"
    tput_setup(summary,summary_client,nfmt,nexp,x_name,v_name,title="TPCC")

def tputvlat_setup(summary,summary_cl,nfmt,nexp,x_name,v_name):
    from plot_helper import tput_v_lat
    x_vals = []
    v_vals = []
    exp = [list(e) for e in nexp]
    fmt = list(nfmt)
    print(x_name)
    print(v_name)
    for e in exp:
        x_vals.append(e[fmt.index(x_name)])
        del e[fmt.index(x_name)]
    fmt.remove(x_name)
    for e in exp:
        v_vals.append(e[fmt.index(v_name)])
        del e[fmt.index(v_name)]
    fmt.remove(v_name)
    x_vals = list(set(x_vals))
    x_vals.sort()
    v_vals = list(set(v_vals))
    v_vals.sort()
    exp.sort()
    exp = list(k for k,_ in itertools.groupby(exp))
    for e in exp:
        title = "Tput vs Lat "
        for t in fmt_title:
            if t not in fmt: continue
            title+="{} {}, ".format(SHORTNAMES[t],e[fmt.index(t)])
        tput_v_lat(x_vals,v_vals,summary,summary_cl,cfg_fmt=fmt,cfg=e,xname=x_name,vname=v_name,title=title)


def tput_setup(summary,summary_cl,nfmt,nexp,x_name,v_name
        ,extras={}
        ,title=""
#        ,extras={'PART_CNT':'NODE_CNT','CLIENT_NODE_CNT':'NODE_CNT','PART_PER_TXN':'NODE_CNT'}
        ):
    from plot_helper import tput
    x_vals = []
    v_vals = []
    exp = [list(e) for e in nexp]
    fmt = list(nfmt)
    print(x_name)
    print(v_name)
    for e in exp:
        x_vals.append(e[fmt.index(x_name)])
        del e[fmt.index(x_name)]
    fmt.remove(x_name)
    for e in exp:
        v_vals.append(e[fmt.index(v_name)])
        del e[fmt.index(v_name)]
    fmt.remove(v_name)
    for x in extras.keys():
        if x not in fmt: 
            del extras[x]
            continue
        for e in exp:
            del e[fmt.index(x)]
        fmt.remove(x)
    x_vals = list(set(x_vals))
    x_vals.sort()
    v_vals = list(set(v_vals))
    v_vals.sort()
    exp.sort()
    exp = list(k for k,_ in itertools.groupby(exp))
    for e in exp:
#        if "PART_PER_TXN" in fmt and e[fmt.index("PART_PER_TXN")] == 1 and ("NODE_CNT" == x_name or "NODE_CNT" == v_name):
#            continue
#title = "System Tput "
        _title = ""
        if title == "":
            for t in fmt_title:
                if t not in fmt: continue
                _title+="{} {} ".format(SHORTNAMES[t],e[fmt.index(t)])
        else:
            _title = title
        tput(x_vals,v_vals,summary,summary_cl,cfg_fmt=fmt,cfg=list(e),xname=x_name,vname=v_name,title=_title,extras=extras)

def line_rate_setup(summary,summary_cl,nfmt,nexp,x_name,v_name,key
        ,extras={}
        ):
    from plot_helper import line_rate
    x_vals = []
    v_vals = []
    exp = [list(e) for e in nexp]
    fmt = list(nfmt)
    print(x_name)
    print(v_name)
    for e in exp:
        x_vals.append(e[fmt.index(x_name)])
        del e[fmt.index(x_name)]
    fmt.remove(x_name)
    for e in exp:
        v_vals.append(e[fmt.index(v_name)])
        del e[fmt.index(v_name)]
    fmt.remove(v_name)
    for x in extras.keys():
        if x not in fmt: continue
        for e in exp:
            del e[fmt.index(x)]
        fmt.remove(x)
    x_vals = list(set(x_vals))
    x_vals.sort()
    v_vals = list(set(v_vals))
    v_vals.sort()
    exp.sort()
    exp = list(k for k,_ in itertools.groupby(exp))
    for e in exp:
        title = key 
        for t in fmt_title:
            if t not in fmt: continue
            title+="{} {}, ".format(t,e[fmt.index(t)])
        line_rate(x_vals,v_vals,summary,summary_cl,key,cfg_fmt=fmt,cfg=list(e),xname=x_name,vname=v_name,title=title,extras=extras)
     
def line_setup(summary,summary_cl,nfmt,nexp,x_name,v_name,key
        ,extras={}
        ):
    from plot_helper import line_general
    x_vals = []
    v_vals = []
    exp = [list(e) for e in nexp]
    fmt = list(nfmt)
    print(x_name)
    print(v_name)
    for e in exp:
        x_vals.append(e[fmt.index(x_name)])
        del e[fmt.index(x_name)]
    fmt.remove(x_name)
    for e in exp:
        v_vals.append(e[fmt.index(v_name)])
        del e[fmt.index(v_name)]
    fmt.remove(v_name)
    for x in extras.keys():
        if x not in fmt: continue
        for e in exp:
            del e[fmt.index(x)]
        fmt.remove(x)
    x_vals = list(set(x_vals))
    x_vals.sort()
    v_vals = list(set(v_vals))
    v_vals.sort()
    exp.sort()
    exp = list(k for k,_ in itertools.groupby(exp))
    for e in exp:
        title = key 
        for t in fmt_title:
            if t not in fmt: continue
            title+="{} {}, ".format(t,e[fmt.index(t)])
        line_general(x_vals,v_vals,summary,summary_cl,key,cfg_fmt=fmt,cfg=list(e),xname=x_name,vname=v_name,title=title,extras=extras)
        
def stacks_setup(summary,nfmt,nexp,x_name,keys,key_names=[],norm=False
        ,extras={}
        ):
    from plot_helper import stacks_general
    x_vals = []
    exp = [list(e) for e in nexp]
    fmt = list(nfmt)
    print(x_name)
    print(keys)
    for e in exp:
        x_vals.append(e[fmt.index(x_name)])
        del e[fmt.index(x_name)]
    fmt.remove(x_name)
    for x in extras.keys():
        if x not in fmt: continue
        for e in exp:
            del e[fmt.index(x)]
        fmt.remove(x)
    x_vals = list(set(x_vals))
    x_vals.sort()
    exp.sort()
    exp = list(k for k,_ in itertools.groupby(exp))
    for e in exp:
        title = "Stacks "
        for t in fmt_title:
            if t not in fmt: continue
            title+="{} {}, ".format(t,e[fmt.index(t)])
        stacks_general(x_vals,summary,list(keys),xname=x_name,key_names=list(key_names),title=title,cfg_fmt=fmt,cfg=list(e),extras=extras)

def breakdown_setup(summary,nfmt,nexp,x_name,key_names=[],norm=False
        ,extras={}
        ):
    from plot_helper import time_breakdown
    x_vals = []
    exp = [list(e) for e in nexp]
    fmt = list(nfmt)
    print('Breakdown Setup: {}'.format(x_name))
    for e in exp:
        x_vals.append(e[fmt.index(x_name)])
        del e[fmt.index(x_name)]
    fmt.remove(x_name)
    for x in extras.keys():
        if x not in fmt: continue
        for e in exp:
            del e[fmt.index(x)]
        fmt.remove(x)
    x_vals = list(set(x_vals))
    x_vals.sort()
    exp.sort()
    exp = list(k for k,_ in itertools.groupby(exp))
    for e in exp:
        title = "Breakdown "
        for t in fmt_title:
            if t not in fmt: continue
            title+="{} {}, ".format(t,e[fmt.index(t)])
        time_breakdown(x_vals,summary,xname=x_name,title=title,cfg_fmt=fmt,cfg=list(e),extras=extras,normalized=norm)


def ft_mode_plot(summary,summary_client):
    nfmt,nexp = ft_mode()
    x_name = "MAX_TXN_IN_FLIGHT"
    v_name = "CC_ALG"
    tput_setup(summary,nfmt,nexp,x_name,v_name)

def test_plot3(summary,summary_client):
    nfmt,nexp = test()
#    tput_setup(summary,summary_client,nfmt,nexp,x_name="MAX_TXN_IN_FLIGHT",v_name="MODE")
    tput_setup(summary,summary_client,nfmt,nexp,x_name="NODE_CNT",v_name="MODE",extras={'PART_CNT':'NODE_CNT','CLIENT_NODE_CNT':'NODE_CNT','PART_PER_TXN':'NODE_CNT','NUM_WH':128,'PERC_PAYMENT':0.0})
#    tput_setup(summary,summary_client,nfmt,nexp,x_name="NODE_CNT",v_name="ZIPF_THETA")
#    tput_setup(summary,summary_client,nfmt,nexp,x_name="NODE_CNT",v_name="CC_ALG")
#    tput_setup(summary,summary_client,nfmt,nexp,x_name="NODE_CNT",v_name="MPR")
#    tput_setup(summary,summary_client,nfmt,nexp,x_name="NODE_CNT",v_name="MAX_TXN_IN_FLIGHT")
#    tput_setup(summary,summary_client,nfmt,nexp,x_name="MAX_TXN_IN_FLIGHT",v_name="NODE_CNT")

#    breakdown_setup(summary,nfmt,nexp,x_name="NODE_CNT",norm=True)
#    tput_setup(summary,summary_client,nfmt,nexp,x_name="WRITE_PERC",v_name="ZIPF_THETA")
#    tput_setup(summary,summary_client,nfmt,nexp,x_name="WRITE_PERC",v_name="ACCESS_PERC")
#    tput_setup(summary,summary_client,nfmt,nexp,x_name="NODE_CNT",v_name="WRITE_PERC")
#    tput_setup(summary,summary_client,nfmt,nexp,x_name="ACCESS_PERC",v_name="WRITE_PERC")

#    line_rate_setup(summary,summary_client,nfmt,nexp,x_name="MAX_TXN_IN_FLIGHT",v_name="CC_ALG",key='abort_cnt')
#    line_setup(summary,summary_client,nfmt,nexp,x_name="MAX_TXN_IN_FLIGHT",v_name="NODE_CNT",key='thd1')
#    line_setup(summary,summary_client,nfmt,nexp,x_name="MAX_TXN_IN_FLIGHT",v_name="NODE_CNT",key='txn_cnt')
#    line_rate_setup(summary,summary_client,nfmt,nexp,x_name="MAX_TXN_IN_FLIGHT",v_name="CC_ALG",key='abort_cnt')
#    line_setup(summary,summary_client,nfmt,nexp,x_name="MAX_TXN_IN_FLIGHT",v_name="CC_ALG",key='tot_avg_abort_row_cnt')
#    line_setup(summary,summary_client,nfmt,nexp,x_name="MAX_TXN_IN_FLIGHT",v_name="CC_ALG",key='time_validate')
#    line_setup(summary,summary_client,nfmt,nexp,x_name="NODE_CNT",v_name="ACCESS_PERC",key='cpu_ttl')
#    line_setup(summary,summary_client,nfmt,nexp,x_name="NODE_CNT",v_name="NODE_CNT",key='abort_cnt')
#    line_setup(summary,summary_client,nfmt,nexp,x_name="NODE_CNT",v_name="CC_ALG",key='tot_avg_abort_row_cnt')
#    line_rate_setup(summary,summary_client,nfmt,nexp,x_name="NODE_CNT",v_name="ACCESS_PERC",key='abort_cnt')
#    line_setup(summary,summary_client,nfmt,nexp,x_name="NODE_CNT",v_name="ACCESS_PERC",key='avg_abort_row_cnt')
#    line_rate_setup(summary,summary_client,nfmt,nexp,x_name="NODE_CNT",v_name="CC_ALG",key='mpq_cnt')
#    line_rate_setup(summary,summary_client,nfmt,nexp,x_name="NODE_CNT",v_name="CC_ALG",key='abort_cnt')
#    line_setup(summary,summary_client,nfmt,nexp,x_name="NODE_CNT",v_name="CC_ALG",key='avg_abort_row_cnt')
#    line_rate_setup(summary,summary_client,nfmt,nexp,x_name="NODE_CNT",v_name="NODE_CNT",key='abort_cnt')
#    line_setup(summary,summary_client,nfmt,nexp,x_name="NODE_CNT",v_name="NODE_CNT",key='latency')
#    line_setup(summary,summary_client,nfmt,nexp,x_name="NODE_CNT",v_name="ACCESS_PERC",key='cflt_cnt')
#    line_setup(summary,summary_client,nfmt,nexp,x_name="NODE_CNT",v_name="ACCESS_PERC",key='busy_cnt')
#    line_setup(summary,summary_client,nfmt,nexp,x_name="NODE_CNT",v_name="ACCESS_PERC",key='txn_cnt')
#    line_setup(summary,summary_client,nfmt,nexp,x_name="NODE_CNT",v_name="ACCESS_PERC",key='virt_mem_usage')
#    line_setup(summary,summary_client,nfmt,nexp,x_name="NODE_CNT",v_name="ACCESS_PERC",key='time_abort')
#    line_setup(summary,summary_client,nfmt,nexp,x_name="NODE_CNT",v_name="ACCESS_PERC",key='abort_from_ts')
#    line_setup(summary,summary_client,nfmt,nexp,x_name="NODE_CNT",v_name="ACCESS_PERC",key='time_validate')
#    tputvlat_setup(summary,summary_client,nfmt,nexp,x_name="NODE_CNT",v_name="MODE")

#    stacks_setup(summary,nfmt,nexp,x_name="MAX_TXN_IN_FLIGHT",keys=['thd1','thd2','thd3'],norm=False)
#    stacks_setup(summary,nfmt,nexp,x_name="MAX_TXN_IN_FLIGHT",keys=['txn_table_add','txn_table_get','txn_table0a','txn_table1a','txn_table0b','txn_table1b','txn_table2a','txn_table2'],norm=False)
#    stacks_setup(summary,nfmt,nexp,x_name="MAX_TXN_IN_FLIGHT"            ,keys=['type1','type2','type3','type4','type5','type6','type7','type8','type9','type10','type11','type12','type13','type14']            ,norm=False)
#    stacks_setup(summary,nfmt,nexp,x_name="MAX_TXN_IN_FLIGHT",keys=['thd1a','thd1b','thd1c','thd1d'],norm=False)
#    stacks_setup(summary,nfmt,nexp,x_name="MAX_TXN_IN_FLIGHT",keys=['rtxn1a','rtxn1b','rtxn2','rtxn3','rtxn4'],norm=False)

#    stacks_setup(summary,nfmt,nexp,x_name="NODE_CNT",keys=['thd1','thd2','thd3'],norm=False,key_names=['Getting work','Execution','Wrap-up'])
#    stacks_setup(summary,nfmt,nexp,x_name="NODE_CNT",keys=['txn_table_add','txn_table_get','txn_table_mints1','txn_table_mints2','txn_table0a','txn_table1a','txn_table0b','txn_table1b','txn_table2a'],norm=False)
#    stacks_setup(summary,nfmt,nexp,x_name="NODE_CNT",keys=['type1','type2','type3','type4','type5','type6','type7','type8','type9','type10','type11','type12','type13','type14'],key_names=['DONE','LOCK','UNLOCK','Rem QRY','FIN','LOCK RSP','UNLOCK RSP','QRY RSP','ACK','Exec','INIT','PREP','PASS','CLIENT'],norm=False)
#    stacks_setup(summary,nfmt,nexp,x_name="NODE_CNT",keys=['occ_val1','occ_val2a','occ_val2','occ_val3','occ_val4','occ_val5'],norm=False)
 #   stacks_setup(summary,nfmt,nexp,x_name="NODE_CNT",keys=['mvcc1','mvcc2','mvcc3','mvcc4','mvcc5','mvcc6','mvcc7','mvcc8'],norm=False)
#    stacks_setup(summary,nfmt,nexp,x_name="NODE_CNT",keys=['thd1','thd2','thd3'],norm=False,key_names=['Getting work','Execution','Wrap-up'])
#    stacks_setup(summary,nfmt,nexp,x_name="NODE_CNT",keys=['txn_table_add','txn_table_get','txn_table_mints1','txn_table_mints2','txn_table0a','txn_table1a','txn_table0b','txn_table1b','txn_table2a'],norm=False)
#    stacks_setup(summary,nfmt,nexp,x_name="NODE_CNT",keys=['type1','type2','type3','type4','type5','type6','type7','type8','type9','type10','type11','type12','type13','type14'],key_names=['DONE','LOCK','UNLOCK','Rem QRY','FIN','LOCK RSP','UNLOCK RSP','QRY RSP','ACK','Exec','INIT','PREP','PASS','CLIENT'],norm=False)
#    stacks_setup(summary,nfmt,nexp,x_name="NODE_CNT",keys=['occ_val1','occ_val2a','occ_val2','occ_val3','occ_val4','occ_val5'],norm=False)
#    stacks_setup(summary,nfmt,nexp,x_name="NODE_CNT",keys=['mvcc1','mvcc2','mvcc3','mvcc4','mvcc5','mvcc6','mvcc7','mvcc8'],norm=False)
#    stacks_setup(summary,nfmt,nexp,x_name="WRITE_PERC",keys=['thd1a','thd1c','thd1d'],key_names=['Prog stats','Spinning','Abort queue'],norm=False)
#    stacks_setup(summary,nfmt,nexp,x_name="MODE",keys=['rtxn1a','rtxn1b','rtxn2','rtxn3','rtxn4'],norm=False)
#    stacks_setup(summary,nfmt,nexp,x_name="MODE",keys=['row1','row2','row3'],norm=False)

#    line_setup(summary,summary_client,nfmt,nexp,x_name="MAX_TXN_IN_FLIGHT",v_name="MODE",key='cpu_ttl')

#    stacks_setup(summary,nfmt,nexp,x_name="NODE_CNT",keys=['thd1','thd2','thd3'],norm=False,key_names=['Prep work','Execution','Wrap-up'])
#    stacks_setup(summary,nfmt,nexp,x_name="NODE_CNT",keys=['txn_table_add','txn_table_get','txn_table0a','txn_table1a','txn_table0b','txn_table1b','txn_table2a'],norm=False)

#    stacks_setup(summary,nfmt,nexp,x_name="NODE_CNT"
#            ,keys=['type4','type5','type8','type9','type10','type12']
#            ,key_names=['REM QRY','FIN','QRY RSP','ACK','Exec','PREP']
#            ,norm=False)

#    stacks_setup(summary,nfmt,nexp,x_name="NODE_CNT"
#            ,keys=['type1','type2','type3','type4','type5','type6','type7','type8','type9','type10','type11','type12','type13','type14']
#            ,key_names=['DONE','LOCK','UNLOCK','Rem QRY','FIN','LOCK RSP','UNLOCK RSP','QRY RSP','ACK','Exec','INIT','PREP','PASS','CLIENT']
#            ,norm=False)
#    stacks_setup(summary,nfmt,nexp,x_name="CC_ALG",keys=['thd1a','thd1b','thd1c','thd1d'],norm=False)
#    stacks_setup(summary,nfmt,nexp,x_name="NODE_CNT",keys=['rtxn1a','rtxn1b','rtxn2','rtxn3','rtxn4'],norm=False)
#    stacks_setup(summary,nfmt,nexp,x_name="NODE_CNT",keys=['row1','row2','row3'],norm=False)
#    line_setup(summary,summary_client,nfmt,nexp,x_name="MAX_TXN_IN_FLIGHT",v_name="MODE",key='mbuf_send_time')
#    line_setup(summary,summary_client,nfmt,nexp,x_name="MAX_TXN_IN_FLIGHT",v_name="MODE",key='avg_msg_batch')
#    line_setup(summary,summary_client,nfmt,nexp,x_name="MAX_TXN_IN_FLIGHT",v_name="MODE",key='txn_cnt')
#    line_setup(summary,summary_client,nfmt,nexp,x_name="MAX_TXN_IN_FLIGHT",v_name="MODE",key='time_tport_send')
#    line_setup(summary,summary_client,nfmt,nexp,x_name="MAX_TXN_IN_FLIGHT",v_name="MODE",key='time_tport_rcv')
#    line_setup(summary,summary_client,nfmt,nexp,x_name="MAX_TXN_IN_FLIGHT",v_name="MODE",key='time_tport_rcv')

def network_sweep():
    wl = 'YCSB'
    nalgos=['NO_WAIT','WAIT_DIE','OCC','MVCC','TIMESTAMP','CALVIN']
#    nalgos=['NO_WAIT','MVCC','OCC']
    ndelay=[0,2000,4000,6000,8000,10000,12000,14000,16000,18000,20000,22000,24000,26000,28000,30000]#,32000,34000,36000,38000,40000,42000,44000,46000,48000,50000]#,22000,24000,26000,28000,30000,40000,50000,60000,70000,80000,90000,100000]
    ndelay=[0,0.05,0.1,0.25,0.5,0.75,1,1.75,2.5,5,7.5,10,12.5,15,17.5,20,22.5,25,27.5,30,32.5,35,37.5,40,42.5,45,47.5,50]
    ndelay=[0,0.05,0.1,0.25,0.5,0.75,1,1.75,2.5,5,7.5,10,12.5,15,17.5,20,25,30,35,40,45,50]
    ndelay=[0,0.1,1,10]
    ndelay = [n*1000000 for n in ndelay]
    fmt = ["WORKLOAD","NODE_CNT","CC_ALG","PART_PER_TXN","NETWORK_DELAY","SET_AFFINITY"]
    exp = [[wl,8,cc,2,d,"false"] for d,cc in itertools.product(ndelay,nalgos)]
    return fmt,exp

def network_sweep_plot(summary,summary_client):
    from helper import plot_prep
    from plot_helper import tput
    nfmt,nexp = network_sweep()
    tput_setup(summary,summary_client,nfmt,nexp,x_name="NETWORK_DELAY",v_name="CC_ALG",extras={'PART_CNT':'NODE_CNT','CLIENT_NODE_CNT':'NODE_CNT'},logscalex=True)

def network_experiment():
    fmt_nt = ["NODE_CNT","CLIENT_NODE_CNT","NETWORK_TEST"]
    nnodes = [1]
    cnodes = [1]
    ntest = ["true"]
    exp = [nnodes,cnodes,ntest]
    exp = [[n,c,t] for n,c,t in itertools.product(nnodes,cnodes,ntest)]
    return fmt_nt,exp

def network_experiment_plot(all_exps,all_nodes,timestamps):
    from plot_helper import lat_node_tbls,lat_tbl
    fmt = fmt_nt
    nnodes = [1]
    cnodes = [1]
    ntest = ["true"]
    rexp = [nnodes,cnodes,ntest]
    rexp = [[n,c,t] for n,c,t in itertools.product(nnodes,cnodes,ntest)]
    for i,exp in enumerate(all_exps):
        lat_node_tbls(exp[:-1],all_nodes[i],exp[0].keys(),timestamps[i])
        lat_tbl(exp[-1],exp[-1].keys(),timestamps[i])


def network_test():
    wl = 'YCSB'
    nnodes = [1]
    nalgos=['NO_WAIT']
    fmt = ["WORKLOAD","NODE_CNT","CC_ALG","NETWORK_TEST","SET_AFFINITY"]
    exp = [[wl,n,cc,'true','false'] for n,cc in itertools.product(nnodes,nalgos)]
    return fmt,exp


experiment_map = {
    'network_test':network_test,
    'ycsb_scaling': ycsb_scaling,
    'ycsb_scaling_plot': ycsb_scaling_plot,
    'ycsb_skew': ycsb_skew,
    'ycsb_skew_plot': ycsb_skew_plot,
    'isolation_levels': isolation_levels,
    'isolation_levels_plot': isolation_levels_plot,
    'ycsb_partitions': ycsb_partitions,
#    'ycsb_partitions_plot': ycsb_partitions_plot,
    'ycsb_load': ycsb_load,
    'tpcc_scaling': tpcc_scaling,
#    'tpcc_scaling_plot': tpcc_scaling_plot,
#    'tpcc_scaling_whset_plot': tpcc_scaling_whset_plot,
    'test': test,
    'test_plot': test_plot,
    'test2': test2,
    'test2_plot': test2_plot,
    'network_sweep': network_sweep,
    'network_sweep_plot': network_sweep_plot,
}


# Default values for variable configurations
configs = {
    "NODE_CNT" : 16,
    "THREAD_CNT": 4,
    "REPLICA_CNT": 0,
    "REPLICA_TYPE": "AP",
    "REM_THREAD_CNT": "THREAD_CNT",
    "SEND_THREAD_CNT": "THREAD_CNT",
    "CLIENT_NODE_CNT" : "NODE_CNT",
    "CLIENT_THREAD_CNT" : 4,
    "CLIENT_REM_THREAD_CNT" : 2,
    "CLIENT_SEND_THREAD_CNT" : 2,
    "MAX_TXN_PER_PART" : 500000,
#    "MAX_TXN_PER_PART" : 1,
    "WORKLOAD" : "YCSB",
    "CC_ALG" : "WAIT_DIE",
    "MPR" : 1.0,
    "TPORT_TYPE":"IPC",
    "TPORT_PORT":"17000",#"63200",
    "PART_CNT": "NODE_CNT", #2,
    "PART_PER_TXN": "PART_CNT",
    "MAX_TXN_IN_FLIGHT": 100,
    "NETWORK_DELAY": '0UL',
    "DONE_TIMER": "1 * 60 * BILLION // ~1 minutes",
#    "DONE_TIMER": "1 * 10 * BILLION // ~1 minutes",
    "WARMUP_TIMER": "1 * 60 * BILLION // ~1 minutes",
#    "WARMUP_TIMER": "0 * 60 * BILLION // ~1 minutes",
    "SEQ_BATCH_TIMER": "5 * 1 * MILLION // ~5ms -- same as CALVIN paper",
    "BATCH_TIMER" : "0",#"10000000",
    "PROG_TIMER" : "10 * BILLION // in s",
    "NETWORK_TEST" : "false",
    "ABORT_PENALTY": "10 * 1000000UL   // in ns.",
    "ABORT_PENALTY_MAX": "5 * 100 * 1000000UL   // in ns.",
    "MSG_TIME_LIMIT": "0",#"10 * 1000000UL",
    "MSG_SIZE_MAX": 4096,
#    "PRT_LAT_DISTR": "true",
    "TXN_WRITE_PERC":0.0,
    "PRIORITY":"PRIORITY_ACTIVE",
    "TWOPL_LITE":"false",
#YCSB
    "INIT_PARALLELISM" : 8, 
    "TUP_WRITE_PERC":0.0,
    "ZIPF_THETA":0.3,
    "ACCESS_PERC":0.03,
    "DATA_PERC": 100,
    "REQ_PER_QUERY": 10, #16
    "SYNTH_TABLE_SIZE":"65536",
#    "SYNTH_TABLE_SIZE":"2097152*8",
#TPCC
    "NUM_WH": 'PART_CNT',
    "PERC_PAYMENT":0.0,
    "DEBUG_DISTR":"false",
#    "DEBUG_DISTR":"true",
#    "DEBUG_ALLOC":"true",
    "DEBUG_ALLOC":"false",
    "DEBUG_RACE":"false",
    "MODE":"NORMAL_MODE",
    "SHMEM_ENV":"false",
    "STRICT_PPT":0,
    "SET_AFFINITY":"true",
    "LOGGING":"false",
    "SIM_FULL_ROW":"false",
    "SERVER_GENERATE_QUERIES":"false",
    "SKEW_METHOD":"ZIPF",
    "ENVIRONMENT_EC2":"false",
    "YCSB_ABORT_MODE":"false",
    "LOAD_METHOD": "LOAD_MAX", #"LOAD_RATE","LOAD_MAX"
    "ISOLATION_LEVEL":"SERIALIZABLE"
}

