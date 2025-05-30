import os
import numpy as np
import tensorflow as tf
from arquitectura_cnn import ClasificadorEmociones
from cargador_conjunto_datos import CargadorDatos

class EntrenadorModelo:
    def __init__(self, directorio_modelo='clasificador_emociones/modelos'):
        self.directorio_modelo = directorio_modelo
        os.makedirs(directorio_modelo, exist_ok=True)
        
    def entrenar(self, X_entrenamiento, y_entrenamiento, X_validacion, y_validacion, 
                 epocas=100, tamano_lote=64):
        """
        Entrena el modelo para clasificación de emociones
        """
        # Crear modelo
        modelo = ClasificadorEmociones.construir_modelo()
        
        # Callbacks de entrenamiento
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True,
                verbose=1
            ),
            tf.keras.callbacks.ModelCheckpoint(
                os.path.join(self.directorio_modelo, 'mejor_modelo_emociones.keras'),
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.2,
                patience=5,
                min_lr=1e-6,
                verbose=1
            ),
            tf.keras.callbacks.TensorBoard(
                log_dir='logs/entrenamiento_emociones',
                histogram_freq=1
            )
        ]
        
        # Aumento de datos
        aumento_datos = tf.keras.Sequential([
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(0.1),
            tf.keras.layers.RandomZoom(0.1),
            tf.keras.layers.RandomContrast(0.1),
        ])
        
        # Entrenar modelo
        historia = modelo.fit(
            tf.keras.preprocessing.image.ImageDataGenerator(
                preprocessing_function=aumento_datos
            ).flow(X_entrenamiento, y_entrenamiento, batch_size=tamano_lote),
            epochs=epocas,
            validation_data=(X_validacion, y_validacion),
            callbacks=callbacks,
            verbose=1
        )
        
        return modelo, historia
    
    def evaluar(self, modelo, X_validacion, y_validacion):
        """
        Evalúa el modelo e imprime métricas detalladas
        """
        resultados = modelo.evaluate(X_validacion, y_validacion, verbose=1)
        print("\nResultados de Validación:")
        for nombre, valor in zip(modelo.metrics_names, resultados):
            print(f"{nombre}: {valor:.4f}")
        
        # Guardar matriz de confusión
        y_pred = modelo.predict(X_validacion)
        y_pred_classes = np.argmax(y_pred, axis=1)
        y_true = np.argmax(y_validacion, axis=1)
        
        conf_matrix = tf.math.confusion_matrix(y_true, y_pred_classes)
        print("\nMatriz de Confusión:")
        print(conf_matrix.numpy())
        
if __name__ == "__main__":
    try:
        # Cargar conjunto de datos
        print("Cargando conjunto de datos...")
        cargador = CargadorDatos('clasificador_emociones/datos')
        X_entrenamiento, y_entrenamiento, X_validacion, y_validacion = cargador.cargar_conjunto_datos()
        
        # Entrenar modelo
        print("\nIniciando entrenamiento...")
        entrenador = EntrenadorModelo()
        modelo, historia = entrenador.entrenar(X_entrenamiento, y_entrenamiento, X_validacion, y_validacion)
        
        # Evaluar modelo
        print("\nEvaluando modelo...")
        entrenador.evaluar(modelo, X_validacion, y_validacion)
        
    except Exception as e:
        print(f"Error de entrenamiento: {str(e)}")