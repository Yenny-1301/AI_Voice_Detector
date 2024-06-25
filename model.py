# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
# from sklearn.model_selection import GridSearchCV
# from sklearn.tree import plot_tree
# import pickle
# from sklearn.model_selection import train_test_split
# import pandas as pd

# col_names = ['File_Name','Amplitude', 'ZCR', 'RMSE', 'SC', 'SB', 'Real', 'MFCC1', 'MFCC2', 'MFCC3', 'MFCC4', 'MFCC5', 'MFCC6', 'MFCC7', 'MFCC8', 'MFCC9', 'MFCC10', 'MFCC11', 'MFCC12', 'MFCC13']
# audio_data = pd.read_csv("clean_audio_extract.csv")

# X = audio_data.drop(columns=['Real', 'File_Name', 'type'])  # Elimina las columnas no necesarias
# y = audio_data['Real']

# X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
# X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# param_grid = {
#     'criterion': ['gini', 'entropy'],
#     'n_estimators': [4, 6 , 8],
#     'max_depth': [None,5, 10, 20],
#     'min_samples_split': [2, 5, 10],
#     'min_samples_leaf': [1, 2, 4]
# }

# # Crea el modelo de Random Forest
# rf_model = RandomForestClassifier(random_state=42, class_weight='balanced')
# grid_search = GridSearchCV(rf_model, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
# grid_search.fit(X_train, y_train)

# best_rf_model = grid_search.best_estimator_
# best_rf_model.fit(X_train, y_train)

# val_accuracy = best_rf_model.score(X_val, y_val)
# print("Precisión en la validación: {:.2f}".format(val_accuracy))

# test_accuracy = best_rf_model.score(X_test, y_test)
# print("Precision con el conjunto de prueba: {:.2f}".format(test_accuracy))

# # Predicciones en el conjunto de validación
# y_val_pred = best_rf_model.predict(X_val)
# # Evaluación de las predicciones en el conjunto de validación
# print("Accuracy Score (Validation Set):", accuracy_score(y_val, y_val_pred))
# print("Classification Report (Validation Set):")
# print(classification_report(y_val, y_val_pred))

# # Evaluación del rendimiento del mejor modelo en el conjunto de prueba
# test_accuracy = best_rf_model.score(X_test, y_test)
# print("Accuracy on test set with best parameters: {:.2f}".format(test_accuracy))

# # # Guardar el modelo entrenado
# with open('modelo_entrenado_rf.pkl', 'wb') as f:
#     pickle.dump(best_rf_model, f)


# model_path = 'modelo_entrenado_rf.pkl'
# try:
#     with open(model_path, 'rb') as f:
#         modelo = pickle.load(f)
#         print(f"Loaded model type: {type(modelo)}")
# except Exception as e:
#     print(f"Error loading model: {e}")

