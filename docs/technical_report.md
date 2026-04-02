# Informe Técnico: Preparación de Datos - Bank Marketing 🏦

**Equipo:** [Nombres de los integrantes]  
**Asignatura:** SCY1101 - Programación para la Ciencia de Datos  
**Fecha:** [Fecha de entrega]  

---

## 1. Resumen Ejecutivo
Este proyecto tiene como objetivo procesar el dataset *Bank Marketing* para preparar los datos para un futuro modelo de Machine Learning. Se implementó un flujo de trabajo reproducible que incluye la verificación de integridad de los datos, optimización de memoria, tratamiento automatizado de valores nulos y atípicos, y la construcción de Pipelines de Scikit-Learn para su escalabilidad.

## 2. Análisis Exploratorio Inicial (EDA)
*(Insertar aquí tabla resumen del dataset: cantidad de filas, columnas y tipos de datos)*

Durante la inspección inicial, se identificaron los siguientes patrones clave:
* **Desbalance de clases:** La variable objetivo `y` (suscripción al depósito) presenta un fuerte desbalance. *(Insertar gráfico de barras de la variable objetivo)*.
* **Correlaciones Numéricas:** *(Insertar Matriz de Correlación)*. Se analizó la relación entre las variables numéricas para identificar posibles redundancias [Referencia: Análisis en Notebook 01].


## 3. Metodología de Transformación
Para asegurar la calidad de los datos sin perder información valiosa, se tomaron las siguientes decisiones técnicas, justificadas por las reglas del negocio:
* **Prevención de Fuga de Datos (Data Leakage):** Se eliminó la columna `duration`, ya que su valor solo se conoce una vez finalizada la llamada, lo cual invalidaría un modelo predictivo en la vida real.
* **Tratamiento de Valores Atípicos:** En lugar de eliminar clientes con saldos extremos (outliers en `balance`), se aplicó una técnica de *Winsorización (Capping)* para limitar los valores anómalos sin perder el registro del cliente. *(Insertar boxplot comparativo Antes/Después)*.
* **Imputación Inteligente:** * Columnas con alto porcentaje de nulos (ej. `poutcome`) fueron descartadas.
    * Columnas con nulos moderados fueron imputadas utilizando medidas de tendencia central u otras estrategias justificadas.

## 4. Resultados y Validación Técnica
El proceso fue validado mediante auditorías automáticas y técnicas de ingeniería de datos:
* **Integridad (Checksum):** El archivo original fue validado exitosamente generando su firma SHA-256 (`[Pegar el Hash obtenido aquí]`), confirmando la ausencia de corrupción de datos.
* **Optimización de Memoria:** Se implementó una técnica de *Downcasting* numérico, logrando reducir el peso del dataset en memoria en un `[Insertar porcentaje]%`.
* **Pipelines de Scikit-Learn:** Se consolidó una arquitectura de procesamiento robusta que garantiza la reproducibilidad en entornos de producción. *(Insertar captura del diagrama interactivo del Pipeline)*.

## 5. Conclusiones y Recomendaciones
* **Conclusiones:** El tratamiento de datos permitió rescatar la mayor cantidad de registros útiles, empaquetando la limpieza en un formato automatizado.
* **Lecciones Aprendidas:** El uso de herramientas de control de versiones (Git) y entornos virtuales (`.venv`) demostró ser fundamental para evitar conflictos de dependencias.
* **Mejoras Futuras:** Se recomienda explorar algoritmos más avanzados de imputación (ej. KNN Imputer) para variables categóricas complejas. 

