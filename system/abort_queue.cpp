/*
   Copyright 2015 Rachael Harding

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

#include "mem_alloc.h"
#include "abort_queue.h"
#include "message.h"
#include "work_queue.h"

void AbortQueue::init() {
  pthread_mutex_init(&mtx,NULL);
}

// FIXME: Rewrite abort queue
void AbortQueue::enqueue(uint64_t txn_id, uint64_t abort_cnt) {
  uint64_t starttime = get_sys_clock();
  uint64_t penalty = g_abort_penalty;
#if BACKOFF
  penalty = max(penalty * 2^abort_cnt,g_abort_penalty_max);
#endif
  penalty += starttime;
  //abort_entry * entry = new abort_entry(penalty,txn_id);
  abort_entry * entry = (abort_entry*)mem_allocator.alloc(sizeof(abort_entry));
  entry->penalty_end = penalty;
  entry->txn_id = txn_id;
  pthread_mutex_lock(&mtx);
  DEBUG("AQ Enqueue %ld %f -- %f\n",entry->txn_id,float(penalty - starttime)/BILLION,simulation->seconds_from_start(starttime));
  INC_STATS(0,abort_queue_penalty,penalty - starttime);
  INC_STATS(0,abort_queue_enqueue_cnt,1);
  queue.push(entry);
  pthread_mutex_unlock(&mtx);
  
  INC_STATS(0,abort_queue_enqueue_time,get_sys_clock() - starttime);
}

void AbortQueue::process() {
  if(queue.empty())
    return;
  abort_entry * entry;
  pthread_mutex_lock(&mtx);
  uint64_t starttime = get_sys_clock();
  while(!queue.empty()) {
    entry = queue.top();
    if(entry->penalty_end < starttime) {
      queue.pop();
      // FIXME: add restart to work queue
      DEBUG("AQ Dequeue %ld %f -- %f\n",entry->txn_id,float(starttime - entry->penalty_end)/BILLION,simulation->seconds_from_start(starttime));
      INC_STATS(0,abort_queue_penalty_extra,starttime - entry->penalty_end);
      INC_STATS(0,abort_queue_dequeue_cnt,1);
      Message * msg = Message::create_message(RTXN);
      msg->txn_id = entry->txn_id;
      work_queue.enqueue(g_thread_cnt,msg,false);
      //entry = queue.top();
      mem_allocator.free(entry,sizeof(abort_entry));
    } else {
      break;
    }

  }
  pthread_mutex_unlock(&mtx);

  INC_STATS(0,abort_queue_dequeue_time,get_sys_clock() - starttime);

}
