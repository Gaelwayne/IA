# 1 - INSTALACION DE LAS LIBRERIAS NECESARIAS
# pip install numpy pandas scikit-learn

# 2 - IMPORTACION DE LIBRERIAS NECESARIAS
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics import accuracy_score, recall_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import time
import gc  # Para gestión de memoria

# Función para imprimir separadores consistentes
def print_separator():
    print('=' * 90)
    
# Función para mostrar el tiempo transcurrido
def tiempo_transcurrido(inicio):
    fin = time.time()
    print(f"Tiempo: {fin - inicio:.2f} segundos")

# 3 - CARGA Y PREPROCESAMIENTO DE LOS DATOS
inicio_total = time.time()

print("Iniciando carga de datos...")
inicio = time.time()
# Cargamos los datos
try:
    data = pd.read_csv('spam_assassin.csv')
    registros_iniciales = len(data)
    print()
    print_separator()
    print('Registros iniciales: ', registros_iniciales)
    tiempo_transcurrido(inicio)
except FileNotFoundError:
    print("Error: No se encontró el archivo 'spam_assassin.csv'")
    print("Asegúrate de que el archivo esté en el directorio correcto.")
    exit(1)

# Eliminacion de correos duplicados
print("\nEliminando duplicados...")
inicio = time.time()
data = data.drop_duplicates()
registros_unicos = len(data)
print('Registros sin duplicados: ', registros_unicos)
print("Registros eliminados: ", registros_iniciales - registros_unicos)
tiempo_transcurrido(inicio)

print_separator()

# Estadísticas de spam
cantidad_spam = data['target'].sum()
print('Correos SPAM: ', cantidad_spam)
cantidad_no_spam = len(data) - cantidad_spam
print('Correos NO SPAM: ', cantidad_no_spam)

print_separator()

# PREPROCESAMIENTO DE LOS DATOS
print("Preprocesando texto...")
inicio = time.time()

# Verificamos si las columnas necesarias existen
if 'text' not in data.columns or 'target' not in data.columns:
    print("Error: El dataset debe contener las columnas 'text' y 'target'")
    exit(1)

# Convertir a minúsculas (solo si la columna es de tipo string)
if data['text'].dtype == object:
    data['text'] = data['text'].str.lower()
    
    # Eliminamos filas con valores nulos
    data = data.dropna(subset=['text'])
    
    # Eliminar caracteres especiales - usando una operación más eficiente
    data['text'] = data['text'].str.replace('[^a-zA-Z0-9 ]', '', regex=True)
    
    # Tokenización y eliminación de stopwords - vectorizada
    stopwords = set(ENGLISH_STOP_WORDS)  # Usamos set para búsquedas más rápidas
    
    # Enfoque más eficiente para tokenizar y eliminar stopwords
    def limpiar_texto(texto):
        if isinstance(texto, str):
            palabras = texto.split()
            return ' '.join([palabra for palabra in palabras if palabra not in stopwords])
        return ""
    
    data['text'] = data['text'].apply(limpiar_texto)
else:
    print("Advertencia: La columna 'text' no es de tipo string. Revisa tus datos.")
    exit(1)

tiempo_transcurrido(inicio)
print_separator()

# 4 - EXTRAER CARACTERISTICAS DE LOS DATOS
print("Extrayendo características (vectorizando)...")
inicio = time.time()

# Reducimos el tamaño del conjunto de características para mayor eficiencia
max_features = 5000  # Limitamos las características para mejorar rendimiento

# Vectorización TF-IDF directa (más eficiente que calcular TF e IDF por separado)
vectorizer = TfidfVectorizer(stop_words='english', max_features=max_features)
X = vectorizer.fit_transform(data['text'])
palabras = vectorizer.get_feature_names_out()

print(f'Matriz X: {X.shape} (Se limitó a {max_features} características)')

# Obtener TF (para las visualizaciones)
print("Calculando TF...")
count_vectorizer = CountVectorizer(stop_words='english', max_features=max_features)
X_tf = count_vectorizer.fit_transform(data['text'])

# Solo mostramos una pequeña muestra de la matriz TF para evitar sobrecarga
muestra_size = min(5, X_tf.shape[0])
muestra_palabras = min(10, len(count_vectorizer.get_feature_names_out()))
tf_muestra = X_tf[:muestra_size, :muestra_palabras].toarray()
print(f"Muestra de Frecuencia de términos (TF) - primeras {muestra_size} filas, {muestra_palabras} columnas:")
palabras_muestra = count_vectorizer.get_feature_names_out()[:muestra_palabras]
print(pd.DataFrame(tf_muestra, columns=palabras_muestra))

print_separator()

# IDF (solo para visualización)
print("Calculando IDF...")
tfidf_transformer = TfidfTransformer(use_idf=True, norm=None, smooth_idf=True)
tfidf_transformer.fit(X_tf)
idf_values = tfidf_transformer.idf_
# Mostramos solo las primeras 10 palabras para evitar sobrecarga
idf_dict = dict(zip(palabras_muestra, idf_values[:muestra_palabras]))
print(f"Muestra de IDF (primeras {muestra_palabras} palabras):")
print(pd.DataFrame(list(idf_dict.items()), columns=['Palabra', 'Valor IDF']))

print_separator()

# TF-IDF (solo para visualización) - CORREGIDO
print("Calculando TF-IDF (muestra)...")
# Transformamos toda la matriz y luego tomamos una muestra para visualización
X_tfidf = tfidf_transformer.transform(X_tf)
tfidf_muestra = X_tfidf[:muestra_size, :muestra_palabras].toarray()
print(f"Muestra de matriz TF-IDF (primeras {muestra_size} filas, {muestra_palabras} columnas):")
print(pd.DataFrame(tfidf_muestra, columns=palabras_muestra))

print_separator()

# Liberamos memoria
del X_tf
del X_tfidf
del tfidf_transformer
gc.collect()

# Definir las etiquetas
y = data['target']

# Dividir los datos en entrenamiento y prueba
print("Dividiendo datos para entrenamiento y prueba...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print('Datos de entrenamiento:', X_train.shape)
print('Datos de prueba:', X_test.shape)
tiempo_transcurrido(inicio)

print_separator()

# 5 - ENTRENAMIENTO DEL MODELO
print("Entrenando modelo Naive Bayes...")
inicio = time.time()
modelo_bayes = MultinomialNB()
modelo_bayes.fit(X_train, y_train)
y_pred = modelo_bayes.predict(X_test)
tiempo_transcurrido(inicio)

print_separator()

# CALCULO DE PROBABILIDADES PRINCIPALES
P_Spam = data['target'].sum() / len(data)
print(f'Probabilidad de que sea spam P(Spam): {P_Spam:.4f} = {P_Spam * 100:.2f}%')

P_NoSpam = 1 - P_Spam
print(f"Probabilidad de que NO sea spam P(NoSpam): {P_NoSpam:.4f} = {P_NoSpam * 100:.2f}%")

print_separator()

# Cálculo de probabilidades para palabras importantes (muestra)
print("Calculando probabilidades para palabras importantes (muestra)...")
inicio = time.time()

try:
    # Obtenemos las características más discriminativas
    coef = modelo_bayes.feature_log_prob_
    
    # Limitamos a un número menor que max_features por si acaso
    num_features_to_show = min(10, max_features)
    
    top_spam_idx = np.argsort(coef[1])[-num_features_to_show:]  # Índices de las palabras más relacionadas con spam
    top_nospam_idx = np.argsort(coef[0])[-num_features_to_show:]  # Índices de las palabras más relacionadas con no-spam

    # Mostramos las palabras más relacionadas con spam
    print(f"Top {num_features_to_show} palabras relacionadas con SPAM:")
    top_spam_words = [palabras[i] for i in top_spam_idx]
    top_spam_probs = [np.exp(coef[1][i]) for i in top_spam_idx]
    spam_words_df = pd.DataFrame({'Palabra': top_spam_words, 'Probabilidad': top_spam_probs})
    print(spam_words_df)

    print(f"\nTop {num_features_to_show} palabras relacionadas con NO SPAM:")
    top_nospam_words = [palabras[i] for i in top_nospam_idx]
    top_nospam_probs = [np.exp(coef[0][i]) for i in top_nospam_idx]
    nospam_words_df = pd.DataFrame({'Palabra': top_nospam_words, 'Probabilidad': top_nospam_probs})
    print(nospam_words_df)
except Exception as e:
    print(f"No se pudieron calcular las probabilidades de palabras específicas: {e}")
    print("Continuando con la evaluación del modelo...")

tiempo_transcurrido(inicio)
print_separator()

# 6 - EVALUACION DEL MODELO
print("Evaluando modelo...")
inicio = time.time()
precision = accuracy_score(y_test, y_pred)
recuperacion = recall_score(y_test, y_pred)
print(f'Precisión (Naive Bayes): {precision:.4f} = {precision * 100:.2f}%')
print(f'Recuperación (Naive Bayes): {recuperacion:.4f} = {recuperacion * 100:.2f}%')

print_separator()
print("Reporte de clasificación completo:")
print(classification_report(y_test, y_pred))

# Tiempo total de ejecución
tiempo_total = time.time() - inicio_total
print(f"Tiempo total de ejecución: {tiempo_total:.2f} segundos")

print_separator()

# 7 - FUNCIONALIDAD PARA CLASIFICAR NUEVOS CORREOS
def clasificar_correo(texto, modelo, vectorizador):
    """
    Clasifica un nuevo correo electrónico como spam o no spam.
    
    Args:
        texto (str): El texto del correo a clasificar
        modelo: El modelo entrenado de Naive Bayes
        vectorizador: El vectorizador TF-IDF entrenado
        
    Returns:
        str: "Spam" o "No Spam"
        float: Probabilidad de que sea spam
    """
    # Preprocesar el texto igual que en el entrenamiento
    texto = texto.lower()
    texto = ''.join([c for c in texto if c.isalnum() or c.isspace()])
    palabras = texto.split()
    texto = ' '.join([palabra for palabra in palabras if palabra not in stopwords])
    
    # Vectorizar
    X_nuevo = vectorizador.transform([texto])
    
    # Predecir
    resultado = modelo.predict(X_nuevo)[0]
    probabilidad = modelo.predict_proba(X_nuevo)[0][1]  # Probabilidad de clase 1 (spam)
    
    return "Spam" if resultado == 1 else "No Spam", probabilidad

# Ejemplo de uso
print("\nEjemplo de clasificación de nuevo correo:")
ejemplo_texto = "Congratulations! You've won a free iPhone. Click here to claim your prize now!"
resultado, prob = clasificar_correo(ejemplo_texto, modelo_bayes, vectorizer)
print(f"Texto: {ejemplo_texto}")
print(f"Clasificación: {resultado}")
print(f"Probabilidad de spam: {prob:.2%}")

print_separator()
print("Modelo de clasificación de spam listo para usar. Puedes clasificar nuevos correos usando la función 'clasificar_correo'.")