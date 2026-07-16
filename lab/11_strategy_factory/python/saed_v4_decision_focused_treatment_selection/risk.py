from __future__ import annotations
from .numerics import lcb,ucb,cvar_lower,std,mean

def compute_risk_adjusted_scores(outcome,utility,risk):
    draws=list(map(float,outcome['utility_draws']))
    mu=mean(draws) if draws else utility['expected_utility'];sigma=std(draws)
    lower=lcb(mu,sigma,risk.confidence_z);upper=ucb(mu,sigma,risk.confidence_z)
    cvar=cvar_lower(draws,risk.cvar_alpha) if draws else lower
    ambiguity=max(0.0,risk.ambiguity_radius*(abs(mu)+sigma+1.0))
    robust=lower-risk.uncertainty_weight*sigma-risk.tail_weight*max(0.0,-cvar)-ambiguity
    return {'mean_utility':mu,'utility_std':sigma,'lower_confidence_utility':lower,'upper_confidence_utility':upper,'cvar_utility':cvar,'ambiguity_penalty':ambiguity,'robust_utility':robust}

def constraint_risk_failures(stats,constraints):
    r=[]
    if stats['tail_loss_probability']>constraints.maximum_tail_loss_probability:r.append('tail_loss_probability')
    if stats['max_drawdown']>constraints.maximum_drawdown:r.append('maximum_drawdown')
    return r
