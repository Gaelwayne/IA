# 1 - INSTALACION DE LAS LIBRERIAS NECESARIAS
# pip install numpy pandas scikit-learn



# 2 - IMPORTACION DE LIBRERIAS NECESARIAS
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics import accuracy_score, recall_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB



# 3 - CARGA Y PREPROCESAMIENTO DE LOS DATOS
# Cargamos los datos
data = pd.read_csv('spam_assassin.csv')
registros_iniciales = len(data)
print()
print('=' * 90)
print('Registros iniciales: ', registros_iniciales)

# Eliminacion de correos duplicados
data = data.drop_duplicates()
registros_unicos = len(data)
print('Registros sin duplicados: ', registros_unicos)
print("Registros eliminados: ", registros_iniciales - registros_unicos)

print('=' * 90)

# Imprimir el total de regostros que tienen 1 en la columna target
cantidad_spam = data['target'].sum()
print('Correos SPAM: ', cantidad_spam)
# Imprimir el total de regostros que tienen 0 en la columna target
cantidad_no_spam = len(data) - cantidad_spam
print('Correos NO SPAM: ', cantidad_no_spam)

print('=' * 90)

# PREPROCESAMIENTO DE LOS DATOS
# Convertir todo a minusculas
data['text'] = data['text'].str.lower()

# Eliminar caracteres especiales para mantener solo letras y numeros
data['text'] = data['text'].str.replace('[^a-zA-Z0-9 ]', '')
data['text'] = data['text'].str.split()

# Tokenizar y eliminar stopwords
stopwords = list(ENGLISH_STOP_WORDS)
data['text'] = data['text'].apply(lambda x: ' '.join([word for word in x if word not in stopwords]))



# 4 - EXTRAER CARACTERISTICAS DE LOS DATOS (TF, IDF, TF-IDF)

# Frecuencia de término (TF): Número de veces que una palabra aparece en un documento.
count_vectorizer = CountVectorizer(stop_words = 'english')
X_tf = count_vectorizer.fit_transform(data['text'])
tf_matrix = X_tf.toarray()
palabras = count_vectorizer.get_feature_names_out()
print("Frecuencia de términos (TF):\n", pd.DataFrame(tf_matrix, columns=palabras))

print('=' * 90)

# Frecuencia de término inversa de documento (IDF): Mide la importancia de una palabra en un documento.
tfidf_transformer = TfidfTransformer(use_idf=True, norm=None, smooth_idf=True)
tfidf_transformer.fit(X_tf)
idf_values = tfidf_transformer.idf_
idf_dict = dict(zip(palabras, idf_values))
print("Frecuencia Inversa de Documentos (IDF):\n", pd.DataFrame(list(idf_dict.items()), columns=['Palabra', 'Valor IDF']))

print('=' * 90)

# TF-IDF: Multiplicación de TF y IDF para obtener la importancia de una palabra en un documento.
X_tfidf = tfidf_transformer.transform(X_tf).toarray()
print("TF-IDF Matrix:\n", pd.DataFrame(X_tfidf, columns=palabras))

print('=' * 90)

vectorizer = TfidfVectorizer(stop_words = 'english')
X = vectorizer.fit_transform(data['text'])
print('X: ', X.shape)

# Definir las etiquetas (spam o no spam)
y = data['target']

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
print('Datos de entrenamiento: ', X_train.shape)
print('Datos de prueba: ', X_test.shape)

print('=' * 90)



# 5 - ENTRENAMIENTO DEL MODELO
modelo_bayes = MultinomialNB()
modelo_bayes.fit(X_train, y_train)
y_pred = modelo_bayes.predict(X_test)



# CALCULO DE PROBABILIDADES
# Probabilidad de que sea spam
P_Spam = data['target'].sum() / len(data)
print('Probabilidad de que sea spam P(Spam): ', P_Spam, ' = ', round(P_Spam * 100, 2), '%')

# Probabilidad de que no sea spam
P_NoSpam = 1 - P_Spam
print("Probabilidad de que NO sea spam P(Spam)': ", P_NoSpam, ' = ', round(P_NoSpam * 100, 2), '%')

print('=' * 90)

# Calcular la probabilidad de las características del correo electrónico dado que es spam P(Características|Spam):
P_Caracteristicas_Spam = X[data['target'] == 1].sum(axis=0) / X[data['target'] == 1].sum()

df_Caracteristicas_Spam = pd.DataFrame(P_Caracteristicas_Spam.T, columns=['Probabilidad'])
df_Caracteristicas_Spam['Palabra'] = palabras
df_Caracteristicas_Spam = df_Caracteristicas_Spam[['Palabra', 'Probabilidad']]
print('Probabilidad de las características del correo electrónico dado que es spam P(Caracteristicas | Spam):\n', df_Caracteristicas_Spam)

print('=' * 90)

# Calcular la probabilidad de las características del correo electrónico dado que no es spam P(Características|NoSpam):
P_Caracteristicas_NoSpam = X[data['target'] == 0].sum(axis=0) / X[data['target'] == 0].sum()

df_Caracteristicas_NoSpam = pd.DataFrame(P_Caracteristicas_NoSpam.T, columns=['Probabilidad'])
df_Caracteristicas_NoSpam['Palabra'] = palabras
df_Caracteristicas_NoSpam = df_Caracteristicas_NoSpam[['Palabra', 'Probabilidad']]
print('Probabilidad de las características del correo electrónico dado que NO es spam P(Caracteristicas | NoSpam): ', df_Caracteristicas_NoSpam)

print('=' * 90)

# Calcular la probabilidad posterior de que el correo electrónico sea spam P(Spam|Caracteristicas):
P_Spam_Caracteristicas = (P_Spam * P_Caracteristicas_Spam) / (P_Spam * P_Caracteristicas_Spam + P_NoSpam * P_Caracteristicas_NoSpam)

df_Spam_Caracteristicas = pd.DataFrame(P_Spam_Caracteristicas.T, columns=['Probabilidad'])
df_Spam_Caracteristicas['Palabra'] = palabras
df_Spam_Caracteristicas = df_Spam_Caracteristicas[['Palabra', 'Probabilidad']]
print('Probabilidad posterior de que el correo electrónico sea spam P(Spam | Caracteristicas):\n', df_Spam_Caracteristicas)

print('=' * 90)

# Calculamos la probabilidad posterior de que el correo electrónico no sea spam P(NoSpam|Caracteristicas):
P_NoSpam_Caracteristicas = (P_NoSpam * P_Caracteristicas_NoSpam) / (P_Spam * P_Caracteristicas_Spam + P_NoSpam * P_Caracteristicas_NoSpam)
df_NoSpam_Caracteristicas = pd.DataFrame(P_NoSpam_Caracteristicas.T, columns=['Probabilidad'])
df_NoSpam_Caracteristicas['Palabra'] = palabras
df_NoSpam_Caracteristicas = df_NoSpam_Caracteristicas[['Palabra', 'Probabilidad']]
print('Probabilidad posterior de que el correo electrónico NO sea spam P(NoSpam | Caracteristicas):\n', df_NoSpam_Caracteristicas)

print('=' * 90)

# Clasificación:
# Un correo electrónico se clasificara como 'spam' si P(Spam|Caracteristicas) > P(NoSpam|Caracteristicas):
clasificaciones = np.where(P_Spam_Caracteristicas > P_NoSpam_Caracteristicas, "Spam", "No Spam")
print('Clasificaciones: ', clasificaciones)

print('=' * 90)



# 6 - EVALUACION DEL MODELO
# Evaluamos las predicciones del modelo de Naive Bayes estándar
precision = accuracy_score(y_test, y_pred)
recuperacion = recall_score(y_test, y_pred)
print('Precisión (Naive Bayes): ', precision, ' = ', round(precision * 100, 2), '%')
print('Recuperación (Naive Bayes): ', recuperacion, ' = ', round(recuperacion * 100, 2), '%')

print('=' * 90)

# print("Reporte de clasificación:\n", classification_report(y_test, y_pred))

# print('=' * 90)