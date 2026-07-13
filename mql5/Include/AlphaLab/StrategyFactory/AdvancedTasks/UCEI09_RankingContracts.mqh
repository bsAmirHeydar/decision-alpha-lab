#ifndef __UCEI09_RANKING_CONTRACTS_MQH__
#define __UCEI09_RANKING_CONTRACTS_MQH__
struct UCEI09_RankingPair{string pair_id;string group_id;string preferred_row_id;string other_row_id;double weight;double utility_gap;bool Valid()const{return pair_id!="" && group_id!="" && preferred_row_id!=other_row_id && weight>0.0 && utility_gap>0.0;}};
struct UCEI09_RankingMetricReport{string report_id;int group_count;int row_count;int pair_count;double pairwise_accuracy;double mean_ndcg_at_k;double mean_map_at_k;double mean_top_k_utility;int k;string evidence_hash;bool Valid()const{return report_id!="" && group_count>0 && row_count>0 && k>0 && pairwise_accuracy>=0.0 && pairwise_accuracy<=1.0;}};
#endif
