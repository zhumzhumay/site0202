import joblib
X_test = [300, 100, 30, 67]

best_model = joblib.load("D:/diplom/site02.8.02.20/app/model.pkl", mmap_mode=None)
predicted = best_model.predict(X_test)
print(predicted)