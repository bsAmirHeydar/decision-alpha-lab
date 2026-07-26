# Calibration and Probability Disclosure

Every probability output has one of three disclosures: calibrated, uncalibrated, or not applicable. Calibration fits only on dedicated calibration rows. Threshold selection fits only on threshold rows. Neither may access OOF holdout or final-test labels for selection.

The pack supports identity disclosure, Platt scaling, and isotonic calibration through the shared trainer lifecycle. Calibration state records model hash, row-ID hash, role, method, parameters, and evidence hash. Calibration quality is evaluated separately from discrimination and utility.

A model can rank well and calibrate poorly. Such a model may still order opportunities but cannot drive probability-proportional sizing until calibration passes.
