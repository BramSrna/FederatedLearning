# https://scikit-learn.org/0.15/modules/generated/sklearn.linear_model.SGDRegressor.html#sklearn.linear_model.SGDRegressor.partial_fit
# https://scikit-learn.org/0.15/modules/scaling_strategies.html

import numpy as np
from sklearn import linear_model

n_samples, n_features = 10, 5

np.random.seed(0)

y = np.random.randn(n_samples)
X = np.random.randn(n_samples, n_features)
clf = linear_model.SGDRegressor()
model = clf.fit(X, y)
print(model)

y = np.random.randn(n_samples)
X = np.random.randn(n_samples, n_features)

print(model.score(X, y))

updated_model = model.partial_fit(X, y)

print(updated_model)
print(updated_model.score(X, y))