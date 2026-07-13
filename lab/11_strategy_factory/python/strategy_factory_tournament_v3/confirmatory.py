from __future__ import annotations
from .contracts import TournamentReport
from .enums import TrialStatus

def confirmatory_findings(report:TournamentReport,max_failure_rate:float=0.05)->tuple[str,...]:
 findings=list(report.critical_findings)
 if report.declared_trial_count==0:return ('empty_universe',)
 failure_rate=report.failed_trial_count/max(1,report.executed_trial_count)
 if failure_rate>max_failure_rate:findings.append('excessive_trial_failure_rate')
 succeeded=[r for r in report.trial_results if r.status is TrialStatus.SUCCEEDED]
 if not succeeded:findings.append('no_successful_trials')
 if len(report.candidate_ids)==0:findings.append('no_bounded_challengers')
 if report.reference_only:findings.append('reference_fixture_not_confirmatory_real_data')
 return tuple(dict.fromkeys(findings))

def bounded_challengers(report:TournamentReport,limit:int)->tuple[str,...]:return report.candidate_ids[:max(0,limit)]
