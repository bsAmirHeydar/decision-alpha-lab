# Kernel, Neighborhood, and Probabilistic Models

Linear and RBF SVM adapters provide margin and nonlinear kernel references. k-nearest-neighbor and nearest-centroid models expose local geometry assumptions. These families require scaling and explicit compute gates because inference cost and distance concentration can become unacceptable with large row counts or dimensions.

Gaussian, Bernoulli, and Multinomial Naive Bayes provide probabilistic references under different support assumptions. Multinomial NB requires nonnegative features and must reject incompatible schemas rather than silently transform them.

Probability-producing estimators are calibrated on calibration rows only or explicitly marked uncalibrated. A value in the interval [0,1] is not automatically a calibrated probability.
