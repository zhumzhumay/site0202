import joblib
import numpy as np

X_test =([0,0,0,0,0,0], [9.8, 66.64, 45, 200, 1, 21.31])
X_test = np.array(X_test)
best_model = joblib.load("model.pkl")
predicted = best_model.predict(X_test)
print(predicted[1])

