#include "remote_query.h"
#include "mem_alloc.h"
#include "tpcc.h"
#include "tpcc_query.h"
#include "query.h"
#include "transport.h"
#include "plock.h"

void Remote_query::init(uint64_t node_id, workload * wl) {
	q_idx = 0;
	_node_id = node_id;
	_wl = wl;
  pthread_mutex_init(&mtx,NULL);
}

txn_man * Remote_query::get_txn_man(uint64_t thd_id, uint64_t node_id, uint64_t txn_id) {

  txn_man * next_txn = NULL;

  return next_txn;
}

void Remote_query::remote_qry(base_query * query, int type, int dest_id, txn_man * txn) {
#if WORKLOAD == TPCC
	tpcc_query * m_query = (tpcc_query *) query;
	m_query->remote_qry(query,type,dest_id);
#endif
}

void Remote_query::ack_response(RC rc, txn_man * txn) {

	// Maximum number of parameters
	// NOTE: Adjust if parameters sent is changed
#if DEBUG_DISTR
  printf("Sending RACK-1 %ld\n",txn->get_txn_id());
#endif
  uint64_t total = 3;
	void ** data = new void *[total];
	int * sizes = new int [total];
	int num = 0;

  txnid_t txn_id = txn->get_txn_id();
  RC _rc =rc;
	RemReqType rtype = RACK;

	data[num] = &txn_id;
	sizes[num++] = sizeof(txnid_t);

	data[num] = &rtype;
	sizes[num++] = sizeof(RemReqType);

  data[num] = &_rc;
	sizes[num++] = sizeof(RC);

  send_remote_query(GET_NODE_ID(txn->get_pid()),data,sizes,num);
}
void Remote_query::ack_response(base_query * query) {

	// Maximum number of parameters
	// NOTE: Adjust if parameters sent is changed
#if DEBUG_DISTR
  printf("Sending RACK-2 %ld\n",query->txn_id);
#endif
  uint64_t total = 3;
	void ** data = new void *[total];
	int * sizes = new int [total];
	int num = 0;

  txnid_t txn_id = query->txn_id;
	RemReqType rtype = RACK;

	data[num] = &txn_id;
	sizes[num++] = sizeof(txnid_t);

	data[num] = &rtype;
	sizes[num++] = sizeof(RemReqType);

  data[num] = &query->rc;
	sizes[num++] = sizeof(RC);

  send_remote_query(query->return_id,data,sizes,num);
}

void Remote_query::send_init_done(uint64_t dest_id) {
  uint64_t total = 2;
	void ** data = new void *[total];
	int * sizes = new int [total];
  int num = 0;

  txnid_t txn_id = 0;
	RemReqType rtype = INIT_DONE;

	data[num] = &txn_id;
	sizes[num++] = sizeof(txnid_t);
	data[num] = &rtype;
	sizes[num++] = sizeof(RemReqType);
  send_remote_query(dest_id,data,sizes,num);
}

// FIXME: What if in HStore we want to lock multiple partitions at same node?
void Remote_query::send_init(base_query * query,uint64_t dest_part_id) {

	// Maximum number of parameters
	// NOTE: Adjust if parameters sent is changed
#if DEBUG_DISTR
  printf("Sending RINIT %ld\n",query->txn_id);
#endif
  uint64_t total = 3;
#if CC_ALG == HSTORE
  total += 3;
#endif
	void ** data = new void *[total];
	int * sizes = new int [total];
	int num = 0;

  txnid_t txn_id = query->txn_id;
	RemReqType rtype = RINIT;

	data[num] = &txn_id;
	sizes[num++] = sizeof(txnid_t);

	data[num] = &rtype;
	sizes[num++] = sizeof(RemReqType);

	data[num] = &query->ts;
	sizes[num++] = sizeof(ts_t);

#if CC_ALG == HSTORE
  uint64_t _dest_part_id = dest_part_id;
  uint64_t _part_id = GET_PART_ID(0,g_node_id);
  uint64_t _part_cnt = 1; // FIXME
	data[num] = &_part_id;
	sizes[num++] = sizeof(uint64_t);
	data[num] = &_part_cnt;
	sizes[num++] = sizeof(uint64_t);
	data[num] = &_dest_part_id;
	sizes[num++] = sizeof(uint64_t);
#endif

  send_remote_query(GET_NODE_ID(dest_part_id),data,sizes,num);
}

void Remote_query::send_remote_query(uint64_t dest_id, void ** data, int * sizes, int num) {
	tport_man.send_msg(dest_id, data, sizes, num);
}

void Remote_query::remote_rsp(base_query * query, txn_man * txn) {

#if WORKLOAD == TPCC
    tpcc_query * m_query = (tpcc_query *) query;
    m_query->remote_rsp(query);
#endif

}

void Remote_query::send_remote_rsp(uint64_t dest_id, void ** data, int * sizes, int num) {
	tport_man.send_msg(dest_id, data, sizes, num);
}

base_query * Remote_query::unpack(void * d, int len) {
  base_query * query;
	char * data = (char *) d;
	uint64_t ptr = 0;
  
  uint32_t dest_id;
  uint32_t return_id;
  txnid_t txn_id;
	RemReqType rtype;
  RC rc;

	memcpy(&dest_id,&data[ptr],sizeof(uint32_t));
	ptr += sizeof(uint32_t);
	memcpy(&return_id,&data[ptr],sizeof(uint32_t));
	ptr += sizeof(uint32_t);
	memcpy(&txn_id,&data[ptr],sizeof(txnid_t));
	ptr += sizeof(txnid_t);
	memcpy(&rtype,&data[ptr],sizeof(query->rtype));
	ptr += sizeof(query->rtype);
  

  if(rtype == RINIT || rtype == INIT_DONE) {
#if WORKLOAD == TPCC
	  query = (tpcc_query *) mem_allocator.alloc(sizeof(tpcc_query), 0);
    query->clear();
#endif
  } else {
    query = txn_pool.get_qry(g_node_id,txn_id);
  }

  query->dest_id = dest_id;
  query->return_id = return_id;
  query->txn_id = txn_id;
  query->rtype = rtype;

  /*
	memcpy(&query->dest_id,&data[ptr],sizeof(uint32_t));
	ptr += sizeof(uint32_t);
	memcpy(&query->return_id,&data[ptr],sizeof(uint32_t));
	ptr += sizeof(uint32_t);
	memcpy(&query->txn_id,&data[ptr],sizeof(txnid_t));
	ptr += sizeof(txnid_t);
	memcpy(&query->rtype,&data[ptr],sizeof(query->rtype));
	ptr += sizeof(query->rtype);
  */

	if(query->dest_id != _node_id)
		return NULL;

	switch(query->rtype) {
    case RINIT:
	    memcpy(&query->ts,&data[ptr],sizeof(ts_t));
	    ptr += sizeof(ts_t);
#if CC_ALG == HSTORE
	memcpy(&query->pid,&data[ptr],sizeof(query->pid));
	ptr += sizeof(query->pid);
	memcpy(&query->part_cnt,&data[ptr],sizeof(query->part_cnt));
	ptr += sizeof(query->part_cnt);
  assert(query->part_cnt == 1);
	query->parts = new uint64_t[query->part_cnt];
	for (uint64_t i = 0; i < query->part_cnt; i++) {
		memcpy(&query->parts[i],&data[ptr],sizeof(query->parts[i]));
		ptr += sizeof(query->parts[i]);
	}

#endif
      break;
    case RPREPARE:
      break;
#if CC_ALG == HSTORE
		case RLK:
		case RULK:
			part_lock_man.unpack(query,data);
			break;
		case RLK_RSP:
		case RULK_RSP: 
			part_lock_man.unpack_rsp(query,data);
			break;
#endif
		case RQRY: {
#if WORKLOAD == TPCC
			tpcc_query * m_query = new tpcc_query;
#endif
			m_query->unpack(query,data);
			break;
							 }
		case RQRY_RSP: {
#if WORKLOAD == TPCC
			tpcc_query * m_query = new tpcc_query;
#endif
			m_query->unpack_rsp(query,data);
			break;
									 }
    case RFIN:
      query->unpack_finish(query, data);
      break;
    case RACK:
	    memcpy(&rc,&data[ptr],sizeof(RC));
	    ptr += sizeof(RC);
      if(rc == Abort) {
        query->rc = rc;
      }
      break;
    case INIT_DONE:
      break;
		default:
			assert(false);
	}
  return query;
}

