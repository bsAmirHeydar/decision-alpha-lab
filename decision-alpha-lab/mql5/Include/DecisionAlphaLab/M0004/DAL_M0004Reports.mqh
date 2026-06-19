#ifndef __DAL_M0004_REPORTS_MQH__
#define __DAL_M0004_REPORTS_MQH__

#include <DecisionAlphaLab/M0002/DAL_M0002Reports.mqh>

#define DAL_M0004_LABEL_REVERSAL 0
#define DAL_M0004_LABEL_CONTINUATION 1

struct DALM0004Config
{
   int stress_iterations;
   int block_size;
   int placebo_lag_events;
   int regime_block_size_fast;
   int regime_block_size_slow;
   int circular_min_shift_events;
   int local_block_shuffle_size;
   int context_k_fast;
   int context_k_main;
   int context_k_slow;
   double context_ewma_alpha;
   double context_strong_threshold;
};

struct DALM0004TransitionStats
{
   int n;
   int transitions;
   int reversal_count;
   int continuation_count;
   int rr;
   int rc;
   int cr;
   int cc;
   double reversal_pct;
   double continuation_pct;
   double same_pct;
   double switch_pct;
   double iid_same_pct;
   double same_lift;
   double p_reversal_after_reversal;
   double p_continuation_after_reversal;
   double p_reversal_after_continuation;
   double p_continuation_after_continuation;
   double reversal_persistence_lift;
   double continuation_persistence_lift;
   double lag1_corr;
   double lag2_corr;
   double markov_chi2;
   double mutual_info_nats;
};

struct DALM0004RunStats
{
   int state;
   int n;
   int state_count;
   int run_count;
   int max_run;
   double state_pct;
   double avg_run;
   double iid_expected_avg_run;
   double avg_run_over_iid;
};

string DAL_M0004Prefix(
   const string tag,
   const string symbol,
   const string timeframe,
   const string source_mode,
   const int source_events,
   const datetime min_entry_time
)
{
   return tag
      + " *** symbol=" + symbol
      + "*tf=" + timeframe
      + "*source=" + source_mode
      + "*sourceEvents=" + IntegerToString(source_events)
      + "*analysisStart=" + DAL_M0001AnalysisStartText(min_entry_time)
      + " *** ";
}

double DAL_M0004SafeRatio(const double numerator, const double denominator)
{
   if(MathAbs(denominator) <= 0.000000000001)
      return 0.0;
   return numerator / denominator;
}

int DAL_M0004SampleSortKey(const DALM0002BranchSample &sample)
{
   if(sample.outcome_index >= 0)
      return sample.outcome_index;
   if(sample.exit_index >= 0)
      return sample.exit_index;
   return sample.entry_index;
}

bool DAL_M0004SampleBefore(const DALM0002BranchSample &a, const DALM0002BranchSample &b)
{
   int ka = DAL_M0004SampleSortKey(a);
   int kb = DAL_M0004SampleSortKey(b);
   if(ka != kb)
      return ka < kb;
   if(a.entry_index != b.entry_index)
      return a.entry_index < b.entry_index;
   return a.id < b.id;
}

void DAL_M0004SwapSamples(DALM0002BranchSample &a, DALM0002BranchSample &b)
{
   DALM0002BranchSample tmp = a;
   a = b;
   b = tmp;
}

void DAL_M0004QuickSortSamples(DALM0002BranchSample &samples[], int left, int right)
{
   int i = left;
   int j = right;
   DALM0002BranchSample pivot = samples[(left + right) / 2];

   while(i <= j)
   {
      while(DAL_M0004SampleBefore(samples[i], pivot))
         i++;
      while(DAL_M0004SampleBefore(pivot, samples[j]))
         j--;
      if(i <= j)
      {
         DAL_M0004SwapSamples(samples[i], samples[j]);
         i++;
         j--;
      }
   }

   if(left < j)
      DAL_M0004QuickSortSamples(samples, left, j);
   if(i < right)
      DAL_M0004QuickSortSamples(samples, i, right);
}

void DAL_M0004SortSamplesByOutcome(DALM0002BranchSample &samples[])
{
   int n = ArraySize(samples);
   if(n > 1)
      DAL_M0004QuickSortSamples(samples, 0, n - 1);
}

int DAL_M0004LabelFromOutcome(const ENUM_DALM0002Outcome outcome)
{
   if(outcome == DAL_M0002_OUTCOME_CONTINUATION_AFTER_EXIT)
      return DAL_M0004_LABEL_CONTINUATION;
   return DAL_M0004_LABEL_REVERSAL;
}

void DAL_M0004BuildLabelArrays(
   const DALM0002BranchSample &samples[],
   int &labels[],
   int &sessions[],
   int &trend_regimes[],
   int &revisit_ids[],
   double &prevols[],
   datetime &times[]
)
{
   int n = ArraySize(samples);
   ArrayResize(labels, n);
   ArrayResize(sessions, n);
   ArrayResize(trend_regimes, n);
   ArrayResize(revisit_ids, n);
   ArrayResize(prevols, n);
   ArrayResize(times, n);

   for(int i = 0; i < n; i++)
   {
      labels[i] = DAL_M0004LabelFromOutcome(samples[i].outcome);
      sessions[i] = samples[i].utc_session;
      trend_regimes[i] = samples[i].trend_regime;
      revisit_ids[i] = samples[i].revisit_id;
      prevols[i] = samples[i].pre_entry_vol;
      times[i] = samples[i].outcome_time;
   }
}

void DAL_M0004BuildPermutation(const int count, const int iter, const int salt, int &perm[])
{
   ArrayResize(perm, count);
   for(int i = 0; i < count; i++)
      perm[i] = i;

   for(int i = count - 1; i > 0; i--)
   {
      double frac = DAL_M0001RandomFractionK(iter + salt, count, count + salt * 23, i + salt * 37);
      int j = (int)MathFloor(frac * (i + 1));
      if(j < 0) j = 0;
      if(j > i) j = i;
      int tmp = perm[i];
      perm[i] = perm[j];
      perm[j] = tmp;
   }
}

double DAL_M0004LabelLagCorr(const int &labels[], const int count, const int lag)
{
   if(lag <= 0 || count <= lag + 2)
      return 0.0;

   int n = count - lag;
   double mean_x = 0.0;
   double mean_y = 0.0;
   for(int i = lag; i < count; i++)
   {
      mean_x += labels[i];
      mean_y += labels[i - lag];
   }
   mean_x /= n;
   mean_y /= n;

   double cov = 0.0;
   double vx = 0.0;
   double vy = 0.0;
   for(int i = lag; i < count; i++)
   {
      double x = labels[i] - mean_x;
      double y = labels[i - lag] - mean_y;
      cov += x * y;
      vx += x * x;
      vy += y * y;
   }
   if(vx <= 0.0 || vy <= 0.0)
      return 0.0;
   return cov / MathSqrt(vx * vy);
}

void DAL_M0004ComputeTransitionStats(const int &labels[], const int count, DALM0004TransitionStats &stats)
{
   stats.n = count;
   stats.transitions = MathMax(0, count - 1);
   stats.reversal_count = 0;
   stats.continuation_count = 0;
   stats.rr = 0;
   stats.rc = 0;
   stats.cr = 0;
   stats.cc = 0;

   for(int i = 0; i < count; i++)
   {
      if(labels[i] == DAL_M0004_LABEL_CONTINUATION)
         stats.continuation_count++;
      else
         stats.reversal_count++;
   }

   for(int i = 1; i < count; i++)
   {
      int prev = labels[i - 1];
      int cur = labels[i];
      if(prev == DAL_M0004_LABEL_REVERSAL && cur == DAL_M0004_LABEL_REVERSAL) stats.rr++;
      else if(prev == DAL_M0004_LABEL_REVERSAL && cur == DAL_M0004_LABEL_CONTINUATION) stats.rc++;
      else if(prev == DAL_M0004_LABEL_CONTINUATION && cur == DAL_M0004_LABEL_REVERSAL) stats.cr++;
      else if(prev == DAL_M0004_LABEL_CONTINUATION && cur == DAL_M0004_LABEL_CONTINUATION) stats.cc++;
   }

   double n = (double)MathMax(1, count);
   double t = (double)MathMax(1, stats.transitions);
   double p_r = stats.reversal_count / n;
   double p_c = stats.continuation_count / n;

   stats.reversal_pct = 100.0 * p_r;
   stats.continuation_pct = 100.0 * p_c;
   stats.same_pct = 100.0 * (stats.rr + stats.cc) / t;
   stats.switch_pct = 100.0 * (stats.rc + stats.cr) / t;
   stats.iid_same_pct = 100.0 * (p_r * p_r + p_c * p_c);
   stats.same_lift = stats.same_pct - stats.iid_same_pct;

   int r_prev = stats.rr + stats.rc;
   int c_prev = stats.cr + stats.cc;
   stats.p_reversal_after_reversal = r_prev > 0 ? 100.0 * stats.rr / r_prev : 0.0;
   stats.p_continuation_after_reversal = r_prev > 0 ? 100.0 * stats.rc / r_prev : 0.0;
   stats.p_reversal_after_continuation = c_prev > 0 ? 100.0 * stats.cr / c_prev : 0.0;
   stats.p_continuation_after_continuation = c_prev > 0 ? 100.0 * stats.cc / c_prev : 0.0;
   stats.reversal_persistence_lift = stats.p_reversal_after_reversal - stats.reversal_pct;
   stats.continuation_persistence_lift = stats.p_continuation_after_continuation - stats.continuation_pct;
   stats.lag1_corr = DAL_M0004LabelLagCorr(labels, count, 1);
   stats.lag2_corr = DAL_M0004LabelLagCorr(labels, count, 2);

   double a = stats.rr;
   double b = stats.rc;
   double c = stats.cr;
   double d = stats.cc;
   double row1 = a + b;
   double row2 = c + d;
   double col1 = a + c;
   double col2 = b + d;
   double denom = row1 * row2 * col1 * col2;
   if(denom > 0.0)
      stats.markov_chi2 = (a + b + c + d) * MathPow(a * d - b * c, 2.0) / denom;
   else
      stats.markov_chi2 = 0.0;

   stats.mutual_info_nats = 0.0;
   double total = a + b + c + d;
   if(total > 0.0)
   {
      double cells[4];
      double row_probs[2];
      double col_probs[2];
      cells[0] = a / total;
      cells[1] = b / total;
      cells[2] = c / total;
      cells[3] = d / total;
      row_probs[0] = row1 / total;
      row_probs[1] = row2 / total;
      col_probs[0] = col1 / total;
      col_probs[1] = col2 / total;
      for(int ri = 0; ri < 2; ri++)
      {
         for(int ci = 0; ci < 2; ci++)
         {
            int idx = ri * 2 + ci;
            double p = cells[idx];
            double expected = row_probs[ri] * col_probs[ci];
            if(p > 0.0 && expected > 0.0)
               stats.mutual_info_nats += p * MathLog(p / expected);
         }
      }
   }
}

void DAL_M0004ComputeRunStats(const int &labels[], const int count, const int state, DALM0004RunStats &rs)
{
   rs.state = state;
   rs.n = count;
   rs.state_count = 0;
   rs.run_count = 0;
   rs.max_run = 0;
   rs.state_pct = 0.0;
   rs.avg_run = 0.0;
   rs.iid_expected_avg_run = 0.0;
   rs.avg_run_over_iid = 0.0;

   int current = 0;
   int total_run_length = 0;
   for(int i = 0; i < count; i++)
   {
      if(labels[i] == state)
      {
         rs.state_count++;
         current++;
      }
      else
      {
         if(current > 0)
         {
            rs.run_count++;
            total_run_length += current;
            if(current > rs.max_run)
               rs.max_run = current;
            current = 0;
         }
      }
   }

   if(current > 0)
   {
      rs.run_count++;
      total_run_length += current;
      if(current > rs.max_run)
         rs.max_run = current;
   }

   if(count > 0)
      rs.state_pct = 100.0 * rs.state_count / count;
   if(rs.run_count > 0)
      rs.avg_run = (double)total_run_length / rs.run_count;

   double p = count > 0 ? (double)rs.state_count / count : 0.0;
   if(p < 1.0)
      rs.iid_expected_avg_run = 1.0 / (1.0 - p);
   else
      rs.iid_expected_avg_run = count;
   rs.avg_run_over_iid = DAL_M0004SafeRatio(rs.avg_run, rs.iid_expected_avg_run);
}

void DAL_M0004ComputeAllRunStats(const int &labels[], const int count, int &run_count, int &max_run, double &avg_run)
{
   run_count = 0;
   max_run = 0;
   avg_run = 0.0;
   if(count <= 0)
      return;

   int cur = 1;
   int sum_len = 0;
   for(int i = 1; i < count; i++)
   {
      if(labels[i] == labels[i - 1])
         cur++;
      else
      {
         run_count++;
         sum_len += cur;
         if(cur > max_run) max_run = cur;
         cur = 1;
      }
   }
   run_count++;
   sum_len += cur;
   if(cur > max_run) max_run = cur;
   avg_run = run_count > 0 ? (double)sum_len / run_count : 0.0;
}

string DAL_M0004TransitionText(const DALM0004TransitionStats &s)
{
   string inertia_model = "mixed_or_no_branch_label_inertia";
   if(s.same_lift > 0.0 && s.lag1_corr > 0.0 && s.reversal_persistence_lift > 0.0 && s.continuation_persistence_lift > 0.0)
      inertia_model = "both_branches_persistent_markov_regime";
   else if(s.same_lift > 0.0 && s.lag1_corr > 0.0)
      inertia_model = "positive_same_branch_inertia";

   return "TRANSITION_MATRIX"
      + "*n=" + IntegerToString(s.n)
      + "*transitions=" + IntegerToString(s.transitions)
      + "*reversalN=" + IntegerToString(s.reversal_count)
      + "*continuationN=" + IntegerToString(s.continuation_count)
      + "*reversalPct=" + DAL_M0001FmtPct(s.reversal_pct)
      + "*continuationPct=" + DAL_M0001FmtPct(s.continuation_pct)
      + "*RR=" + IntegerToString(s.rr)
      + "*RC=" + IntegerToString(s.rc)
      + "*CR=" + IntegerToString(s.cr)
      + "*CC=" + IntegerToString(s.cc)
      + "*samePct=" + DAL_M0001FmtPct(s.same_pct)
      + "*switchPct=" + DAL_M0001FmtPct(s.switch_pct)
      + "*iidSamePct=" + DAL_M0001FmtPct(s.iid_same_pct)
      + "*sameLiftPct=" + DAL_M0001FmtPct(s.same_lift)
      + "*pRevAfterRev=" + DAL_M0001FmtPct(s.p_reversal_after_reversal)
      + "*pContAfterRev=" + DAL_M0001FmtPct(s.p_continuation_after_reversal)
      + "*pRevAfterCont=" + DAL_M0001FmtPct(s.p_reversal_after_continuation)
      + "*pContAfterCont=" + DAL_M0001FmtPct(s.p_continuation_after_continuation)
      + "*revPersistenceLift=" + DAL_M0001FmtPct(s.reversal_persistence_lift)
      + "*contPersistenceLift=" + DAL_M0001FmtPct(s.continuation_persistence_lift)
      + "*lag1Corr=" + DAL_M0001Fmt4(s.lag1_corr)
      + "*lag2Corr=" + DAL_M0001Fmt4(s.lag2_corr)
      + "*markovChi2=" + DAL_M0001Fmt4(s.markov_chi2)
      + "*mutualInfoNats=" + DAL_M0001Fmt4(s.mutual_info_nats)
      + "*inertiaModel=" + inertia_model;
}

string DAL_M0004RunStatsText(const DALM0004RunStats &rev, const DALM0004RunStats &cont, const int all_run_count, const int all_max_run, const double all_avg_run)
{
   string run_model = "mixed_branch_runs";
   if(rev.avg_run_over_iid > 1.0 && cont.avg_run_over_iid > 1.0)
      run_model = "both_branches_run_cluster_above_iid";
   if(cont.avg_run_over_iid > rev.avg_run_over_iid && cont.avg_run > rev.avg_run)
      run_model = "continuation_run_persistence_stronger_than_reversal";

   return "BRANCH_RUNS"
      + "*allRunCount=" + IntegerToString(all_run_count)
      + "*allMaxRun=" + IntegerToString(all_max_run)
      + "*allAvgRun=" + DAL_M0001Fmt4(all_avg_run)
      + "*revN=" + IntegerToString(rev.state_count)
      + "*revRuns=" + IntegerToString(rev.run_count)
      + "*revMaxRun=" + IntegerToString(rev.max_run)
      + "*revAvgRun=" + DAL_M0001Fmt4(rev.avg_run)
      + "*revIidExpectedAvgRun=" + DAL_M0001Fmt4(rev.iid_expected_avg_run)
      + "*revAvgRunOverIid=" + DAL_M0001Fmt4(rev.avg_run_over_iid)
      + "*contN=" + IntegerToString(cont.state_count)
      + "*contRuns=" + IntegerToString(cont.run_count)
      + "*contMaxRun=" + IntegerToString(cont.max_run)
      + "*contAvgRun=" + DAL_M0001Fmt4(cont.avg_run)
      + "*contIidExpectedAvgRun=" + DAL_M0001Fmt4(cont.iid_expected_avg_run)
      + "*contAvgRunOverIid=" + DAL_M0001Fmt4(cont.avg_run_over_iid)
      + "*contMinusRevAvgRun=" + DAL_M0001Fmt4(cont.avg_run - rev.avg_run)
      + "*contOverRevAvgRun=" + DAL_M0001Fmt4(DAL_M0004SafeRatio(cont.avg_run, rev.avg_run))
      + "*runModel=" + run_model;
}

string DAL_M0004TransitionPermutationStressText(const int &labels[], const int count, const int iterations)
{
   if(count <= 5 || iterations <= 0)
      return "TRANSITION_PERM_STRESS*n=" + IntegerToString(count) + "*iters=0";

   DALM0004TransitionStats obs;
   DAL_M0004ComputeTransitionStats(labels, count, obs);

   int perm[];
   int tmp[];
   ArrayResize(tmp, count);
   double same_sum = 0.0, same_sumsq = 0.0;
   double lag_sum = 0.0, lag_sumsq = 0.0;
   int same_ge = 0;
   int lag_ge = 0;

   for(int iter = 0; iter < iterations; iter++)
   {
      DAL_M0004BuildPermutation(count, iter, 4401, perm);
      for(int i = 0; i < count; i++)
         tmp[i] = labels[perm[i]];

      DALM0004TransitionStats s;
      DAL_M0004ComputeTransitionStats(tmp, count, s);
      if(s.same_lift >= obs.same_lift) same_ge++;
      if(s.lag1_corr >= obs.lag1_corr) lag_ge++;
      same_sum += s.same_lift;
      same_sumsq += s.same_lift * s.same_lift;
      lag_sum += s.lag1_corr;
      lag_sumsq += s.lag1_corr * s.lag1_corr;
   }

   double same_mean = same_sum / iterations;
   double lag_mean = lag_sum / iterations;
   double same_sd = MathSqrt(MathMax(0.0, same_sumsq / iterations - same_mean * same_mean));
   double lag_sd = MathSqrt(MathMax(0.0, lag_sumsq / iterations - lag_mean * lag_mean));
   double same_z = same_sd > 0.0 ? (obs.same_lift - same_mean) / same_sd : 0.0;
   double lag_z = lag_sd > 0.0 ? (obs.lag1_corr - lag_mean) / lag_sd : 0.0;
   double same_p = (same_ge + 1.0) / (iterations + 1.0);
   double lag_p = (lag_ge + 1.0) / (iterations + 1.0);

   string verdict = "branch_inertia_not_above_label_permutation";
   if(obs.same_lift > 0.0 && same_z > 2.0 && obs.lag1_corr > 0.0)
      verdict = "branch_label_inertia_above_label_permutation";

   return "TRANSITION_PERM_STRESS"
      + "*n=" + IntegerToString(count)
      + "*iters=" + IntegerToString(iterations)
      + "*obsSameLiftPct=" + DAL_M0001FmtPct(obs.same_lift)
      + "*permMeanSameLiftPct=" + DAL_M0001FmtPct(same_mean)
      + "*permSdSameLiftPct=" + DAL_M0001FmtPct(same_sd)
      + "*sameLiftZ=" + DAL_M0001Fmt4(same_z)
      + "*sameLiftEmpP=" + DAL_M0001Fmt4(same_p)
      + "*obsLag1Corr=" + DAL_M0001Fmt4(obs.lag1_corr)
      + "*permMeanLag1Corr=" + DAL_M0001Fmt4(lag_mean)
      + "*permSdLag1Corr=" + DAL_M0001Fmt4(lag_sd)
      + "*lag1Z=" + DAL_M0001Fmt4(lag_z)
      + "*lag1EmpP=" + DAL_M0001Fmt4(lag_p)
      + "*stressVerdict=" + verdict;
}

string DAL_M0004RunShuffleStressText(const int &labels[], const int count, const int iterations)
{
   if(count <= 5 || iterations <= 0)
      return "RUN_SHUFFLE_STRESS*n=" + IntegerToString(count) + "*iters=0";

   int obs_all_count = 0, obs_all_max = 0;
   double obs_all_avg = 0.0;
   DAL_M0004ComputeAllRunStats(labels, count, obs_all_count, obs_all_max, obs_all_avg);

   DALM0004RunStats obs_rev, obs_cont;
   DAL_M0004ComputeRunStats(labels, count, DAL_M0004_LABEL_REVERSAL, obs_rev);
   DAL_M0004ComputeRunStats(labels, count, DAL_M0004_LABEL_CONTINUATION, obs_cont);

   int perm[];
   int tmp[];
   ArrayResize(tmp, count);
   double max_sum = 0.0, max_sumsq = 0.0, avg_sum = 0.0, avg_sumsq = 0.0;
   double cont_avg_sum = 0.0, cont_avg_sumsq = 0.0;
   int max_ge = 0, avg_ge = 0, cont_avg_ge = 0;

   for(int iter = 0; iter < iterations; iter++)
   {
      DAL_M0004BuildPermutation(count, iter, 5501, perm);
      for(int i = 0; i < count; i++)
         tmp[i] = labels[perm[i]];

      int rc = 0, mx = 0;
      double av = 0.0;
      DAL_M0004ComputeAllRunStats(tmp, count, rc, mx, av);
      DALM0004RunStats rs_cont;
      DAL_M0004ComputeRunStats(tmp, count, DAL_M0004_LABEL_CONTINUATION, rs_cont);

      if(mx >= obs_all_max) max_ge++;
      if(av >= obs_all_avg) avg_ge++;
      if(rs_cont.avg_run >= obs_cont.avg_run) cont_avg_ge++;
      max_sum += mx;
      max_sumsq += mx * mx;
      avg_sum += av;
      avg_sumsq += av * av;
      cont_avg_sum += rs_cont.avg_run;
      cont_avg_sumsq += rs_cont.avg_run * rs_cont.avg_run;
   }

   double max_mean = max_sum / iterations;
   double avg_mean = avg_sum / iterations;
   double cont_avg_mean = cont_avg_sum / iterations;
   double max_sd = MathSqrt(MathMax(0.0, max_sumsq / iterations - max_mean * max_mean));
   double avg_sd = MathSqrt(MathMax(0.0, avg_sumsq / iterations - avg_mean * avg_mean));
   double cont_avg_sd = MathSqrt(MathMax(0.0, cont_avg_sumsq / iterations - cont_avg_mean * cont_avg_mean));
   double max_z = max_sd > 0.0 ? (obs_all_max - max_mean) / max_sd : 0.0;
   double avg_z = avg_sd > 0.0 ? (obs_all_avg - avg_mean) / avg_sd : 0.0;
   double cont_avg_z = cont_avg_sd > 0.0 ? (obs_cont.avg_run - cont_avg_mean) / cont_avg_sd : 0.0;
   double max_p = (max_ge + 1.0) / (iterations + 1.0);
   double avg_p = (avg_ge + 1.0) / (iterations + 1.0);
   double cont_avg_p = (cont_avg_ge + 1.0) / (iterations + 1.0);

   string verdict = "branch_runs_not_above_shuffle";
   if(max_z > 2.0 || avg_z > 2.0 || cont_avg_z > 2.0)
      verdict = "branch_runs_cluster_above_iid_shuffle";

   return "RUN_SHUFFLE_STRESS"
      + "*n=" + IntegerToString(count)
      + "*iters=" + IntegerToString(iterations)
      + "*obsAllMaxRun=" + IntegerToString(obs_all_max)
      + "*shuffleAllMaxRunMean=" + DAL_M0001Fmt4(max_mean)
      + "*shuffleAllMaxRunSd=" + DAL_M0001Fmt4(max_sd)
      + "*allMaxRunZ=" + DAL_M0001Fmt4(max_z)
      + "*allMaxRunEmpP=" + DAL_M0001Fmt4(max_p)
      + "*obsAllAvgRun=" + DAL_M0001Fmt4(obs_all_avg)
      + "*shuffleAllAvgRunMean=" + DAL_M0001Fmt4(avg_mean)
      + "*shuffleAllAvgRunSd=" + DAL_M0001Fmt4(avg_sd)
      + "*allAvgRunZ=" + DAL_M0001Fmt4(avg_z)
      + "*allAvgRunEmpP=" + DAL_M0001Fmt4(avg_p)
      + "*obsContAvgRun=" + DAL_M0001Fmt4(obs_cont.avg_run)
      + "*shuffleContAvgRunMean=" + DAL_M0001Fmt4(cont_avg_mean)
      + "*shuffleContAvgRunSd=" + DAL_M0001Fmt4(cont_avg_sd)
      + "*contAvgRunZ=" + DAL_M0001Fmt4(cont_avg_z)
      + "*contAvgRunEmpP=" + DAL_M0001Fmt4(cont_avg_p)
      + "*stressVerdict=" + verdict;
}

double DAL_M0004BlockContinuationPctSd(const int &labels[], const int count, const int block_size, double &min_pct, double &max_pct, int &blocks)
{
   blocks = 0;
   min_pct = 100.0;
   max_pct = 0.0;
   int bs = block_size;
   if(bs < 2) bs = 2;
   if(count <= 0)
      return 0.0;

   int max_blocks = (count + bs - 1) / bs;
   double pcts[];
   ArrayResize(pcts, max_blocks);

   for(int start = 0; start < count; start += bs)
   {
      int end = start + bs;
      if(end > count) end = count;
      int n = end - start;
      if(n <= 0) continue;
      int cont = 0;
      for(int i = start; i < end; i++)
         if(labels[i] == DAL_M0004_LABEL_CONTINUATION)
            cont++;
      double pct = 100.0 * cont / n;
      pcts[blocks] = pct;
      if(pct < min_pct) min_pct = pct;
      if(pct > max_pct) max_pct = pct;
      blocks++;
   }

   if(blocks <= 1)
      return 0.0;
   double mean = 0.0;
   for(int i = 0; i < blocks; i++) mean += pcts[i];
   mean /= blocks;
   double var = 0.0;
   for(int i = 0; i < blocks; i++)
   {
      double d = pcts[i] - mean;
      var += d * d;
   }
   return MathSqrt(var / (blocks - 1));
}

string DAL_M0004BlockConcentrationStressText(const int &labels[], const int count, const int block_size, const int iterations)
{
   if(count <= 5 || iterations <= 0)
      return "BLOCK_CONCENTRATION_STRESS*n=" + IntegerToString(count) + "*iters=0";

   double obs_min = 0.0, obs_max = 0.0;
   int obs_blocks = 0;
   double obs_sd = DAL_M0004BlockContinuationPctSd(labels, count, block_size, obs_min, obs_max, obs_blocks);

   int perm[];
   int tmp[];
   ArrayResize(tmp, count);
   double sd_sum = 0.0, sd_sumsq = 0.0;
   int sd_ge = 0;
   for(int iter = 0; iter < iterations; iter++)
   {
      DAL_M0004BuildPermutation(count, iter, 6601, perm);
      for(int i = 0; i < count; i++)
         tmp[i] = labels[perm[i]];
      double mn = 0.0, mx = 0.0;
      int b = 0;
      double sd = DAL_M0004BlockContinuationPctSd(tmp, count, block_size, mn, mx, b);
      if(sd >= obs_sd) sd_ge++;
      sd_sum += sd;
      sd_sumsq += sd * sd;
   }

   double mean = sd_sum / iterations;
   double sd_sd = MathSqrt(MathMax(0.0, sd_sumsq / iterations - mean * mean));
   double z = sd_sd > 0.0 ? (obs_sd - mean) / sd_sd : 0.0;
   double p = (sd_ge + 1.0) / (iterations + 1.0);

   string verdict = "branch_block_concentration_not_above_shuffle";
   if(z > 2.0)
      verdict = "branch_block_concentration_above_shuffle_regime_clustering";

   return "BLOCK_CONCENTRATION_STRESS"
      + "*n=" + IntegerToString(count)
      + "*blockSize=" + IntegerToString(block_size)
      + "*blocks=" + IntegerToString(obs_blocks)
      + "*obsContinuationPctSd=" + DAL_M0001Fmt4(obs_sd)
      + "*obsContinuationPctMin=" + DAL_M0001FmtPct(obs_min)
      + "*obsContinuationPctMax=" + DAL_M0001FmtPct(obs_max)
      + "*shuffleMeanPctSd=" + DAL_M0001Fmt4(mean)
      + "*shuffleSdPctSd=" + DAL_M0001Fmt4(sd_sd)
      + "*pctSdZ=" + DAL_M0001Fmt4(z)
      + "*pctSdEmpP=" + DAL_M0001Fmt4(p)
      + "*stressVerdict=" + verdict;
}

string DAL_M0004FarLagText(const int &labels[], const int count, const int lag)
{
   double l1 = DAL_M0004LabelLagCorr(labels, count, 1);
   double l2 = DAL_M0004LabelLagCorr(labels, count, 2);
   double lk = DAL_M0004LabelLagCorr(labels, count, lag);
   string decay = "far_lag_not_configured";
   if(lag > 2)
      decay = MathAbs(lk) < MathAbs(l1) ? "memory_decays_with_lag" : "long_range_label_memory_present";

   return "FAR_LAG_PLACEBO"
      + "*n=" + IntegerToString(count)
      + "*lag1Corr=" + DAL_M0001Fmt4(l1)
      + "*lag2Corr=" + DAL_M0001Fmt4(l2)
      + "*placeboLag=" + IntegerToString(lag)
      + "*placeboLagCorr=" + DAL_M0001Fmt4(lk)
      + "*decayModel=" + decay;
}

void DAL_M0004FilterLabelsByInt(const int &labels[], const int &keys[], const int count, const int key, int &out[])
{
   ArrayResize(out, 0);
   for(int i = 0; i < count; i++)
   {
      if(keys[i] != key)
         continue;
      int n = ArraySize(out);
      ArrayResize(out, n + 1);
      out[n] = labels[i];
   }
}

string DAL_M0004SegmentTransitionText(const string tag, const int &labels[], const int &keys[], const int count, const int k0, const int k1, const int k2, const int k3)
{
   int keys_in[4];
   keys_in[0] = k0;
   keys_in[1] = k1;
   keys_in[2] = k2;
   keys_in[3] = k3;

   string out = tag;
   for(int i = 0; i < 4; i++)
   {
      int sub[];
      DAL_M0004FilterLabelsByInt(labels, keys, count, keys_in[i], sub);
      DALM0004TransitionStats s;
      DAL_M0004ComputeTransitionStats(sub, ArraySize(sub), s);
      out += "*seg" + IntegerToString(keys_in[i])
         + "N=" + IntegerToString(s.n)
         + "*seg" + IntegerToString(keys_in[i])
         + "ContPct=" + DAL_M0001FmtPct(s.continuation_pct)
         + "*seg" + IntegerToString(keys_in[i])
         + "SameLift=" + DAL_M0001FmtPct(s.same_lift)
         + "*seg" + IntegerToString(keys_in[i])
         + "Lag1=" + DAL_M0001Fmt4(s.lag1_corr);
   }
   return out;
}

void DAL_M0004PrevolTerciles(const double &prevols[], const int count, double &t1, double &t2)
{
   double vals[];
   ArrayResize(vals, count);
   for(int i = 0; i < count; i++)
      vals[i] = prevols[i];
   ArraySort(vals);
   if(count <= 0)
   {
      t1 = 0.0;
      t2 = 0.0;
      return;
   }
   int i1 = (int)MathFloor((count - 1) / 3.0);
   int i2 = (int)MathFloor(2.0 * (count - 1) / 3.0);
   t1 = vals[i1];
   t2 = vals[i2];
}

void DAL_M0004BuildPrevolRegimes(const double &prevols[], const int count, int &regimes[], double &t1, double &t2)
{
   DAL_M0004PrevolTerciles(prevols, count, t1, t2);
   ArrayResize(regimes, count);
   for(int i = 0; i < count; i++)
   {
      if(prevols[i] <= t1) regimes[i] = 0;
      else if(prevols[i] <= t2) regimes[i] = 1;
      else regimes[i] = 2;
   }
}

string DAL_M0004PrevolSegmentText(const int &labels[], const double &prevols[], const int count)
{
   int regimes[];
   double t1 = 0.0, t2 = 0.0;
   DAL_M0004BuildPrevolRegimes(prevols, count, regimes, t1, t2);
   string out = "PREVOL_REGIME_BRANCH_INERTIA*preVolT1=" + DAL_M0001Fmt4(t1) + "*preVolT2=" + DAL_M0001Fmt4(t2);
   for(int k = 0; k < 3; k++)
   {
      int sub[];
      DAL_M0004FilterLabelsByInt(labels, regimes, count, k, sub);
      DALM0004TransitionStats s;
      DAL_M0004ComputeTransitionStats(sub, ArraySize(sub), s);
      out += "*reg" + IntegerToString(k)
         + "N=" + IntegerToString(s.n)
         + "*reg" + IntegerToString(k)
         + "ContPct=" + DAL_M0001FmtPct(s.continuation_pct)
         + "*reg" + IntegerToString(k)
         + "SameLift=" + DAL_M0001FmtPct(s.same_lift)
         + "*reg" + IntegerToString(k)
         + "Lag1=" + DAL_M0001Fmt4(s.lag1_corr)
         + "*reg" + IntegerToString(k)
         + "PContAfterCont=" + DAL_M0001FmtPct(s.p_continuation_after_continuation);
   }
   return out;
}


int DAL_M0004FindIntIndex(const int &values[], const int count, const int value)
{
   for(int i = 0; i < count; i++)
      if(values[i] == value)
         return i;
   return -1;
}

void DAL_M0004UniqueKeys(const int &keys[], const int count, int &unique_keys[])
{
   ArrayResize(unique_keys, 0);
   for(int i = 0; i < count; i++)
   {
      int n = ArraySize(unique_keys);
      if(DAL_M0004FindIntIndex(unique_keys, n, keys[i]) >= 0)
         continue;
      ArrayResize(unique_keys, n + 1);
      unique_keys[n] = keys[i];
   }
}

void DAL_M0004BuildRevisitBuckets(const int &revisit_ids[], const int count, int &buckets[])
{
   ArrayResize(buckets, count);
   for(int i = 0; i < count; i++)
   {
      if(revisit_ids[i] <= 0) buckets[i] = 0;
      else if(revisit_ids[i] == 1) buckets[i] = 1;
      else if(revisit_ids[i] == 2) buckets[i] = 2;
      else buckets[i] = 3;
   }
}

void DAL_M0004BuildCompositeStrata(
   const int &sessions[],
   const int &trend_regimes[],
   const int &prevol_regimes[],
   const int &revisit_buckets[],
   const int count,
   int &strata[]
)
{
   ArrayResize(strata, count);
   for(int i = 0; i < count; i++)
   {
      int session = sessions[i]; if(session < 0) session = 9;
      int trend = trend_regimes[i]; if(trend < 0) trend = 9;
      int prevol = prevol_regimes[i]; if(prevol < 0) prevol = 9;
      int revisit = revisit_buckets[i]; if(revisit < 0) revisit = 9;
      strata[i] = session + 10 * prevol + 100 * trend + 1000 * revisit;
   }
}

void DAL_M0004BuildSpacingRegimes(const DALM0002BranchSample &samples[], const int count, int &regimes[], double &t1, double &t2)
{
   ArrayResize(regimes, count);
   double gaps[];
   ArrayResize(gaps, count);
   for(int i = 0; i < count; i++)
   {
      if(i == 0)
         gaps[i] = 0.0;
      else
      {
         int g = DAL_M0004SampleSortKey(samples[i]) - DAL_M0004SampleSortKey(samples[i - 1]);
         if(g < 0) g = 0;
         gaps[i] = (double)g;
      }
   }
   if(count > 1 && gaps[0] == 0.0)
      gaps[0] = gaps[1];
   DAL_M0004PrevolTerciles(gaps, count, t1, t2);
   for(int i = 0; i < count; i++)
   {
      if(gaps[i] <= t1) regimes[i] = 0;
      else if(gaps[i] <= t2) regimes[i] = 1;
      else regimes[i] = 2;
   }
}

string DAL_M0004SingleSegmentDetailText(const string tag, const string segment_name, const int &labels[], const int &keys[], const int count, const int key)
{
   int sub[];
   DAL_M0004FilterLabelsByInt(labels, keys, count, key, sub);
   int n = ArraySize(sub);
   DALM0004TransitionStats s;
   DALM0004RunStats rev;
   DALM0004RunStats cont;
   int all_count = 0, all_max = 0;
   double all_avg = 0.0;
   DAL_M0004ComputeTransitionStats(sub, n, s);
   DAL_M0004ComputeRunStats(sub, n, DAL_M0004_LABEL_REVERSAL, rev);
   DAL_M0004ComputeRunStats(sub, n, DAL_M0004_LABEL_CONTINUATION, cont);
   DAL_M0004ComputeAllRunStats(sub, n, all_count, all_max, all_avg);

   return tag
      + "*segment=" + segment_name
      + "*key=" + IntegerToString(key)
      + "*n=" + IntegerToString(n)
      + "*revPct=" + DAL_M0001FmtPct(s.reversal_pct)
      + "*contPct=" + DAL_M0001FmtPct(s.continuation_pct)
      + "*samePct=" + DAL_M0001FmtPct(s.same_pct)
      + "*iidSamePct=" + DAL_M0001FmtPct(s.iid_same_pct)
      + "*sameLift=" + DAL_M0001FmtPct(s.same_lift)
      + "*switchPct=" + DAL_M0001FmtPct(s.switch_pct)
      + "*pRevAfterRev=" + DAL_M0001FmtPct(s.p_reversal_after_reversal)
      + "*pContAfterCont=" + DAL_M0001FmtPct(s.p_continuation_after_continuation)
      + "*revLift=" + DAL_M0001FmtPct(s.reversal_persistence_lift)
      + "*contLift=" + DAL_M0001FmtPct(s.continuation_persistence_lift)
      + "*lag1=" + DAL_M0001Fmt4(s.lag1_corr)
      + "*lag2=" + DAL_M0001Fmt4(s.lag2_corr)
      + "*markovChi2=" + DAL_M0001Fmt4(s.markov_chi2)
      + "*mutualInfoNats=" + DAL_M0001Fmt4(s.mutual_info_nats)
      + "*allAvgRun=" + DAL_M0001Fmt4(all_avg)
      + "*allMaxRun=" + IntegerToString(all_max)
      + "*revRunOverIid=" + DAL_M0001Fmt4(rev.avg_run_over_iid)
      + "*contRunOverIid=" + DAL_M0001Fmt4(cont.avg_run_over_iid);
}

string DAL_M0004LagDecayText(const int &labels[], const int count, const int placebo_lag)
{
   int lags[9];
   lags[0] = 1;
   lags[1] = 2;
   lags[2] = 3;
   lags[3] = 5;
   lags[4] = 10;
   lags[5] = 20;
   lags[6] = 50;
   lags[7] = 100;
   lags[8] = placebo_lag;

   string out = "LAG_DECAY*n=" + IntegerToString(count);
   double l1 = DAL_M0004LabelLagCorr(labels, count, 1);
   double auc = 0.0;
   for(int i = 0; i < 9; i++)
   {
      int lag = lags[i];
      if(lag < 1) lag = 1;
      double c = DAL_M0004LabelLagCorr(labels, count, lag);
      out += "*lag" + IntegerToString(lag) + "Corr=" + DAL_M0001Fmt4(c);
      if(i < 8) auc += MathMax(0.0, c);
   }
   out += "*positiveLagCorrAuc=" + DAL_M0001Fmt4(auc)
      + "*lag2OverLag1=" + DAL_M0001Fmt4(DAL_M0004SafeRatio(DAL_M0004LabelLagCorr(labels, count, 2), l1))
      + "*lag5OverLag1=" + DAL_M0001Fmt4(DAL_M0004SafeRatio(DAL_M0004LabelLagCorr(labels, count, 5), l1))
      + "*lag20OverLag1=" + DAL_M0001Fmt4(DAL_M0004SafeRatio(DAL_M0004LabelLagCorr(labels, count, 20), l1))
      + "*decayProfile=" + (MathAbs(DAL_M0004LabelLagCorr(labels, count, placebo_lag)) < MathAbs(l1) ? "near_memory_decays" : "far_memory_persists");
   return out;
}

string DAL_M0004RunLengthTransitionText(const int &labels[], const int count)
{
   int total[5], same[5], rev_total[5], rev_same[5], cont_total[5], cont_same[5];
   for(int i = 0; i < 5; i++)
   {
      total[i] = 0; same[i] = 0; rev_total[i] = 0; rev_same[i] = 0; cont_total[i] = 0; cont_same[i] = 0;
   }
   if(count <= 1)
      return "RUN_LENGTH_TRANSITION*n=" + IntegerToString(count);

   int prev_run_len = 1;
   for(int i = 1; i < count; i++)
   {
      int bucket = prev_run_len;
      if(bucket > 4) bucket = 4;
      total[bucket]++;
      if(labels[i] == labels[i - 1]) same[bucket]++;
      if(labels[i - 1] == DAL_M0004_LABEL_REVERSAL)
      {
         rev_total[bucket]++;
         if(labels[i] == labels[i - 1]) rev_same[bucket]++;
      }
      else
      {
         cont_total[bucket]++;
         if(labels[i] == labels[i - 1]) cont_same[bucket]++;
      }

      if(labels[i] == labels[i - 1]) prev_run_len++;
      else prev_run_len = 1;
   }

   string out = "RUN_LENGTH_TRANSITION*n=" + IntegerToString(count);
   for(int b = 1; b <= 4; b++)
   {
      string name = (b < 4 ? IntegerToString(b) : "4plus");
      out += "*run" + name + "N=" + IntegerToString(total[b])
         + "*run" + name + "SamePct=" + DAL_M0001FmtPct(total[b] > 0 ? 100.0 * same[b] / total[b] : 0.0)
         + "*run" + name + "RevSamePct=" + DAL_M0001FmtPct(rev_total[b] > 0 ? 100.0 * rev_same[b] / rev_total[b] : 0.0)
         + "*run" + name + "ContSamePct=" + DAL_M0001FmtPct(cont_total[b] > 0 ? 100.0 * cont_same[b] / cont_total[b] : 0.0);
   }
   return out;
}

string DAL_M0004BlockRegimeProfileText(const int &labels[], const int count, const int block_size)
{
   if(count <= 0)
      return "BLOCK_REGIME_PROFILE*n=0";
   int bs = block_size;
   if(bs < 2) bs = 2;
   int blocks = 0;
   double global_cont = 0.0;
   for(int i = 0; i < count; i++) if(labels[i] == DAL_M0004_LABEL_CONTINUATION) global_cont++;
   global_cont = 100.0 * global_cont / count;

   double cont_sum = 0.0, cont_sumsq = 0.0, cont_min = 100.0, cont_max = 0.0;
   double lift_sum = 0.0, lift_sumsq = 0.0, lift_min = 1000000.0, lift_max = -1000000.0;
   double lag_sum = 0.0, lag_sumsq = 0.0;
   int positive_lift = 0, positive_lag = 0, hot = 0, cold = 0;

   for(int start = 0; start < count; start += bs)
   {
      int end = start + bs;
      if(end > count) end = count;
      int n = end - start;
      if(n <= 2) continue;
      int sub[];
      ArrayResize(sub, n);
      for(int j = 0; j < n; j++) sub[j] = labels[start + j];
      DALM0004TransitionStats s;
      DAL_M0004ComputeTransitionStats(sub, n, s);
      double cp = s.continuation_pct;
      cont_sum += cp; cont_sumsq += cp * cp;
      if(cp < cont_min) cont_min = cp;
      if(cp > cont_max) cont_max = cp;
      lift_sum += s.same_lift; lift_sumsq += s.same_lift * s.same_lift;
      if(s.same_lift < lift_min) lift_min = s.same_lift;
      if(s.same_lift > lift_max) lift_max = s.same_lift;
      lag_sum += s.lag1_corr; lag_sumsq += s.lag1_corr * s.lag1_corr;
      if(s.same_lift > 0.0) positive_lift++;
      if(s.lag1_corr > 0.0) positive_lag++;
      if(cp >= global_cont + 10.0) hot++;
      if(cp <= global_cont - 10.0) cold++;
      blocks++;
   }
   double b = (double)MathMax(1, blocks);
   double cont_mean = cont_sum / b;
   double lift_mean = lift_sum / b;
   double lag_mean = lag_sum / b;
   double cont_sd = MathSqrt(MathMax(0.0, cont_sumsq / b - cont_mean * cont_mean));
   double lift_sd = MathSqrt(MathMax(0.0, lift_sumsq / b - lift_mean * lift_mean));
   double lag_sd = MathSqrt(MathMax(0.0, lag_sumsq / b - lag_mean * lag_mean));

   return "BLOCK_REGIME_PROFILE"
      + "*n=" + IntegerToString(count)
      + "*blockSize=" + IntegerToString(bs)
      + "*blocks=" + IntegerToString(blocks)
      + "*globalContPct=" + DAL_M0001FmtPct(global_cont)
      + "*meanContPct=" + DAL_M0001FmtPct(cont_mean)
      + "*sdContPct=" + DAL_M0001Fmt4(cont_sd)
      + "*minContPct=" + DAL_M0001FmtPct(cont_min)
      + "*maxContPct=" + DAL_M0001FmtPct(cont_max)
      + "*meanSameLift=" + DAL_M0001FmtPct(lift_mean)
      + "*sdSameLift=" + DAL_M0001Fmt4(lift_sd)
      + "*minSameLift=" + DAL_M0001FmtPct(lift_min)
      + "*maxSameLift=" + DAL_M0001FmtPct(lift_max)
      + "*meanLag1=" + DAL_M0001Fmt4(lag_mean)
      + "*sdLag1=" + DAL_M0001Fmt4(lag_sd)
      + "*positiveLiftBlockPct=" + DAL_M0001FmtPct(100.0 * positive_lift / b)
      + "*positiveLagBlockPct=" + DAL_M0001FmtPct(100.0 * positive_lag / b)
      + "*hotContinuationBlockPct=" + DAL_M0001FmtPct(100.0 * hot / b)
      + "*coldContinuationBlockPct=" + DAL_M0001FmtPct(100.0 * cold / b);
}

void DAL_M0004StratifiedShuffleLabels(const int &labels[], const int &strata[], const int count, const int iter, const int salt, int &out[])
{
   ArrayResize(out, count);
   for(int i = 0; i < count; i++) out[i] = labels[i];

   int unique[];
   DAL_M0004UniqueKeys(strata, count, unique);
   int unique_count = ArraySize(unique);
   for(int u = 0; u < unique_count; u++)
   {
      int key = unique[u];
      int pos[];
      ArrayResize(pos, 0);
      for(int i = 0; i < count; i++)
      {
         if(strata[i] != key) continue;
         int n = ArraySize(pos);
         ArrayResize(pos, n + 1);
         pos[n] = i;
      }
      int pn = ArraySize(pos);
      for(int p = pn - 1; p > 0; p--)
      {
         double frac = DAL_M0001RandomFractionK(iter + salt, count + (int)MathAbs((double)key), p + 17, salt + u * 101);
         int q = (int)MathFloor(frac * (p + 1));
         if(q < 0) q = 0;
         if(q > p) q = p;
         int a = pos[p];
         int b = pos[q];
         int tmp = out[a];
         out[a] = out[b];
         out[b] = tmp;
      }
   }
}

string DAL_M0004StratifiedPermutationStressText(const string name, const int &labels[], const int &strata[], const int count, const int iterations)
{
   if(count <= 5 || iterations <= 0)
      return "STRATIFIED_PERM_STRESS*name=" + name + "*n=" + IntegerToString(count) + "*iters=0";
   DALM0004TransitionStats obs;
   DAL_M0004ComputeTransitionStats(labels, count, obs);

   int tmp[];
   double same_sum = 0.0, same_sumsq = 0.0, lag_sum = 0.0, lag_sumsq = 0.0;
   int same_ge = 0, lag_ge = 0;
   for(int iter = 0; iter < iterations; iter++)
   {
      DAL_M0004StratifiedShuffleLabels(labels, strata, count, iter, 7701, tmp);
      DALM0004TransitionStats s;
      DAL_M0004ComputeTransitionStats(tmp, count, s);
      if(s.same_lift >= obs.same_lift) same_ge++;
      if(s.lag1_corr >= obs.lag1_corr) lag_ge++;
      same_sum += s.same_lift; same_sumsq += s.same_lift * s.same_lift;
      lag_sum += s.lag1_corr; lag_sumsq += s.lag1_corr * s.lag1_corr;
   }
   double same_mean = same_sum / iterations;
   double lag_mean = lag_sum / iterations;
   double same_sd = MathSqrt(MathMax(0.0, same_sumsq / iterations - same_mean * same_mean));
   double lag_sd = MathSqrt(MathMax(0.0, lag_sumsq / iterations - lag_mean * lag_mean));
   double same_z = same_sd > 0.0 ? (obs.same_lift - same_mean) / same_sd : 0.0;
   double lag_z = lag_sd > 0.0 ? (obs.lag1_corr - lag_mean) / lag_sd : 0.0;
   double same_p = (same_ge + 1.0) / (iterations + 1.0);
   double lag_p = (lag_ge + 1.0) / (iterations + 1.0);
   int unique[]; DAL_M0004UniqueKeys(strata, count, unique);

   string verdict = "branch_inertia_not_above_stratified_null";
   if(same_z > 2.0 && lag_z > 2.0)
      verdict = "branch_inertia_above_stratified_engineered_null";

   return "STRATIFIED_PERM_STRESS"
      + "*name=" + name
      + "*n=" + IntegerToString(count)
      + "*strata=" + IntegerToString(ArraySize(unique))
      + "*iters=" + IntegerToString(iterations)
      + "*obsSameLiftPct=" + DAL_M0001FmtPct(obs.same_lift)
      + "*stratMeanSameLiftPct=" + DAL_M0001FmtPct(same_mean)
      + "*stratSdSameLiftPct=" + DAL_M0001FmtPct(same_sd)
      + "*sameLiftZ=" + DAL_M0001Fmt4(same_z)
      + "*sameLiftEmpP=" + DAL_M0001Fmt4(same_p)
      + "*obsLag1Corr=" + DAL_M0001Fmt4(obs.lag1_corr)
      + "*stratMeanLag1Corr=" + DAL_M0001Fmt4(lag_mean)
      + "*stratSdLag1Corr=" + DAL_M0001Fmt4(lag_sd)
      + "*lag1Z=" + DAL_M0001Fmt4(lag_z)
      + "*lag1EmpP=" + DAL_M0001Fmt4(lag_p)
      + "*stressVerdict=" + verdict;
}

double DAL_M0004CircularShiftCorr(const int &labels[], const int count, const int lag, const int shift)
{
   if(count <= lag + 2)
      return 0.0;
   int n = count;
   double mx = 0.0, my = 0.0;
   for(int i = 0; i < n; i++)
   {
      int j = i - lag - shift;
      while(j < 0) j += count;
      j = j % count;
      mx += labels[i];
      my += labels[j];
   }
   mx /= n; my /= n;
   double cov = 0.0, vx = 0.0, vy = 0.0;
   for(int i = 0; i < n; i++)
   {
      int j = i - lag - shift;
      while(j < 0) j += count;
      j = j % count;
      double x = labels[i] - mx;
      double y = labels[j] - my;
      cov += x * y; vx += x * x; vy += y * y;
   }
   if(vx <= 0.0 || vy <= 0.0) return 0.0;
   return cov / MathSqrt(vx * vy);
}

string DAL_M0004CircularShiftStressText(const int &labels[], const int count, const int iterations, const int min_shift)
{
   if(count <= min_shift + 10 || iterations <= 0)
      return "CIRCULAR_SHIFT_STRESS*n=" + IntegerToString(count) + "*iters=0";
   double obs = DAL_M0004LabelLagCorr(labels, count, 1);
   int min_s = min_shift;
   if(min_s < 3) min_s = 3;
   int max_s = count - min_s - 1;
   if(max_s <= min_s) max_s = count - 3;
   double sum = 0.0, sumsq = 0.0;
   int ge = 0;
   int span = MathMax(1, max_s - min_s + 1);
   for(int iter = 0; iter < iterations; iter++)
   {
      double frac = DAL_M0001RandomFractionK(iter + 8801, count, min_s, max_s);
      int shift = min_s + (int)MathFloor(frac * span);
      if(shift < min_s) shift = min_s;
      if(shift > max_s) shift = max_s;
      double c = DAL_M0004CircularShiftCorr(labels, count, 1, shift);
      if(c >= obs) ge++;
      sum += c; sumsq += c * c;
   }
   double mean = sum / iterations;
   double sd = MathSqrt(MathMax(0.0, sumsq / iterations - mean * mean));
   double z = sd > 0.0 ? (obs - mean) / sd : 0.0;
   double p = (ge + 1.0) / (iterations + 1.0);
   string verdict = z > 2.0 ? "near_lag_memory_above_circular_far_lag_null" : "near_lag_memory_not_above_circular_null";
   return "CIRCULAR_SHIFT_STRESS"
      + "*n=" + IntegerToString(count)
      + "*iters=" + IntegerToString(iterations)
      + "*minShift=" + IntegerToString(min_s)
      + "*obsLag1Corr=" + DAL_M0001Fmt4(obs)
      + "*shiftMeanCorr=" + DAL_M0001Fmt4(mean)
      + "*shiftSdCorr=" + DAL_M0001Fmt4(sd)
      + "*lag1Z=" + DAL_M0001Fmt4(z)
      + "*lag1EmpP=" + DAL_M0001Fmt4(p)
      + "*stressVerdict=" + verdict;
}

void DAL_M0004BlockOrderShuffleLabels(const int &labels[], const int count, const int block_size, const int iter, int &out[])
{
   ArrayResize(out, count);
   int bs = block_size;
   if(bs < 2) bs = 2;
   int blocks = (count + bs - 1) / bs;
   int order[];
   DAL_M0004BuildPermutation(blocks, iter, 9901, order);
   int idx = 0;
   for(int bi = 0; bi < blocks; bi++)
   {
      int b = order[bi];
      int start = b * bs;
      int end = start + bs;
      if(end > count) end = count;
      for(int i = start; i < end && idx < count; i++)
      {
         out[idx] = labels[i];
         idx++;
      }
   }
}

string DAL_M0004BlockOrderShuffleStressText(const int &labels[], const int count, const int block_size, const int iterations)
{
   if(count <= block_size * 3 || iterations <= 0)
      return "BLOCK_ORDER_SHUFFLE_STRESS*n=" + IntegerToString(count) + "*iters=0";
   DALM0004TransitionStats obs;
   DAL_M0004ComputeTransitionStats(labels, count, obs);
   int tmp[];
   double same_sum = 0.0, same_sumsq = 0.0, lag_sum = 0.0, lag_sumsq = 0.0;
   int same_ge = 0, lag_ge = 0;
   for(int iter = 0; iter < iterations; iter++)
   {
      DAL_M0004BlockOrderShuffleLabels(labels, count, block_size, iter, tmp);
      DALM0004TransitionStats s;
      DAL_M0004ComputeTransitionStats(tmp, count, s);
      if(s.same_lift >= obs.same_lift) same_ge++;
      if(s.lag1_corr >= obs.lag1_corr) lag_ge++;
      same_sum += s.same_lift; same_sumsq += s.same_lift * s.same_lift;
      lag_sum += s.lag1_corr; lag_sumsq += s.lag1_corr * s.lag1_corr;
   }
   double same_mean = same_sum / iterations;
   double lag_mean = lag_sum / iterations;
   double same_sd = MathSqrt(MathMax(0.0, same_sumsq / iterations - same_mean * same_mean));
   double lag_sd = MathSqrt(MathMax(0.0, lag_sumsq / iterations - lag_mean * lag_mean));
   double same_z = same_sd > 0.0 ? (obs.same_lift - same_mean) / same_sd : 0.0;
   double lag_z = lag_sd > 0.0 ? (obs.lag1_corr - lag_mean) / lag_sd : 0.0;
   double same_p = (same_ge + 1.0) / (iterations + 1.0);
   double lag_p = (lag_ge + 1.0) / (iterations + 1.0);
   string verdict = "local_block_structure_explains_most_inertia";
   if(same_z > 2.0 && lag_z > 2.0)
      verdict = "inertia_exceeds_local_block_order_null";
   return "BLOCK_ORDER_SHUFFLE_STRESS"
      + "*n=" + IntegerToString(count)
      + "*blockSize=" + IntegerToString(block_size)
      + "*iters=" + IntegerToString(iterations)
      + "*obsSameLiftPct=" + DAL_M0001FmtPct(obs.same_lift)
      + "*blockNullMeanSameLiftPct=" + DAL_M0001FmtPct(same_mean)
      + "*blockNullSdSameLiftPct=" + DAL_M0001FmtPct(same_sd)
      + "*sameLiftZ=" + DAL_M0001Fmt4(same_z)
      + "*sameLiftEmpP=" + DAL_M0001Fmt4(same_p)
      + "*obsLag1Corr=" + DAL_M0001Fmt4(obs.lag1_corr)
      + "*blockNullMeanLag1Corr=" + DAL_M0001Fmt4(lag_mean)
      + "*blockNullSdLag1Corr=" + DAL_M0001Fmt4(lag_sd)
      + "*lag1Z=" + DAL_M0001Fmt4(lag_z)
      + "*lag1EmpP=" + DAL_M0001Fmt4(lag_p)
      + "*stressVerdict=" + verdict;
}


struct DALM0004ContextStats
{
   int n;
   int evaluated;
   int dominant_count;
   int neutral_count;
   int rev_context_count;
   int cont_context_count;
   int follow_dominant;
   int rev_context_follow;
   int cont_context_follow;
   int conflict_count;
   int conflict_last_follow;
   int conflict_context_follow;
   int consensus_count;
   int consensus_follow;
   int current_continuation_count;
   double global_continuation_pct;
   double mean_context_continuation_pct;
   double mean_confidence_pct;
   double dominant_follow_pct;
   double expected_follow_pct;
   double dominant_lift_pct;
   double rev_context_next_reversal_pct;
   double cont_context_next_continuation_pct;
   double conflict_last_follow_pct;
   double conflict_context_follow_pct;
   double conflict_context_minus_last_pct;
   double consensus_follow_pct;
};

void DAL_M0004ComputeContextStats(
   const int &labels[],
   const int count,
   const int lookback,
   const double ewma_alpha,
   const double strong_threshold,
   const bool use_ewma,
   DALM0004ContextStats &st
)
{
   st.n = count;
   st.evaluated = 0;
   st.dominant_count = 0;
   st.neutral_count = 0;
   st.rev_context_count = 0;
   st.cont_context_count = 0;
   st.follow_dominant = 0;
   st.rev_context_follow = 0;
   st.cont_context_follow = 0;
   st.conflict_count = 0;
   st.conflict_last_follow = 0;
   st.conflict_context_follow = 0;
   st.consensus_count = 0;
   st.consensus_follow = 0;
   st.current_continuation_count = 0;
   st.global_continuation_pct = 0.0;
   st.mean_context_continuation_pct = 0.0;
   st.mean_confidence_pct = 0.0;
   st.dominant_follow_pct = 0.0;
   st.expected_follow_pct = 0.0;
   st.dominant_lift_pct = 0.0;
   st.rev_context_next_reversal_pct = 0.0;
   st.cont_context_next_continuation_pct = 0.0;
   st.conflict_last_follow_pct = 0.0;
   st.conflict_context_follow_pct = 0.0;
   st.conflict_context_minus_last_pct = 0.0;
   st.consensus_follow_pct = 0.0;

   if(count <= 1)
      return;

   int global_cont = 0;
   for(int i = 0; i < count; i++)
      if(labels[i] == DAL_M0004_LABEL_CONTINUATION)
         global_cont++;
   double global_cont_prob = (double)global_cont / count;
   double global_rev_prob = 1.0 - global_cont_prob;
   st.global_continuation_pct = 100.0 * global_cont_prob;

   int k = lookback;
   if(k < 1) k = 1;
   double alpha = ewma_alpha;
   if(alpha <= 0.0) alpha = 0.35;
   if(alpha >= 1.0) alpha = 0.99;
   double decay = 1.0 - alpha;
   double thr = strong_threshold;
   if(thr < 0.51) thr = 0.51;
   if(thr > 0.95) thr = 0.95;

   double context_p_sum = 0.0;
   double confidence_sum = 0.0;
   double expected_follow_sum = 0.0;
   int rev_context_total = 0;
   int cont_context_total = 0;

   for(int i = 1; i < count; i++)
   {
      int start = i - k;
      if(start < 0) start = 0;
      int window = i - start;
      if(window <= 0)
         continue;

      double p = 0.0;
      if(use_ewma)
      {
         double w = 1.0;
         double sumw = 0.0;
         double score = 0.0;
         for(int j = i - 1; j >= start; j--)
         {
            score += w * labels[j];
            sumw += w;
            w *= decay;
         }
         p = sumw > 0.0 ? score / sumw : 0.0;
      }
      else
      {
         int cont = 0;
         for(int j = start; j < i; j++)
            if(labels[j] == DAL_M0004_LABEL_CONTINUATION)
               cont++;
         p = (double)cont / window;
      }

      int dominant = -1;
      if(p >= thr)
         dominant = DAL_M0004_LABEL_CONTINUATION;
      else if(p <= 1.0 - thr)
         dominant = DAL_M0004_LABEL_REVERSAL;

      st.evaluated++;
      if(labels[i] == DAL_M0004_LABEL_CONTINUATION)
         st.current_continuation_count++;
      context_p_sum += p;
      confidence_sum += MathAbs(2.0 * p - 1.0);

      if(dominant < 0)
      {
         st.neutral_count++;
         continue;
      }

      st.dominant_count++;
      if(dominant == DAL_M0004_LABEL_CONTINUATION)
      {
         st.cont_context_count++;
         cont_context_total++;
         expected_follow_sum += global_cont_prob;
         if(labels[i] == DAL_M0004_LABEL_CONTINUATION)
            st.cont_context_follow++;
      }
      else
      {
         st.rev_context_count++;
         rev_context_total++;
         expected_follow_sum += global_rev_prob;
         if(labels[i] == DAL_M0004_LABEL_REVERSAL)
            st.rev_context_follow++;
      }

      if(labels[i] == dominant)
         st.follow_dominant++;

      int last_label = labels[i - 1];
      if(last_label == dominant)
      {
         st.consensus_count++;
         if(labels[i] == dominant)
            st.consensus_follow++;
      }
      else
      {
         st.conflict_count++;
         if(labels[i] == last_label)
            st.conflict_last_follow++;
         if(labels[i] == dominant)
            st.conflict_context_follow++;
      }
   }

   if(st.evaluated > 0)
   {
      st.mean_context_continuation_pct = 100.0 * context_p_sum / st.evaluated;
      st.mean_confidence_pct = 100.0 * confidence_sum / st.evaluated;
   }
   if(st.dominant_count > 0)
   {
      st.dominant_follow_pct = 100.0 * st.follow_dominant / st.dominant_count;
      st.expected_follow_pct = 100.0 * expected_follow_sum / st.dominant_count;
      st.dominant_lift_pct = st.dominant_follow_pct - st.expected_follow_pct;
   }
   if(rev_context_total > 0)
      st.rev_context_next_reversal_pct = 100.0 * st.rev_context_follow / rev_context_total;
   if(cont_context_total > 0)
      st.cont_context_next_continuation_pct = 100.0 * st.cont_context_follow / cont_context_total;
   if(st.conflict_count > 0)
   {
      st.conflict_last_follow_pct = 100.0 * st.conflict_last_follow / st.conflict_count;
      st.conflict_context_follow_pct = 100.0 * st.conflict_context_follow / st.conflict_count;
      st.conflict_context_minus_last_pct = st.conflict_context_follow_pct - st.conflict_last_follow_pct;
   }
   if(st.consensus_count > 0)
      st.consensus_follow_pct = 100.0 * st.consensus_follow / st.consensus_count;
}

string DAL_M0004ContextStatsText(
   const string tag,
   const string method,
   const int &labels[],
   const int count,
   const int lookback,
   const double ewma_alpha,
   const double strong_threshold,
   const bool use_ewma
)
{
   DALM0004ContextStats st;
   DAL_M0004ComputeContextStats(labels, count, lookback, ewma_alpha, strong_threshold, use_ewma, st);
   string model = "context_not_dominant_or_insufficient";
   if(st.dominant_lift_pct > 0.0 && st.conflict_context_minus_last_pct > 0.0)
      model = "context_beats_last_event_in_conflicts";
   else if(st.dominant_lift_pct > 0.0)
      model = "context_dominant_state_has_predictive_lift";

   return tag
      + "*method=" + method
      + "*k=" + IntegerToString(lookback)
      + "*alpha=" + DAL_M0001Fmt4(ewma_alpha)
      + "*threshold=" + DAL_M0001Fmt4(strong_threshold)
      + "*n=" + IntegerToString(count)
      + "*evaluated=" + IntegerToString(st.evaluated)
      + "*dominantN=" + IntegerToString(st.dominant_count)
      + "*neutralN=" + IntegerToString(st.neutral_count)
      + "*revContextN=" + IntegerToString(st.rev_context_count)
      + "*contContextN=" + IntegerToString(st.cont_context_count)
      + "*globalContPct=" + DAL_M0001FmtPct(st.global_continuation_pct)
      + "*meanContextContPct=" + DAL_M0001FmtPct(st.mean_context_continuation_pct)
      + "*meanConfidencePct=" + DAL_M0001FmtPct(st.mean_confidence_pct)
      + "*dominantFollowPct=" + DAL_M0001FmtPct(st.dominant_follow_pct)
      + "*expectedFollowPct=" + DAL_M0001FmtPct(st.expected_follow_pct)
      + "*dominantLiftPct=" + DAL_M0001FmtPct(st.dominant_lift_pct)
      + "*revContextNextRevPct=" + DAL_M0001FmtPct(st.rev_context_next_reversal_pct)
      + "*contContextNextContPct=" + DAL_M0001FmtPct(st.cont_context_next_continuation_pct)
      + "*conflictN=" + IntegerToString(st.conflict_count)
      + "*conflictLastFollowPct=" + DAL_M0001FmtPct(st.conflict_last_follow_pct)
      + "*conflictContextFollowPct=" + DAL_M0001FmtPct(st.conflict_context_follow_pct)
      + "*conflictContextMinusLastPct=" + DAL_M0001FmtPct(st.conflict_context_minus_last_pct)
      + "*consensusN=" + IntegerToString(st.consensus_count)
      + "*consensusFollowPct=" + DAL_M0001FmtPct(st.consensus_follow_pct)
      + "*contextModel=" + model;
}

string DAL_M0004ContextBucketText(
   const string tag,
   const string method,
   const int &labels[],
   const int count,
   const int lookback,
   const double ewma_alpha,
   const bool use_ewma
)
{
   int bucket_n[5], bucket_cont[5], bucket_follow[5];
   double bucket_p_sum[5];
   for(int b = 0; b < 5; b++)
   {
      bucket_n[b] = 0;
      bucket_cont[b] = 0;
      bucket_follow[b] = 0;
      bucket_p_sum[b] = 0.0;
   }

   int k = lookback;
   if(k < 1) k = 1;
   double alpha = ewma_alpha;
   if(alpha <= 0.0) alpha = 0.35;
   if(alpha >= 1.0) alpha = 0.99;
   double decay = 1.0 - alpha;

   for(int i = 1; i < count; i++)
   {
      int start = i - k;
      if(start < 0) start = 0;
      int window = i - start;
      if(window <= 0) continue;
      double p = 0.0;
      if(use_ewma)
      {
         double w = 1.0, sumw = 0.0, score = 0.0;
         for(int j = i - 1; j >= start; j--)
         {
            score += w * labels[j];
            sumw += w;
            w *= decay;
         }
         p = sumw > 0.0 ? score / sumw : 0.0;
      }
      else
      {
         int cont = 0;
         for(int j = start; j < i; j++) if(labels[j] == DAL_M0004_LABEL_CONTINUATION) cont++;
         p = (double)cont / window;
      }

      int b = 2;
      if(p <= 0.35) b = 0;
      else if(p < 0.45) b = 1;
      else if(p <= 0.55) b = 2;
      else if(p < 0.65) b = 3;
      else b = 4;

      bucket_n[b]++;
      bucket_p_sum[b] += p;
      if(labels[i] == DAL_M0004_LABEL_CONTINUATION) bucket_cont[b]++;
      if((b <= 1 && labels[i] == DAL_M0004_LABEL_REVERSAL) || (b >= 3 && labels[i] == DAL_M0004_LABEL_CONTINUATION))
         bucket_follow[b]++;
   }

   string names[5];
   names[0] = "strongRev";
   names[1] = "leanRev";
   names[2] = "mixed";
   names[3] = "leanCont";
   names[4] = "strongCont";

   string out = tag + "*method=" + method + "*k=" + IntegerToString(lookback) + "*alpha=" + DAL_M0001Fmt4(ewma_alpha);
   for(int b = 0; b < 5; b++)
   {
      double cont_pct = bucket_n[b] > 0 ? 100.0 * bucket_cont[b] / bucket_n[b] : 0.0;
      double follow_pct = bucket_n[b] > 0 ? 100.0 * bucket_follow[b] / bucket_n[b] : 0.0;
      double mean_p = bucket_n[b] > 0 ? 100.0 * bucket_p_sum[b] / bucket_n[b] : 0.0;
      out += "*" + names[b] + "N=" + IntegerToString(bucket_n[b])
         + "*" + names[b] + "MeanContCtx=" + DAL_M0001FmtPct(mean_p)
         + "*" + names[b] + "NextContPct=" + DAL_M0001FmtPct(cont_pct)
         + "*" + names[b] + "FollowCtxPct=" + DAL_M0001FmtPct(follow_pct);
   }
   return out;
}

string DAL_M0004ContextShuffleStressText(
   const string name,
   const int &labels[],
   const int &strata[],
   const int count,
   const int lookback,
   const double ewma_alpha,
   const double strong_threshold,
   const bool use_ewma,
   const int iterations,
   const bool stratified
)
{
   if(count <= lookback + 5 || iterations <= 0)
      return "CONTEXT_SHUFFLE_STRESS*name=" + name + "*n=" + IntegerToString(count) + "*iters=0";

   DALM0004ContextStats obs;
   DAL_M0004ComputeContextStats(labels, count, lookback, ewma_alpha, strong_threshold, use_ewma, obs);

   int tmp[];
   int perm[];
   double lift_sum = 0.0, lift_sumsq = 0.0;
   double conflict_sum = 0.0, conflict_sumsq = 0.0;
   int lift_ge = 0, conflict_ge = 0;

   for(int iter = 0; iter < iterations; iter++)
   {
      if(stratified)
      {
         DAL_M0004StratifiedShuffleLabels(labels, strata, count, iter, 11701, tmp);
      }
      else
      {
         DAL_M0004BuildPermutation(count, iter, 11601, perm);
         ArrayResize(tmp, count);
         for(int i = 0; i < count; i++) tmp[i] = labels[perm[i]];
      }

      DALM0004ContextStats s;
      DAL_M0004ComputeContextStats(tmp, count, lookback, ewma_alpha, strong_threshold, use_ewma, s);
      if(s.dominant_lift_pct >= obs.dominant_lift_pct) lift_ge++;
      if(s.conflict_context_minus_last_pct >= obs.conflict_context_minus_last_pct) conflict_ge++;
      lift_sum += s.dominant_lift_pct;
      lift_sumsq += s.dominant_lift_pct * s.dominant_lift_pct;
      conflict_sum += s.conflict_context_minus_last_pct;
      conflict_sumsq += s.conflict_context_minus_last_pct * s.conflict_context_minus_last_pct;
   }

   double lift_mean = lift_sum / iterations;
   double conflict_mean = conflict_sum / iterations;
   double lift_sd = MathSqrt(MathMax(0.0, lift_sumsq / iterations - lift_mean * lift_mean));
   double conflict_sd = MathSqrt(MathMax(0.0, conflict_sumsq / iterations - conflict_mean * conflict_mean));
   double lift_z = lift_sd > 0.0 ? (obs.dominant_lift_pct - lift_mean) / lift_sd : 0.0;
   double conflict_z = conflict_sd > 0.0 ? (obs.conflict_context_minus_last_pct - conflict_mean) / conflict_sd : 0.0;
   double lift_p = (lift_ge + 1.0) / (iterations + 1.0);
   double conflict_p = (conflict_ge + 1.0) / (iterations + 1.0);

   int unique[];
   if(stratified)
      DAL_M0004UniqueKeys(strata, count, unique);

   string verdict = "context_state_not_above_null";
   if(lift_z > 2.0)
      verdict = "context_state_predictive_above_engineered_null";
   string null_name = stratified ? "stratified_composite" : "global_label_shuffle";
   string method_name = use_ewma ? "ewma" : "rolling";
   int strata_count = stratified ? ArraySize(unique) : 1;

   return "CONTEXT_SHUFFLE_STRESS"
      + "*name=" + name
      + "*null=" + null_name
      + "*n=" + IntegerToString(count)
      + "*strata=" + IntegerToString(strata_count)
      + "*iters=" + IntegerToString(iterations)
      + "*method=" + method_name
      + "*k=" + IntegerToString(lookback)
      + "*obsDominantLiftPct=" + DAL_M0001FmtPct(obs.dominant_lift_pct)
      + "*nullMeanDominantLiftPct=" + DAL_M0001FmtPct(lift_mean)
      + "*nullSdDominantLiftPct=" + DAL_M0001FmtPct(lift_sd)
      + "*dominantLiftZ=" + DAL_M0001Fmt4(lift_z)
      + "*dominantLiftEmpP=" + DAL_M0001Fmt4(lift_p)
      + "*obsConflictContextMinusLastPct=" + DAL_M0001FmtPct(obs.conflict_context_minus_last_pct)
      + "*nullMeanConflictContextMinusLastPct=" + DAL_M0001FmtPct(conflict_mean)
      + "*nullSdConflictContextMinusLastPct=" + DAL_M0001FmtPct(conflict_sd)
      + "*conflictAdvantageZ=" + DAL_M0001Fmt4(conflict_z)
      + "*conflictAdvantageEmpP=" + DAL_M0001Fmt4(conflict_p)
      + "*stressVerdict=" + verdict;
}


int DAL_M0004ContextDominantAt(
   const int &labels[],
   const int count,
   const int index,
   const int lookback,
   const double ewma_alpha,
   const double strong_threshold,
   const bool use_ewma,
   double &context_continuation_prob,
   double &context_confidence
)
{
   context_continuation_prob = 0.0;
   context_confidence = 0.0;

   if(index <= 0 || index >= count)
      return -1;

   int k = lookback;
   if(k < 1) k = 1;

   int start = index - k;
   if(start < 0) start = 0;
   int window = index - start;
   if(window <= 0)
      return -1;

   double alpha = ewma_alpha;
   if(alpha <= 0.0) alpha = 0.35;
   if(alpha >= 1.0) alpha = 0.99;
   double decay = 1.0 - alpha;

   double p = 0.0;
   if(use_ewma)
   {
      double w = 1.0;
      double sumw = 0.0;
      double score = 0.0;
      for(int j = index - 1; j >= start; j--)
      {
         score += w * labels[j];
         sumw += w;
         w *= decay;
      }
      p = sumw > 0.0 ? score / sumw : 0.0;
   }
   else
   {
      int cont = 0;
      for(int j = start; j < index; j++)
         if(labels[j] == DAL_M0004_LABEL_CONTINUATION)
            cont++;
      p = (double)cont / window;
   }

   double thr = strong_threshold;
   if(thr < 0.51) thr = 0.51;
   if(thr > 0.95) thr = 0.95;

   context_continuation_prob = p;
   context_confidence = MathAbs(2.0 * p - 1.0);

   if(p >= thr)
      return DAL_M0004_LABEL_CONTINUATION;
   if(p <= 1.0 - thr)
      return DAL_M0004_LABEL_REVERSAL;
   return -1;
}

double DAL_M0004MeanFromArray(const double &vals[])
{
   int n = ArraySize(vals);
   if(n <= 0)
      return 0.0;
   double s = 0.0;
   for(int i = 0; i < n; i++)
      s += vals[i];
   return s / n;
}

double DAL_M0004WinPctFromArray(const double &vals[])
{
   int n = ArraySize(vals);
   if(n <= 0)
      return 0.0;
   int wins = 0;
   for(int i = 0; i < n; i++)
      if(vals[i] > 0.0)
         wins++;
   return 100.0 * wins / n;
}

double DAL_M0004QuantileFromArray(const double &src[], const double q)
{
   int n = ArraySize(src);
   if(n <= 0)
      return 0.0;
   double vals[];
   ArrayResize(vals, n);
   for(int i = 0; i < n; i++)
      vals[i] = src[i];
   ArraySort(vals);
   double qq = q;
   if(qq < 0.0) qq = 0.0;
   if(qq > 1.0) qq = 1.0;
   int idx = (int)MathFloor((n - 1) * qq);
   if(idx < 0) idx = 0;
   if(idx >= n) idx = n - 1;
   return vals[idx];
}

void DAL_M0004AppendDouble(double &vals[], const double v)
{
   int n = ArraySize(vals);
   ArrayResize(vals, n + 1);
   vals[n] = v;
}


double DAL_M0004StdDevFromArray(const double &vals[])
{
   int n = ArraySize(vals);
   if(n <= 1)
      return 0.0;
   double mean = DAL_M0004MeanFromArray(vals);
   double ss = 0.0;
   for(int i = 0; i < n; i++)
   {
      double d = vals[i] - mean;
      ss += d * d;
   }
   return MathSqrt(ss / n);
}

struct DALM0004SignalQualityStats
{
   string name;
   int n;
   int evaluated;
   int signal_count;
   int no_signal_count;
   int signal_reversal_count;
   int signal_continuation_count;
   int current_continuation_count;
   int follow_count;
   int switch_count;
   int reversal_follow_count;
   int continuation_follow_count;
   double coverage_pct;
   double signal_continuation_pct;
   double current_continuation_pct;
   double follow_pct;
   double switch_pct;
   double expected_follow_pct;
   double lift_pct;
   double excess_follow_per_100_events;
   double reversal_next_reversal_pct;
   double continuation_next_continuation_pct;
   double mean_dlog;
   double med_dlog;
   double p90_dlog;
   double p95_dlog;
   double win_dlog_pct;
   double follow_mean_dlog;
   double switch_mean_dlog;
   double follow_win_dlog_pct;
   double switch_win_dlog_pct;
   double follow_minus_switch_dlog;
   double signal_reversal_mean_dlog;
   double signal_continuation_mean_dlog;
};

void DAL_M0004ResetSignalQualityStats(DALM0004SignalQualityStats &st, const string name, const int count)
{
   st.name = name;
   st.n = count;
   st.evaluated = 0;
   st.signal_count = 0;
   st.no_signal_count = 0;
   st.signal_reversal_count = 0;
   st.signal_continuation_count = 0;
   st.current_continuation_count = 0;
   st.follow_count = 0;
   st.switch_count = 0;
   st.reversal_follow_count = 0;
   st.continuation_follow_count = 0;
   st.coverage_pct = 0.0;
   st.signal_continuation_pct = 0.0;
   st.current_continuation_pct = 0.0;
   st.follow_pct = 0.0;
   st.switch_pct = 0.0;
   st.expected_follow_pct = 0.0;
   st.lift_pct = 0.0;
   st.excess_follow_per_100_events = 0.0;
   st.reversal_next_reversal_pct = 0.0;
   st.continuation_next_continuation_pct = 0.0;
   st.mean_dlog = 0.0;
   st.med_dlog = 0.0;
   st.p90_dlog = 0.0;
   st.p95_dlog = 0.0;
   st.win_dlog_pct = 0.0;
   st.follow_mean_dlog = 0.0;
   st.switch_mean_dlog = 0.0;
   st.follow_win_dlog_pct = 0.0;
   st.switch_win_dlog_pct = 0.0;
   st.follow_minus_switch_dlog = 0.0;
   st.signal_reversal_mean_dlog = 0.0;
   st.signal_continuation_mean_dlog = 0.0;
}

void DAL_M0004BuildLastOnlySignals(const int &labels[], const int count, int &signals[])
{
   ArrayResize(signals, count);
   for(int i = 0; i < count; i++)
      signals[i] = (i > 0 ? labels[i - 1] : -1);
}

void DAL_M0004BuildConsensusSignalPartitions(
   const int &labels[],
   const int count,
   const int lookback,
   const double ewma_alpha,
   const double strong_threshold,
   const bool use_ewma,
   int &consensus_signals[],
   int &rejected_last_signals[],
   int &conflict_last_signals[],
   int &conflict_context_signals[],
   int &neutral_last_signals[]
)
{
   ArrayResize(consensus_signals, count);
   ArrayResize(rejected_last_signals, count);
   ArrayResize(conflict_last_signals, count);
   ArrayResize(conflict_context_signals, count);
   ArrayResize(neutral_last_signals, count);

   for(int i = 0; i < count; i++)
   {
      consensus_signals[i] = -1;
      rejected_last_signals[i] = -1;
      conflict_last_signals[i] = -1;
      conflict_context_signals[i] = -1;
      neutral_last_signals[i] = -1;
   }

   for(int i = 1; i < count; i++)
   {
      double p = 0.0;
      double conf = 0.0;
      int dominant = DAL_M0004ContextDominantAt(labels, count, i, lookback, ewma_alpha, strong_threshold, use_ewma, p, conf);
      int last_label = labels[i - 1];
      if(dominant < 0)
      {
         neutral_last_signals[i] = last_label;
         rejected_last_signals[i] = last_label;
         continue;
      }
      if(dominant == last_label)
      {
         consensus_signals[i] = dominant;
         continue;
      }
      conflict_last_signals[i] = last_label;
      conflict_context_signals[i] = dominant;
      rejected_last_signals[i] = last_label;
   }
}

void DAL_M0004ComputeSignalQualityStats(
   const string name,
   const DALM0002BranchSample &samples[],
   const int &labels[],
   const int &signals[],
   const int count,
   DALM0004SignalQualityStats &st
)
{
   DAL_M0004ResetSignalQualityStats(st, name, count);
   if(count <= 1)
      return;

   int global_cont = 0;
   for(int i = 0; i < count; i++)
      if(labels[i] == DAL_M0004_LABEL_CONTINUATION)
         global_cont++;
   double global_cont_prob = (double)global_cont / count;
   double global_rev_prob = 1.0 - global_cont_prob;

   double expected_sum = 0.0;
   double all_dlogs[];
   double follow_dlogs[];
   double switch_dlogs[];
   double rev_signal_dlogs[];
   double cont_signal_dlogs[];

   st.evaluated = count - 1;
   for(int i = 1; i < count; i++)
   {
      int signal = (i < ArraySize(signals) ? signals[i] : -1);
      if(signal != DAL_M0004_LABEL_REVERSAL && signal != DAL_M0004_LABEL_CONTINUATION)
      {
         st.no_signal_count++;
         continue;
      }

      double dlog = (i < ArraySize(samples)) ? samples[i].delta_log : 0.0;
      st.signal_count++;
      if(labels[i] == DAL_M0004_LABEL_CONTINUATION)
         st.current_continuation_count++;
      DAL_M0004AppendDouble(all_dlogs, dlog);

      if(signal == DAL_M0004_LABEL_CONTINUATION)
      {
         st.signal_continuation_count++;
         expected_sum += global_cont_prob;
         DAL_M0004AppendDouble(cont_signal_dlogs, dlog);
         if(labels[i] == DAL_M0004_LABEL_CONTINUATION)
            st.continuation_follow_count++;
      }
      else
      {
         st.signal_reversal_count++;
         expected_sum += global_rev_prob;
         DAL_M0004AppendDouble(rev_signal_dlogs, dlog);
         if(labels[i] == DAL_M0004_LABEL_REVERSAL)
            st.reversal_follow_count++;
      }

      if(labels[i] == signal)
      {
         st.follow_count++;
         DAL_M0004AppendDouble(follow_dlogs, dlog);
      }
      else
      {
         st.switch_count++;
         DAL_M0004AppendDouble(switch_dlogs, dlog);
      }
   }

   if(st.evaluated > 0)
      st.coverage_pct = 100.0 * st.signal_count / st.evaluated;
   if(st.signal_count > 0)
   {
      st.signal_continuation_pct = 100.0 * st.signal_continuation_count / st.signal_count;
      st.current_continuation_pct = 100.0 * st.current_continuation_count / st.signal_count;
      st.follow_pct = 100.0 * st.follow_count / st.signal_count;
      st.switch_pct = 100.0 * st.switch_count / st.signal_count;
      st.expected_follow_pct = 100.0 * expected_sum / st.signal_count;
      st.lift_pct = st.follow_pct - st.expected_follow_pct;
      st.excess_follow_per_100_events = (st.coverage_pct * st.lift_pct) / 100.0;
   }
   if(st.signal_reversal_count > 0)
      st.reversal_next_reversal_pct = 100.0 * st.reversal_follow_count / st.signal_reversal_count;
   if(st.signal_continuation_count > 0)
      st.continuation_next_continuation_pct = 100.0 * st.continuation_follow_count / st.signal_continuation_count;

   st.mean_dlog = DAL_M0004MeanFromArray(all_dlogs);
   st.med_dlog = DAL_M0004QuantileFromArray(all_dlogs, 0.50);
   st.p90_dlog = DAL_M0004QuantileFromArray(all_dlogs, 0.90);
   st.p95_dlog = DAL_M0004QuantileFromArray(all_dlogs, 0.95);
   st.win_dlog_pct = DAL_M0004WinPctFromArray(all_dlogs);
   st.follow_mean_dlog = DAL_M0004MeanFromArray(follow_dlogs);
   st.switch_mean_dlog = DAL_M0004MeanFromArray(switch_dlogs);
   st.follow_win_dlog_pct = DAL_M0004WinPctFromArray(follow_dlogs);
   st.switch_win_dlog_pct = DAL_M0004WinPctFromArray(switch_dlogs);
   st.follow_minus_switch_dlog = st.follow_mean_dlog - st.switch_mean_dlog;
   st.signal_reversal_mean_dlog = DAL_M0004MeanFromArray(rev_signal_dlogs);
   st.signal_continuation_mean_dlog = DAL_M0004MeanFromArray(cont_signal_dlogs);
}

string DAL_M0004SignalQualityCountsText(const string tag, const string method, const DALM0004SignalQualityStats &st)
{
   return tag
      + "*method=" + method
      + "*name=" + st.name
      + "*n=" + IntegerToString(st.n)
      + "*evaluated=" + IntegerToString(st.evaluated)
      + "*signalN=" + IntegerToString(st.signal_count)
      + "*noSignalN=" + IntegerToString(st.no_signal_count)
      + "*coveragePct=" + DAL_M0001FmtPct(st.coverage_pct)
      + "*signalRevN=" + IntegerToString(st.signal_reversal_count)
      + "*signalContN=" + IntegerToString(st.signal_continuation_count)
      + "*signalContPct=" + DAL_M0001FmtPct(st.signal_continuation_pct)
      + "*currentContPct=" + DAL_M0001FmtPct(st.current_continuation_pct);
}

string DAL_M0004SignalQualityFollowText(const string tag, const string method, const DALM0004SignalQualityStats &st)
{
   return tag
      + "*method=" + method
      + "*name=" + st.name
      + "*signalN=" + IntegerToString(st.signal_count)
      + "*followN=" + IntegerToString(st.follow_count)
      + "*switchN=" + IntegerToString(st.switch_count)
      + "*followPct=" + DAL_M0001FmtPct(st.follow_pct)
      + "*switchPct=" + DAL_M0001FmtPct(st.switch_pct)
      + "*expectedFollowPct=" + DAL_M0001FmtPct(st.expected_follow_pct)
      + "*liftPct=" + DAL_M0001FmtPct(st.lift_pct)
      + "*excessFollowPer100Events=" + DAL_M0001Fmt4(st.excess_follow_per_100_events)
      + "*revNextRevPct=" + DAL_M0001FmtPct(st.reversal_next_reversal_pct)
      + "*contNextContPct=" + DAL_M0001FmtPct(st.continuation_next_continuation_pct);
}

string DAL_M0004SignalQualityIntensityText(const string tag, const string method, const DALM0004SignalQualityStats &st)
{
   return tag
      + "*method=" + method
      + "*name=" + st.name
      + "*meanDLog=" + DAL_M0001Fmt4(st.mean_dlog)
      + "*medDLog=" + DAL_M0001Fmt4(st.med_dlog)
      + "*p90DLog=" + DAL_M0001Fmt4(st.p90_dlog)
      + "*p95DLog=" + DAL_M0001Fmt4(st.p95_dlog)
      + "*winDLogPct=" + DAL_M0001FmtPct(st.win_dlog_pct)
      + "*followMeanDLog=" + DAL_M0001Fmt4(st.follow_mean_dlog)
      + "*switchMeanDLog=" + DAL_M0001Fmt4(st.switch_mean_dlog)
      + "*followMinusSwitchDLog=" + DAL_M0001Fmt4(st.follow_minus_switch_dlog)
      + "*followWinDLogPct=" + DAL_M0001FmtPct(st.follow_win_dlog_pct)
      + "*switchWinDLogPct=" + DAL_M0001FmtPct(st.switch_win_dlog_pct);
}

string DAL_M0004SignalQualityBranchIntensityText(const string tag, const string method, const DALM0004SignalQualityStats &st)
{
   return tag
      + "*method=" + method
      + "*name=" + st.name
      + "*signalRevN=" + IntegerToString(st.signal_reversal_count)
      + "*signalContN=" + IntegerToString(st.signal_continuation_count)
      + "*revNextRevPct=" + DAL_M0001FmtPct(st.reversal_next_reversal_pct)
      + "*contNextContPct=" + DAL_M0001FmtPct(st.continuation_next_continuation_pct)
      + "*revSignalMeanDLog=" + DAL_M0001Fmt4(st.signal_reversal_mean_dlog)
      + "*contSignalMeanDLog=" + DAL_M0001Fmt4(st.signal_continuation_mean_dlog)
      + "*contMinusRevSignalMeanDLog=" + DAL_M0001Fmt4(st.signal_continuation_mean_dlog - st.signal_reversal_mean_dlog);
}

string DAL_M0004SignalQualityCompareText(
   const string tag,
   const string method,
   const DALM0004SignalQualityStats &last_only,
   const DALM0004SignalQualityStats &accepted,
   const DALM0004SignalQualityStats &rejected_last,
   const DALM0004SignalQualityStats &conflict_last,
   const DALM0004SignalQualityStats &neutral_last
)
{
   string model = "consensus_does_not_improve_last_only_selection";
   double accepted_vs_rejected_follow = accepted.follow_pct - rejected_last.follow_pct;
   double accepted_vs_last_follow = accepted.follow_pct - last_only.follow_pct;
   double accepted_vs_rejected_lift = accepted.lift_pct - rejected_last.lift_pct;
   double accepted_vs_last_lift = accepted.lift_pct - last_only.lift_pct;
   double accepted_vs_rejected_dlog = accepted.mean_dlog - rejected_last.mean_dlog;
   double accepted_vs_last_dlog = accepted.mean_dlog - last_only.mean_dlog;
   if(accepted_vs_rejected_follow > 0.0 && accepted_vs_rejected_lift > 0.0)
      model = "consensus_filters_higher_quality_last_branch_signals";
   if(accepted_vs_last_follow > 0.0 && accepted_vs_last_lift > 0.0 && accepted.coverage_pct > 50.0)
      model = "consensus_improves_last_only_while_preserving_broad_coverage";
   if(accepted_vs_rejected_follow <= 0.0 && accepted_vs_rejected_lift > 0.0)
      model = "consensus_improves_calibration_lift_but_not_raw_follow_rate";

   return tag
      + "*method=" + method
      + "*lastFollowPct=" + DAL_M0001FmtPct(last_only.follow_pct)
      + "*consensusFollowPct=" + DAL_M0001FmtPct(accepted.follow_pct)
      + "*rejectedLastFollowPct=" + DAL_M0001FmtPct(rejected_last.follow_pct)
      + "*conflictLastFollowPct=" + DAL_M0001FmtPct(conflict_last.follow_pct)
      + "*neutralLastFollowPct=" + DAL_M0001FmtPct(neutral_last.follow_pct)
      + "*consensusMinusLastFollow=" + DAL_M0001FmtPct(accepted_vs_last_follow)
      + "*consensusMinusRejectedFollow=" + DAL_M0001FmtPct(accepted_vs_rejected_follow)
      + "*lastLiftPct=" + DAL_M0001FmtPct(last_only.lift_pct)
      + "*consensusLiftPct=" + DAL_M0001FmtPct(accepted.lift_pct)
      + "*rejectedLastLiftPct=" + DAL_M0001FmtPct(rejected_last.lift_pct)
      + "*consensusMinusLastLift=" + DAL_M0001FmtPct(accepted_vs_last_lift)
      + "*consensusMinusRejectedLift=" + DAL_M0001FmtPct(accepted_vs_rejected_lift)
      + "*consensusCoveragePct=" + DAL_M0001FmtPct(accepted.coverage_pct)
      + "*rejectedCoveragePct=" + DAL_M0001FmtPct(rejected_last.coverage_pct)
      + "*consensusMinusLastMeanDLog=" + DAL_M0001Fmt4(accepted_vs_last_dlog)
      + "*consensusMinusRejectedMeanDLog=" + DAL_M0001Fmt4(accepted_vs_rejected_dlog)
      + "*qualityModel=" + model;
}

string DAL_M0004SignalQualityBlockProfileText(
   const string tag,
   const string method,
   const int &labels[],
   const int &signals[],
   const int count,
   const int block_size
)
{
   if(count <= 2)
      return tag + "*method=" + method + "*n=" + IntegerToString(count) + "*blocks=0";

   int bs = block_size;
   if(bs < 5) bs = 5;

   int global_cont = 0;
   for(int i = 0; i < count; i++)
      if(labels[i] == DAL_M0004_LABEL_CONTINUATION)
         global_cont++;
   double global_cont_prob = (double)global_cont / count;
   double global_rev_prob = 1.0 - global_cont_prob;

   double follow_pcts[];
   double lift_pcts[];
   double coverage_pcts[];
   int positive_lift_blocks = 0;
   int positive_follow_blocks = 0;
   int used_blocks = 0;

   for(int start = 1; start < count; start += bs)
   {
      int end = start + bs;
      if(end > count) end = count;
      int block_total = end - start;
      int signal_count = 0;
      int follow_count = 0;
      double expected_sum = 0.0;
      for(int i = start; i < end; i++)
      {
         int signal = (i < ArraySize(signals) ? signals[i] : -1);
         if(signal != DAL_M0004_LABEL_REVERSAL && signal != DAL_M0004_LABEL_CONTINUATION)
            continue;
         signal_count++;
         if(labels[i] == signal)
            follow_count++;
         expected_sum += (signal == DAL_M0004_LABEL_CONTINUATION ? global_cont_prob : global_rev_prob);
      }
      if(signal_count <= 0)
         continue;
      double follow_pct = 100.0 * follow_count / signal_count;
      double expected_pct = 100.0 * expected_sum / signal_count;
      double lift_pct = follow_pct - expected_pct;
      double coverage_pct = 100.0 * signal_count / block_total;
      DAL_M0004AppendDouble(follow_pcts, follow_pct);
      DAL_M0004AppendDouble(lift_pcts, lift_pct);
      DAL_M0004AppendDouble(coverage_pcts, coverage_pct);
      if(lift_pct > 0.0) positive_lift_blocks++;
      if(follow_pct > expected_pct) positive_follow_blocks++;
      used_blocks++;
   }

   return tag
      + "*method=" + method
      + "*n=" + IntegerToString(count)
      + "*blockSize=" + IntegerToString(bs)
      + "*blocks=" + IntegerToString(used_blocks)
      + "*meanFollowPct=" + DAL_M0001FmtPct(DAL_M0004MeanFromArray(follow_pcts))
      + "*sdFollowPct=" + DAL_M0001FmtPct(DAL_M0004StdDevFromArray(follow_pcts))
      + "*minFollowPct=" + DAL_M0001FmtPct(DAL_M0004QuantileFromArray(follow_pcts, 0.00))
      + "*maxFollowPct=" + DAL_M0001FmtPct(DAL_M0004QuantileFromArray(follow_pcts, 1.00))
      + "*meanLiftPct=" + DAL_M0001FmtPct(DAL_M0004MeanFromArray(lift_pcts))
      + "*sdLiftPct=" + DAL_M0001FmtPct(DAL_M0004StdDevFromArray(lift_pcts))
      + "*positiveLiftBlockPct=" + DAL_M0001FmtPct(used_blocks > 0 ? 100.0 * positive_lift_blocks / used_blocks : 0.0)
      + "*meanCoveragePct=" + DAL_M0001FmtPct(DAL_M0004MeanFromArray(coverage_pcts))
      + "*minCoveragePct=" + DAL_M0001FmtPct(DAL_M0004QuantileFromArray(coverage_pcts, 0.00))
      + "*maxCoveragePct=" + DAL_M0001FmtPct(DAL_M0004QuantileFromArray(coverage_pcts, 1.00));
}

struct DALM0004ConsensusStats
{
   int n;
   int evaluated;
   int dominant_count;
   int neutral_count;
   int consensus_count;
   int conflict_count;
   int consensus_reversal_count;
   int consensus_continuation_count;
   int consensus_follow_count;
   int consensus_switch_count;
   int consensus_reversal_follow_count;
   int consensus_continuation_follow_count;
   int current_continuation_count;
   double global_continuation_pct;
   double consensus_pct;
   double conflict_pct;
   double neutral_pct;
   double consensus_signal_continuation_pct;
   double consensus_current_continuation_pct;
   double consensus_follow_pct;
   double consensus_switch_pct;
   double consensus_expected_follow_pct;
   double consensus_lift_pct;
   double consensus_reversal_next_reversal_pct;
   double consensus_continuation_next_continuation_pct;
   double consensus_mean_context_continuation_pct;
   double consensus_mean_confidence_pct;
   double consensus_mean_dlog;
   double consensus_median_dlog;
   double consensus_p90_dlog;
   double consensus_p95_dlog;
   double consensus_win_dlog_pct;
   double consensus_follow_mean_dlog;
   double consensus_switch_mean_dlog;
   double consensus_follow_win_dlog_pct;
   double consensus_switch_win_dlog_pct;
   double consensus_follow_minus_switch_dlog;
   double conflict_mean_dlog;
   double neutral_mean_dlog;
   double consensus_reversal_mean_dlog;
   double consensus_continuation_mean_dlog;
};

void DAL_M0004ComputeConsensusStats(
   const DALM0002BranchSample &samples[],
   const int &labels[],
   const int count,
   const int lookback,
   const double ewma_alpha,
   const double strong_threshold,
   const bool use_ewma,
   DALM0004ConsensusStats &st
)
{
   st.n = count;
   st.evaluated = 0;
   st.dominant_count = 0;
   st.neutral_count = 0;
   st.consensus_count = 0;
   st.conflict_count = 0;
   st.consensus_reversal_count = 0;
   st.consensus_continuation_count = 0;
   st.consensus_follow_count = 0;
   st.consensus_switch_count = 0;
   st.consensus_reversal_follow_count = 0;
   st.consensus_continuation_follow_count = 0;
   st.current_continuation_count = 0;
   st.global_continuation_pct = 0.0;
   st.consensus_pct = 0.0;
   st.conflict_pct = 0.0;
   st.neutral_pct = 0.0;
   st.consensus_signal_continuation_pct = 0.0;
   st.consensus_current_continuation_pct = 0.0;
   st.consensus_follow_pct = 0.0;
   st.consensus_switch_pct = 0.0;
   st.consensus_expected_follow_pct = 0.0;
   st.consensus_lift_pct = 0.0;
   st.consensus_reversal_next_reversal_pct = 0.0;
   st.consensus_continuation_next_continuation_pct = 0.0;
   st.consensus_mean_context_continuation_pct = 0.0;
   st.consensus_mean_confidence_pct = 0.0;
   st.consensus_mean_dlog = 0.0;
   st.consensus_median_dlog = 0.0;
   st.consensus_p90_dlog = 0.0;
   st.consensus_p95_dlog = 0.0;
   st.consensus_win_dlog_pct = 0.0;
   st.consensus_follow_mean_dlog = 0.0;
   st.consensus_switch_mean_dlog = 0.0;
   st.consensus_follow_win_dlog_pct = 0.0;
   st.consensus_switch_win_dlog_pct = 0.0;
   st.consensus_follow_minus_switch_dlog = 0.0;
   st.conflict_mean_dlog = 0.0;
   st.neutral_mean_dlog = 0.0;
   st.consensus_reversal_mean_dlog = 0.0;
   st.consensus_continuation_mean_dlog = 0.0;

   if(count <= 1)
      return;

   int global_cont = 0;
   for(int i = 0; i < count; i++)
      if(labels[i] == DAL_M0004_LABEL_CONTINUATION)
         global_cont++;
   double global_cont_prob = (double)global_cont / count;
   double global_rev_prob = 1.0 - global_cont_prob;
   st.global_continuation_pct = 100.0 * global_cont_prob;

   double consensus_context_p_sum = 0.0;
   double consensus_confidence_sum = 0.0;
   double consensus_expected_follow_sum = 0.0;
   int consensus_current_cont = 0;

   double consensus_dlogs[];
   double conflict_dlogs[];
   double neutral_dlogs[];
   double consensus_follow_dlogs[];
   double consensus_switch_dlogs[];
   double consensus_rev_dlogs[];
   double consensus_cont_dlogs[];

   for(int i = 1; i < count; i++)
   {
      double p = 0.0;
      double conf = 0.0;
      int dominant = DAL_M0004ContextDominantAt(labels, count, i, lookback, ewma_alpha, strong_threshold, use_ewma, p, conf);
      double dlog = (i < ArraySize(samples)) ? samples[i].delta_log : 0.0;

      st.evaluated++;
      if(labels[i] == DAL_M0004_LABEL_CONTINUATION)
         st.current_continuation_count++;

      if(dominant < 0)
      {
         st.neutral_count++;
         DAL_M0004AppendDouble(neutral_dlogs, dlog);
         continue;
      }

      st.dominant_count++;
      int last_label = labels[i - 1];
      if(last_label != dominant)
      {
         st.conflict_count++;
         DAL_M0004AppendDouble(conflict_dlogs, dlog);
         continue;
      }

      st.consensus_count++;
      consensus_context_p_sum += p;
      consensus_confidence_sum += conf;
      DAL_M0004AppendDouble(consensus_dlogs, dlog);

      if(dominant == DAL_M0004_LABEL_CONTINUATION)
      {
         st.consensus_continuation_count++;
         consensus_expected_follow_sum += global_cont_prob;
         DAL_M0004AppendDouble(consensus_cont_dlogs, dlog);
         if(labels[i] == DAL_M0004_LABEL_CONTINUATION)
            st.consensus_continuation_follow_count++;
      }
      else
      {
         st.consensus_reversal_count++;
         consensus_expected_follow_sum += global_rev_prob;
         DAL_M0004AppendDouble(consensus_rev_dlogs, dlog);
         if(labels[i] == DAL_M0004_LABEL_REVERSAL)
            st.consensus_reversal_follow_count++;
      }

      if(labels[i] == DAL_M0004_LABEL_CONTINUATION)
         consensus_current_cont++;

      if(labels[i] == dominant)
      {
         st.consensus_follow_count++;
         DAL_M0004AppendDouble(consensus_follow_dlogs, dlog);
      }
      else
      {
         st.consensus_switch_count++;
         DAL_M0004AppendDouble(consensus_switch_dlogs, dlog);
      }
   }

   if(st.evaluated > 0)
   {
      st.consensus_pct = 100.0 * st.consensus_count / st.evaluated;
      st.conflict_pct = 100.0 * st.conflict_count / st.evaluated;
      st.neutral_pct = 100.0 * st.neutral_count / st.evaluated;
   }
   if(st.consensus_count > 0)
   {
      st.consensus_signal_continuation_pct = 100.0 * st.consensus_continuation_count / st.consensus_count;
      st.consensus_current_continuation_pct = 100.0 * consensus_current_cont / st.consensus_count;
      st.consensus_follow_pct = 100.0 * st.consensus_follow_count / st.consensus_count;
      st.consensus_switch_pct = 100.0 * st.consensus_switch_count / st.consensus_count;
      st.consensus_expected_follow_pct = 100.0 * consensus_expected_follow_sum / st.consensus_count;
      st.consensus_lift_pct = st.consensus_follow_pct - st.consensus_expected_follow_pct;
      st.consensus_mean_context_continuation_pct = 100.0 * consensus_context_p_sum / st.consensus_count;
      st.consensus_mean_confidence_pct = 100.0 * consensus_confidence_sum / st.consensus_count;
   }
   if(st.consensus_reversal_count > 0)
      st.consensus_reversal_next_reversal_pct = 100.0 * st.consensus_reversal_follow_count / st.consensus_reversal_count;
   if(st.consensus_continuation_count > 0)
      st.consensus_continuation_next_continuation_pct = 100.0 * st.consensus_continuation_follow_count / st.consensus_continuation_count;

   st.consensus_mean_dlog = DAL_M0004MeanFromArray(consensus_dlogs);
   st.consensus_median_dlog = DAL_M0004QuantileFromArray(consensus_dlogs, 0.50);
   st.consensus_p90_dlog = DAL_M0004QuantileFromArray(consensus_dlogs, 0.90);
   st.consensus_p95_dlog = DAL_M0004QuantileFromArray(consensus_dlogs, 0.95);
   st.consensus_win_dlog_pct = DAL_M0004WinPctFromArray(consensus_dlogs);
   st.consensus_follow_mean_dlog = DAL_M0004MeanFromArray(consensus_follow_dlogs);
   st.consensus_switch_mean_dlog = DAL_M0004MeanFromArray(consensus_switch_dlogs);
   st.consensus_follow_win_dlog_pct = DAL_M0004WinPctFromArray(consensus_follow_dlogs);
   st.consensus_switch_win_dlog_pct = DAL_M0004WinPctFromArray(consensus_switch_dlogs);
   st.consensus_follow_minus_switch_dlog = st.consensus_follow_mean_dlog - st.consensus_switch_mean_dlog;
   st.conflict_mean_dlog = DAL_M0004MeanFromArray(conflict_dlogs);
   st.neutral_mean_dlog = DAL_M0004MeanFromArray(neutral_dlogs);
   st.consensus_reversal_mean_dlog = DAL_M0004MeanFromArray(consensus_rev_dlogs);
   st.consensus_continuation_mean_dlog = DAL_M0004MeanFromArray(consensus_cont_dlogs);
}

string DAL_M0004ConsensusStatsText(
   const string tag,
   const string method,
   const DALM0002BranchSample &samples[],
   const int &labels[],
   const int count,
   const int lookback,
   const double ewma_alpha,
   const double strong_threshold,
   const bool use_ewma
)
{
   DALM0004ConsensusStats st;
   DAL_M0004ComputeConsensusStats(samples, labels, count, lookback, ewma_alpha, strong_threshold, use_ewma, st);

   string model = "consensus_not_available";
   if(st.consensus_count > 0 && st.consensus_lift_pct > 0.0)
      model = "last_branch_and_context_consensus_has_predictive_lift";
   if(st.consensus_count > 0 && st.consensus_lift_pct > 0.0 && st.consensus_follow_minus_switch_dlog > 0.0)
      model = "consensus_predicts_branch_and_following_events_are_stronger";

   return tag
      + "*method=" + method
      + "*k=" + IntegerToString(lookback)
      + "*alpha=" + DAL_M0001Fmt4(ewma_alpha)
      + "*threshold=" + DAL_M0001Fmt4(strong_threshold)
      + "*n=" + IntegerToString(count)
      + "*evaluated=" + IntegerToString(st.evaluated)
      + "*dominantN=" + IntegerToString(st.dominant_count)
      + "*consensusN=" + IntegerToString(st.consensus_count)
      + "*conflictN=" + IntegerToString(st.conflict_count)
      + "*neutralN=" + IntegerToString(st.neutral_count)
      + "*consensusPct=" + DAL_M0001FmtPct(st.consensus_pct)
      + "*conflictPct=" + DAL_M0001FmtPct(st.conflict_pct)
      + "*neutralPct=" + DAL_M0001FmtPct(st.neutral_pct)
      + "*globalContPct=" + DAL_M0001FmtPct(st.global_continuation_pct)
      + "*consensusSignalContPct=" + DAL_M0001FmtPct(st.consensus_signal_continuation_pct)
      + "*consensusCurrentContPct=" + DAL_M0001FmtPct(st.consensus_current_continuation_pct)
      + "*consensusFollowPct=" + DAL_M0001FmtPct(st.consensus_follow_pct)
      + "*consensusSwitchPct=" + DAL_M0001FmtPct(st.consensus_switch_pct)
      + "*expectedFollowPct=" + DAL_M0001FmtPct(st.consensus_expected_follow_pct)
      + "*consensusLiftPct=" + DAL_M0001FmtPct(st.consensus_lift_pct)
      + "*consensusRevN=" + IntegerToString(st.consensus_reversal_count)
      + "*consensusContN=" + IntegerToString(st.consensus_continuation_count)
      + "*consensusRevNextRevPct=" + DAL_M0001FmtPct(st.consensus_reversal_next_reversal_pct)
      + "*consensusContNextContPct=" + DAL_M0001FmtPct(st.consensus_continuation_next_continuation_pct)
      + "*consensusMeanContextContPct=" + DAL_M0001FmtPct(st.consensus_mean_context_continuation_pct)
      + "*consensusConfidencePct=" + DAL_M0001FmtPct(st.consensus_mean_confidence_pct)
      + "*consensusMeanDLog=" + DAL_M0001Fmt4(st.consensus_mean_dlog)
      + "*consensusMedDLog=" + DAL_M0001Fmt4(st.consensus_median_dlog)
      + "*consensusP90DLog=" + DAL_M0001Fmt4(st.consensus_p90_dlog)
      + "*consensusP95DLog=" + DAL_M0001Fmt4(st.consensus_p95_dlog)
      + "*consensusWinDLogPct=" + DAL_M0001FmtPct(st.consensus_win_dlog_pct)
      + "*consensusFollowMeanDLog=" + DAL_M0001Fmt4(st.consensus_follow_mean_dlog)
      + "*consensusSwitchMeanDLog=" + DAL_M0001Fmt4(st.consensus_switch_mean_dlog)
      + "*consensusFollowWinDLogPct=" + DAL_M0001FmtPct(st.consensus_follow_win_dlog_pct)
      + "*consensusSwitchWinDLogPct=" + DAL_M0001FmtPct(st.consensus_switch_win_dlog_pct)
      + "*followMinusSwitchDLog=" + DAL_M0001Fmt4(st.consensus_follow_minus_switch_dlog)
      + "*consensusRevMeanDLog=" + DAL_M0001Fmt4(st.consensus_reversal_mean_dlog)
      + "*consensusContMeanDLog=" + DAL_M0001Fmt4(st.consensus_continuation_mean_dlog)
      + "*conflictMeanDLog=" + DAL_M0001Fmt4(st.conflict_mean_dlog)
      + "*neutralMeanDLog=" + DAL_M0001Fmt4(st.neutral_mean_dlog)
      + "*consensusModel=" + model;
}

string DAL_M0004ConsensusShuffleStressText(
   const string name,
   const DALM0002BranchSample &samples[],
   const int &labels[],
   const int &strata[],
   const int count,
   const int lookback,
   const double ewma_alpha,
   const double strong_threshold,
   const bool use_ewma,
   const int iterations,
   const bool stratified
)
{
   if(count <= lookback + 5 || iterations <= 0)
      return "CONSENSUS_SHUFFLE_STRESS*name=" + name + "*n=" + IntegerToString(count) + "*iters=0";

   DALM0004ConsensusStats obs;
   DAL_M0004ComputeConsensusStats(samples, labels, count, lookback, ewma_alpha, strong_threshold, use_ewma, obs);

   int tmp[];
   int perm[];
   double lift_sum = 0.0, lift_sumsq = 0.0;
   double follow_sum = 0.0, follow_sumsq = 0.0;
   double consensus_pct_sum = 0.0, consensus_pct_sumsq = 0.0;
   int lift_ge = 0, follow_ge = 0, pct_ge = 0;

   for(int iter = 0; iter < iterations; iter++)
   {
      if(stratified)
      {
         DAL_M0004StratifiedShuffleLabels(labels, strata, count, iter, 12701, tmp);
      }
      else
      {
         DAL_M0004BuildPermutation(count, iter, 12601, perm);
         ArrayResize(tmp, count);
         for(int i = 0; i < count; i++)
            tmp[i] = labels[perm[i]];
      }

      DALM0004ConsensusStats s;
      DAL_M0004ComputeConsensusStats(samples, tmp, count, lookback, ewma_alpha, strong_threshold, use_ewma, s);
      if(s.consensus_lift_pct >= obs.consensus_lift_pct) lift_ge++;
      if(s.consensus_follow_pct >= obs.consensus_follow_pct) follow_ge++;
      if(s.consensus_pct >= obs.consensus_pct) pct_ge++;
      lift_sum += s.consensus_lift_pct;
      lift_sumsq += s.consensus_lift_pct * s.consensus_lift_pct;
      follow_sum += s.consensus_follow_pct;
      follow_sumsq += s.consensus_follow_pct * s.consensus_follow_pct;
      consensus_pct_sum += s.consensus_pct;
      consensus_pct_sumsq += s.consensus_pct * s.consensus_pct;
   }

   double lift_mean = lift_sum / iterations;
   double follow_mean = follow_sum / iterations;
   double pct_mean = consensus_pct_sum / iterations;
   double lift_sd = MathSqrt(MathMax(0.0, lift_sumsq / iterations - lift_mean * lift_mean));
   double follow_sd = MathSqrt(MathMax(0.0, follow_sumsq / iterations - follow_mean * follow_mean));
   double pct_sd = MathSqrt(MathMax(0.0, consensus_pct_sumsq / iterations - pct_mean * pct_mean));
   double lift_z = lift_sd > 0.0 ? (obs.consensus_lift_pct - lift_mean) / lift_sd : 0.0;
   double follow_z = follow_sd > 0.0 ? (obs.consensus_follow_pct - follow_mean) / follow_sd : 0.0;
   double pct_z = pct_sd > 0.0 ? (obs.consensus_pct - pct_mean) / pct_sd : 0.0;
   double lift_p = (lift_ge + 1.0) / (iterations + 1.0);
   double follow_p = (follow_ge + 1.0) / (iterations + 1.0);
   double pct_p = (pct_ge + 1.0) / (iterations + 1.0);

   int unique[];
   if(stratified)
      DAL_M0004UniqueKeys(strata, count, unique);

   string verdict = "consensus_state_not_above_null";
   if(lift_z > 2.0 && follow_z > 2.0)
      verdict = "last_context_consensus_predictive_above_engineered_null";
   string null_name = stratified ? "stratified_composite" : "global_label_shuffle";
   string method_name = use_ewma ? "ewma" : "rolling";
   int strata_count = stratified ? ArraySize(unique) : 1;

   return "CONSENSUS_SHUFFLE_STRESS"
      + "*name=" + name
      + "*null=" + null_name
      + "*n=" + IntegerToString(count)
      + "*strata=" + IntegerToString(strata_count)
      + "*iters=" + IntegerToString(iterations)
      + "*method=" + method_name
      + "*k=" + IntegerToString(lookback)
      + "*obsConsensusPct=" + DAL_M0001FmtPct(obs.consensus_pct)
      + "*nullMeanConsensusPct=" + DAL_M0001FmtPct(pct_mean)
      + "*nullSdConsensusPct=" + DAL_M0001FmtPct(pct_sd)
      + "*consensusPctZ=" + DAL_M0001Fmt4(pct_z)
      + "*consensusPctEmpP=" + DAL_M0001Fmt4(pct_p)
      + "*obsConsensusFollowPct=" + DAL_M0001FmtPct(obs.consensus_follow_pct)
      + "*nullMeanConsensusFollowPct=" + DAL_M0001FmtPct(follow_mean)
      + "*nullSdConsensusFollowPct=" + DAL_M0001FmtPct(follow_sd)
      + "*consensusFollowZ=" + DAL_M0001Fmt4(follow_z)
      + "*consensusFollowEmpP=" + DAL_M0001Fmt4(follow_p)
      + "*obsConsensusLiftPct=" + DAL_M0001FmtPct(obs.consensus_lift_pct)
      + "*nullMeanConsensusLiftPct=" + DAL_M0001FmtPct(lift_mean)
      + "*nullSdConsensusLiftPct=" + DAL_M0001FmtPct(lift_sd)
      + "*consensusLiftZ=" + DAL_M0001Fmt4(lift_z)
      + "*consensusLiftEmpP=" + DAL_M0001Fmt4(lift_p)
      + "*stressVerdict=" + verdict;
}

string DAL_M0004SummaryText(const DALM0004TransitionStats &s, const DALM0004RunStats &rev, const DALM0004RunStats &cont)
{
   string state = "mixed_or_no_branch_regime";
   bool count_imbalance = s.reversal_count > s.continuation_count;
   bool same_inertia = s.same_lift > 0.0 && s.lag1_corr > 0.0;
   bool both_persist = s.reversal_persistence_lift > 0.0 && s.continuation_persistence_lift > 0.0;
   bool run_cluster = rev.avg_run_over_iid > 1.0 && cont.avg_run_over_iid > 1.0;

   if(same_inertia)
      state = "branch_labels_have_positive_inertia";
   if(same_inertia && both_persist)
      state = "reversal_and_continuation_are_markov_like_regimes";
   if(count_imbalance && same_inertia && both_persist && run_cluster)
      state = "reversal_more_frequent_continuation_less_frequent_both_cluster_as_regimes";

   return "H0004_SUMMARY"
      + "*n=" + IntegerToString(s.n)
      + "*reversalN=" + IntegerToString(s.reversal_count)
      + "*continuationN=" + IntegerToString(s.continuation_count)
      + "*reversalPct=" + DAL_M0001FmtPct(s.reversal_pct)
      + "*continuationPct=" + DAL_M0001FmtPct(s.continuation_pct)
      + "*countRatioRevToCont=" + DAL_M0001Fmt4(DAL_M0004SafeRatio(s.reversal_count, s.continuation_count))
      + "*sameLiftPct=" + DAL_M0001FmtPct(s.same_lift)
      + "*lag1Corr=" + DAL_M0001Fmt4(s.lag1_corr)
      + "*lag2Corr=" + DAL_M0001Fmt4(s.lag2_corr)
      + "*revPersistenceLift=" + DAL_M0001FmtPct(s.reversal_persistence_lift)
      + "*contPersistenceLift=" + DAL_M0001FmtPct(s.continuation_persistence_lift)
      + "*revAvgRunOverIid=" + DAL_M0001Fmt4(rev.avg_run_over_iid)
      + "*contAvgRunOverIid=" + DAL_M0001Fmt4(cont.avg_run_over_iid)
      + "*hypothesisState=" + state;
}

void DAL_M0004PrintFinalReports(
   const DALM0001Event &events[],
   const int events_count,
   const DALBar &bars[],
   const int bars_count,
   const string symbol,
   const string timeframe,
   const string source_mode,
   const datetime min_entry_time,
   const DALM0002Config &h2_config,
   const DALM0004Config &h4_config
)
{
   DALM0002BranchSample all_samples[];
   DALM0002BranchSample reversal_samples[];
   DALM0002BranchSample continuation_samples[];
   DALM0002Audit audit;
   DAL_M0002CollectBranchSamples(events, events_count, bars, bars_count, min_entry_time, h2_config, all_samples, reversal_samples, continuation_samples, audit);
   DAL_M0004SortSamplesByOutcome(all_samples);

   int labels[];
   int sessions[];
   int trend_regimes[];
   int revisit_ids[];
   double prevols[];
   datetime times[];
   DAL_M0004BuildLabelArrays(all_samples, labels, sessions, trend_regimes, revisit_ids, prevols, times);

   int count = ArraySize(labels);
   int prevol_regimes[];
   double prevol_t1 = 0.0, prevol_t2 = 0.0;
   DAL_M0004BuildPrevolRegimes(prevols, count, prevol_regimes, prevol_t1, prevol_t2);

   int revisit_buckets[];
   DAL_M0004BuildRevisitBuckets(revisit_ids, count, revisit_buckets);

   int spacing_regimes[];
   double spacing_t1 = 0.0, spacing_t2 = 0.0;
   DAL_M0004BuildSpacingRegimes(all_samples, count, spacing_regimes, spacing_t1, spacing_t2);

   int composite_strata[];
   DAL_M0004BuildCompositeStrata(sessions, trend_regimes, prevol_regimes, revisit_buckets, count, composite_strata);

   DALM0004TransitionStats trans;
   DAL_M0004ComputeTransitionStats(labels, count, trans);

   DALM0004RunStats rev_run;
   DALM0004RunStats cont_run;
   DAL_M0004ComputeRunStats(labels, count, DAL_M0004_LABEL_REVERSAL, rev_run);
   DAL_M0004ComputeRunStats(labels, count, DAL_M0004_LABEL_CONTINUATION, cont_run);

   int all_run_count = 0, all_max_run = 0;
   double all_avg_run = 0.0;
   DAL_M0004ComputeAllRunStats(labels, count, all_run_count, all_max_run, all_avg_run);

   Print(DAL_M0004Prefix("DAL_M0004_FINAL_AUDIT", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0002AuditText(audit, h2_config), "*branchSequenceOrder=outcome_index_chronological*postOutcomeModeForbidden=1");
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_SUMMARY", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SummaryText(trans, rev_run, cont_run));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_TRANSITION", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004TransitionText(trans));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_RUNS", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004RunStatsText(rev_run, cont_run, all_run_count, all_max_run, all_avg_run));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_TRANSITION_PERM_STRESS", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004TransitionPermutationStressText(labels, count, h4_config.stress_iterations));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_RUN_SHUFFLE_STRESS", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004RunShuffleStressText(labels, count, h4_config.stress_iterations));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_BLOCK_CONCENTRATION_STRESS", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004BlockConcentrationStressText(labels, count, h4_config.block_size, h4_config.stress_iterations));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_BLOCK_PROFILE_FAST", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004BlockRegimeProfileText(labels, count, h4_config.regime_block_size_fast));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_BLOCK_PROFILE_MAIN", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004BlockRegimeProfileText(labels, count, h4_config.block_size));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_BLOCK_PROFILE_SLOW", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004BlockRegimeProfileText(labels, count, h4_config.regime_block_size_slow));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_FAR_LAG_PLACEBO", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004FarLagText(labels, count, h4_config.placebo_lag_events));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_LAG_DECAY", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004LagDecayText(labels, count, h4_config.placebo_lag_events));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_RUN_LENGTH_TRANSITION", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004RunLengthTransitionText(labels, count));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_STRATIFIED_PERM_SESSION", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004StratifiedPermutationStressText("session", labels, sessions, count, h4_config.stress_iterations));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_STRATIFIED_PERM_PREVOL", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004StratifiedPermutationStressText("prevol_tercile", labels, prevol_regimes, count, h4_config.stress_iterations));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_STRATIFIED_PERM_REVISIT", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004StratifiedPermutationStressText("revisit_bucket", labels, revisit_buckets, count, h4_config.stress_iterations));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_STRATIFIED_PERM_COMPOSITE", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004StratifiedPermutationStressText("session_prevol_trend_revisit", labels, composite_strata, count, h4_config.stress_iterations));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CIRCULAR_SHIFT_STRESS", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004CircularShiftStressText(labels, count, h4_config.stress_iterations, h4_config.circular_min_shift_events));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_BLOCK_ORDER_SHUFFLE_STRESS", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004BlockOrderShuffleStressText(labels, count, h4_config.local_block_shuffle_size, h4_config.stress_iterations));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_SESSION_REGIME", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SegmentTransitionText("SESSION_BRANCH_INERTIA", labels, sessions, count, 0, 1, 2, 3));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_TREND_REGIME", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SegmentTransitionText("TREND_BRANCH_INERTIA", labels, trend_regimes, count, 0, 1, 2, 3));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_PREVOL_REGIME", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004PrevolSegmentText(labels, prevols, count));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_SESSION_DETAIL_0", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SingleSegmentDetailText("SESSION_DETAIL", "seg0", labels, sessions, count, 0));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_SESSION_DETAIL_1", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SingleSegmentDetailText("SESSION_DETAIL", "seg1", labels, sessions, count, 1));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_SESSION_DETAIL_2", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SingleSegmentDetailText("SESSION_DETAIL", "seg2", labels, sessions, count, 2));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_SESSION_DETAIL_3", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SingleSegmentDetailText("SESSION_DETAIL", "seg3", labels, sessions, count, 3));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_PREVOL_DETAIL_0", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SingleSegmentDetailText("PREVOL_DETAIL", "low", labels, prevol_regimes, count, 0));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_PREVOL_DETAIL_1", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SingleSegmentDetailText("PREVOL_DETAIL", "mid", labels, prevol_regimes, count, 1));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_PREVOL_DETAIL_2", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SingleSegmentDetailText("PREVOL_DETAIL", "high", labels, prevol_regimes, count, 2));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_REVISIT_DETAIL_0", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SingleSegmentDetailText("REVISIT_DETAIL", "first", labels, revisit_buckets, count, 0));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_REVISIT_DETAIL_1", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SingleSegmentDetailText("REVISIT_DETAIL", "revisit1", labels, revisit_buckets, count, 1));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_REVISIT_DETAIL_2", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SingleSegmentDetailText("REVISIT_DETAIL", "revisit2", labels, revisit_buckets, count, 2));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_REVISIT_DETAIL_3PLUS", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SingleSegmentDetailText("REVISIT_DETAIL", "revisit3plus", labels, revisit_buckets, count, 3));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_SPACING_DETAIL_FAST", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SingleSegmentDetailText("SPACING_DETAIL", "fast", labels, spacing_regimes, count, 0) + "*gapT1=" + DAL_M0001Fmt4(spacing_t1) + "*gapT2=" + DAL_M0001Fmt4(spacing_t2));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_SPACING_DETAIL_MID", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SingleSegmentDetailText("SPACING_DETAIL", "mid", labels, spacing_regimes, count, 1) + "*gapT1=" + DAL_M0001Fmt4(spacing_t1) + "*gapT2=" + DAL_M0001Fmt4(spacing_t2));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_SPACING_DETAIL_SLOW", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SingleSegmentDetailText("SPACING_DETAIL", "slow", labels, spacing_regimes, count, 2) + "*gapT1=" + DAL_M0001Fmt4(spacing_t1) + "*gapT2=" + DAL_M0001Fmt4(spacing_t2));

   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONTEXT_LAST_ONLY_REFERENCE", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004TransitionText(trans));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONTEXT_ROLLING_FAST", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004ContextStatsText("CONTEXT_STATE", "rolling", labels, count, h4_config.context_k_fast, h4_config.context_ewma_alpha, h4_config.context_strong_threshold, false));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONTEXT_ROLLING_MAIN", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004ContextStatsText("CONTEXT_STATE", "rolling", labels, count, h4_config.context_k_main, h4_config.context_ewma_alpha, h4_config.context_strong_threshold, false));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONTEXT_ROLLING_SLOW", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004ContextStatsText("CONTEXT_STATE", "rolling", labels, count, h4_config.context_k_slow, h4_config.context_ewma_alpha, h4_config.context_strong_threshold, false));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONTEXT_EWMA_MAIN", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004ContextStatsText("CONTEXT_STATE", "ewma_human_eye", labels, count, h4_config.context_k_main, h4_config.context_ewma_alpha, h4_config.context_strong_threshold, true));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONTEXT_BUCKETS_ROLLING_MAIN", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004ContextBucketText("CONTEXT_BUCKETS", "rolling", labels, count, h4_config.context_k_main, h4_config.context_ewma_alpha, false));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONTEXT_BUCKETS_EWMA_MAIN", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004ContextBucketText("CONTEXT_BUCKETS", "ewma_human_eye", labels, count, h4_config.context_k_main, h4_config.context_ewma_alpha, true));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONSENSUS_ROLLING_MAIN", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004ConsensusStatsText("CONSENSUS_CONTEXT", "rolling", all_samples, labels, count, h4_config.context_k_main, h4_config.context_ewma_alpha, h4_config.context_strong_threshold, false));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONSENSUS_EWMA_MAIN", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004ConsensusStatsText("CONSENSUS_CONTEXT", "ewma_human_eye", all_samples, labels, count, h4_config.context_k_main, h4_config.context_ewma_alpha, h4_config.context_strong_threshold, true));
   int last_signals[];
   int consensus_roll_signals[], rejected_roll_signals[], conflict_last_roll_signals[], conflict_context_roll_signals[], neutral_last_roll_signals[];
   int consensus_ewma_signals[], rejected_ewma_signals[], conflict_last_ewma_signals[], conflict_context_ewma_signals[], neutral_last_ewma_signals[];
   DAL_M0004BuildLastOnlySignals(labels, count, last_signals);
   DAL_M0004BuildConsensusSignalPartitions(labels, count, h4_config.context_k_main, h4_config.context_ewma_alpha, h4_config.context_strong_threshold, false, consensus_roll_signals, rejected_roll_signals, conflict_last_roll_signals, conflict_context_roll_signals, neutral_last_roll_signals);
   DAL_M0004BuildConsensusSignalPartitions(labels, count, h4_config.context_k_main, h4_config.context_ewma_alpha, h4_config.context_strong_threshold, true, consensus_ewma_signals, rejected_ewma_signals, conflict_last_ewma_signals, conflict_context_ewma_signals, neutral_last_ewma_signals);

   DALM0004SignalQualityStats q_last;
   DALM0004SignalQualityStats q_cons_roll, q_rej_roll, q_conf_last_roll, q_conf_ctx_roll, q_neutral_roll;
   DALM0004SignalQualityStats q_cons_ewma, q_rej_ewma, q_conf_last_ewma, q_conf_ctx_ewma, q_neutral_ewma;
   DAL_M0004ComputeSignalQualityStats("last_only", all_samples, labels, last_signals, count, q_last);
   DAL_M0004ComputeSignalQualityStats("consensus_accept", all_samples, labels, consensus_roll_signals, count, q_cons_roll);
   DAL_M0004ComputeSignalQualityStats("rejected_last", all_samples, labels, rejected_roll_signals, count, q_rej_roll);
   DAL_M0004ComputeSignalQualityStats("conflict_last", all_samples, labels, conflict_last_roll_signals, count, q_conf_last_roll);
   DAL_M0004ComputeSignalQualityStats("conflict_context", all_samples, labels, conflict_context_roll_signals, count, q_conf_ctx_roll);
   DAL_M0004ComputeSignalQualityStats("neutral_last", all_samples, labels, neutral_last_roll_signals, count, q_neutral_roll);
   DAL_M0004ComputeSignalQualityStats("consensus_accept", all_samples, labels, consensus_ewma_signals, count, q_cons_ewma);
   DAL_M0004ComputeSignalQualityStats("rejected_last", all_samples, labels, rejected_ewma_signals, count, q_rej_ewma);
   DAL_M0004ComputeSignalQualityStats("conflict_last", all_samples, labels, conflict_last_ewma_signals, count, q_conf_last_ewma);
   DAL_M0004ComputeSignalQualityStats("conflict_context", all_samples, labels, conflict_context_ewma_signals, count, q_conf_ctx_ewma);
   DAL_M0004ComputeSignalQualityStats("neutral_last", all_samples, labels, neutral_last_ewma_signals, count, q_neutral_ewma);

   Print(DAL_M0004Prefix("DAL_M0004_FINAL_LAST_ONLY_QUALITY_COUNTS", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SignalQualityCountsText("SIGNAL_QUALITY_COUNTS", "last_only", q_last));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_LAST_ONLY_QUALITY_FOLLOW", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SignalQualityFollowText("SIGNAL_QUALITY_FOLLOW", "last_only", q_last));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_LAST_ONLY_QUALITY_INTENSITY", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SignalQualityIntensityText("SIGNAL_QUALITY_INTENSITY", "last_only", q_last));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_LAST_ONLY_QUALITY_BRANCH", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SignalQualityBranchIntensityText("SIGNAL_QUALITY_BRANCH", "last_only", q_last));

   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONSENSUS_QUALITY_ROLLING_COUNTS", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SignalQualityCountsText("SIGNAL_QUALITY_COUNTS", "rolling_consensus", q_cons_roll));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONSENSUS_QUALITY_ROLLING_FOLLOW", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SignalQualityFollowText("SIGNAL_QUALITY_FOLLOW", "rolling_consensus", q_cons_roll));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONSENSUS_QUALITY_ROLLING_INTENSITY", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SignalQualityIntensityText("SIGNAL_QUALITY_INTENSITY", "rolling_consensus", q_cons_roll));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONSENSUS_QUALITY_ROLLING_BRANCH", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SignalQualityBranchIntensityText("SIGNAL_QUALITY_BRANCH", "rolling_consensus", q_cons_roll));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_REJECTED_LAST_QUALITY_ROLLING_FOLLOW", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SignalQualityFollowText("SIGNAL_QUALITY_FOLLOW", "rolling_rejected_last", q_rej_roll));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONFLICT_LAST_QUALITY_ROLLING_FOLLOW", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SignalQualityFollowText("SIGNAL_QUALITY_FOLLOW", "rolling_conflict_last", q_conf_last_roll));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONFLICT_CONTEXT_QUALITY_ROLLING_FOLLOW", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SignalQualityFollowText("SIGNAL_QUALITY_FOLLOW", "rolling_conflict_context", q_conf_ctx_roll));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_NEUTRAL_LAST_QUALITY_ROLLING_FOLLOW", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SignalQualityFollowText("SIGNAL_QUALITY_FOLLOW", "rolling_neutral_last", q_neutral_roll));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONSENSUS_QUALITY_COMPARE_ROLLING", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SignalQualityCompareText("SIGNAL_QUALITY_COMPARE", "rolling_consensus", q_last, q_cons_roll, q_rej_roll, q_conf_last_roll, q_neutral_roll));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONSENSUS_BLOCK_QUALITY_ROLLING", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SignalQualityBlockProfileText("SIGNAL_QUALITY_BLOCK_PROFILE", "rolling_consensus", labels, consensus_roll_signals, count, h4_config.block_size));

   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONSENSUS_QUALITY_EWMA_COUNTS", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SignalQualityCountsText("SIGNAL_QUALITY_COUNTS", "ewma_consensus", q_cons_ewma));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONSENSUS_QUALITY_EWMA_FOLLOW", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SignalQualityFollowText("SIGNAL_QUALITY_FOLLOW", "ewma_consensus", q_cons_ewma));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONSENSUS_QUALITY_EWMA_INTENSITY", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SignalQualityIntensityText("SIGNAL_QUALITY_INTENSITY", "ewma_consensus", q_cons_ewma));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONSENSUS_QUALITY_EWMA_BRANCH", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SignalQualityBranchIntensityText("SIGNAL_QUALITY_BRANCH", "ewma_consensus", q_cons_ewma));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_REJECTED_LAST_QUALITY_EWMA_FOLLOW", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SignalQualityFollowText("SIGNAL_QUALITY_FOLLOW", "ewma_rejected_last", q_rej_ewma));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONFLICT_LAST_QUALITY_EWMA_FOLLOW", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SignalQualityFollowText("SIGNAL_QUALITY_FOLLOW", "ewma_conflict_last", q_conf_last_ewma));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONFLICT_CONTEXT_QUALITY_EWMA_FOLLOW", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SignalQualityFollowText("SIGNAL_QUALITY_FOLLOW", "ewma_conflict_context", q_conf_ctx_ewma));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_NEUTRAL_LAST_QUALITY_EWMA_FOLLOW", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SignalQualityFollowText("SIGNAL_QUALITY_FOLLOW", "ewma_neutral_last", q_neutral_ewma));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONSENSUS_QUALITY_COMPARE_EWMA", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SignalQualityCompareText("SIGNAL_QUALITY_COMPARE", "ewma_consensus", q_last, q_cons_ewma, q_rej_ewma, q_conf_last_ewma, q_neutral_ewma));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONSENSUS_BLOCK_QUALITY_EWMA", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SignalQualityBlockProfileText("SIGNAL_QUALITY_BLOCK_PROFILE", "ewma_consensus", labels, consensus_ewma_signals, count, h4_config.block_size));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONSENSUS_SHUFFLE_STRESS_ROLLING", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004ConsensusShuffleStressText("rolling_last_context_consensus", all_samples, labels, composite_strata, count, h4_config.context_k_main, h4_config.context_ewma_alpha, h4_config.context_strong_threshold, false, h4_config.stress_iterations, false));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONSENSUS_STRATIFIED_STRESS_ROLLING", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004ConsensusShuffleStressText("rolling_last_context_consensus", all_samples, labels, composite_strata, count, h4_config.context_k_main, h4_config.context_ewma_alpha, h4_config.context_strong_threshold, false, h4_config.stress_iterations, true));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONSENSUS_SHUFFLE_STRESS_EWMA", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004ConsensusShuffleStressText("ewma_last_context_consensus", all_samples, labels, composite_strata, count, h4_config.context_k_main, h4_config.context_ewma_alpha, h4_config.context_strong_threshold, true, h4_config.stress_iterations, false));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONSENSUS_STRATIFIED_STRESS_EWMA", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004ConsensusShuffleStressText("ewma_last_context_consensus", all_samples, labels, composite_strata, count, h4_config.context_k_main, h4_config.context_ewma_alpha, h4_config.context_strong_threshold, true, h4_config.stress_iterations, true));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONTEXT_SHUFFLE_STRESS_ROLLING", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004ContextShuffleStressText("rolling_context", labels, composite_strata, count, h4_config.context_k_main, h4_config.context_ewma_alpha, h4_config.context_strong_threshold, false, h4_config.stress_iterations, false));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONTEXT_STRATIFIED_STRESS_ROLLING", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004ContextShuffleStressText("rolling_context", labels, composite_strata, count, h4_config.context_k_main, h4_config.context_ewma_alpha, h4_config.context_strong_threshold, false, h4_config.stress_iterations, true));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONTEXT_SHUFFLE_STRESS_EWMA", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004ContextShuffleStressText("ewma_human_eye_context", labels, composite_strata, count, h4_config.context_k_main, h4_config.context_ewma_alpha, h4_config.context_strong_threshold, true, h4_config.stress_iterations, false));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_CONTEXT_STRATIFIED_STRESS_EWMA", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004ContextShuffleStressText("ewma_human_eye_context", labels, composite_strata, count, h4_config.context_k_main, h4_config.context_ewma_alpha, h4_config.context_strong_threshold, true, h4_config.stress_iterations, true));
}

#endif
