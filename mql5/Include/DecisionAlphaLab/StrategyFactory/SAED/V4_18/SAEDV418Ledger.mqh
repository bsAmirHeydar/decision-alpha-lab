#pragma once
struct SAEDV418ExposureLedger { long rows; int treatments; int estimators; int policies; int folds; int protected_exposures; int hidden_queries; };
bool SAEDV418LedgerClosed(const SAEDV418ExposureLedger &x){ return x.protected_exposures==0 && x.hidden_queries==0; }
