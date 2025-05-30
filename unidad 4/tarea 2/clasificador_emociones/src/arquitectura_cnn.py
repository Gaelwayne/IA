import tensorflow as tf

class ClasificadorEmociones:
    @staticmethod
    def construir_modelo(forma_entrada=(48, 48, 1)):
        """
        Crea un modelo CNN para clasificación de emociones
        """
        entradas = tf.keras.Input(shape=forma_entrada)
        
        # Bloque 1
        x = tf.keras.layers.Conv2D(64, (3, 3), padding='same', activation='relu')(entradas)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Conv2D(64, (3, 3), padding='same', activation='relu')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(x)
        x = tf.keras.layers.Dropout(0.25)(x)
        
        # Bloque 2
        x = tf.keras.layers.Conv2D(128, (3, 3), padding='same', activation='relu')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Conv2D(128, (3, 3), padding='same', activation='relu')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(x)
        x = tf.keras.layers.Dropout(0.25)(x)
        
        # Bloque 3
        x = tf.keras.layers.Conv2D(256, (3, 3), padding='same', activation='relu')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Conv2D(256, (3, 3), padding='same', activation='relu')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2))(x)
        x = tf.keras.layers.Dropout(0.25)(x)
        
        # Capas densas
        x = tf.keras.layers.Flatten()(x)
        x = tf.keras.layers.Dense(1024, activation='relu')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Dropout(0.5)(x)
        
        x = tf.keras.layers.Dense(512, activation='relu')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Dropout(0.5)(x)
        
        # Capa de salida para 7 emociones
        salidas = tf.keras.layers.Dense(7, activation='softmax')(x)
        
        # Crear modelo
        modelo = tf.keras.Model(inputs=entradas, outputs=salidas)
        
        # Compilar con métricas adicionales
        modelo.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=[
                'accuracy',
                tf.keras.metrics.Precision(name='precision'),
                tf.keras.metrics.Recall(name='recall'),
                tf.keras.metrics.AUC(name='auc')
            ]
        )
        
        return modelo

if __name__ == "__main__":
    modelo = ClasificadorEmociones.construir_modelo()
    modelo.summary()