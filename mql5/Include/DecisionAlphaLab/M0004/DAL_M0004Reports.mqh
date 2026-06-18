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
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_FAR_LAG_PLACEBO", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004FarLagText(labels, count, h4_config.placebo_lag_events));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_SESSION_REGIME", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SegmentTransitionText("SESSION_BRANCH_INERTIA", labels, sessions, count, 0, 1, 2, 3));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_TREND_REGIME", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004SegmentTransitionText("TREND_BRANCH_INERTIA", labels, trend_regimes, count, 0, 1, 2, 3));
   Print(DAL_M0004Prefix("DAL_M0004_FINAL_PREVOL_REGIME", symbol, timeframe, source_mode, events_count, min_entry_time), DAL_M0004PrevolSegmentText(labels, prevols, count));
}

#endif
