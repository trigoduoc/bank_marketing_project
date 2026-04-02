"""
Memory Optimization Module.
Reduces DataFrame memory footprint and processes large files in chunks.
"""
import pandas as pd
import logging

# 1. Configuración del monitor de eventos (logs)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def optimize_memory_usage(df: pd.DataFrame) -> pd.DataFrame:
    """
    Optimizes Pandas DataFrame memory by downcasting numeric columns.
    """
    logging.info("Starting memory optimization (Downcasting)...")
    
    # Calculamos la memoria inicial consumida en Megabytes
    start_mem = df.memory_usage(deep=True).sum() / 1024**2
    logging.info(f"Initial memory usage: {start_mem:.2f} MB")
    
    # Hacemos una copia para no alterar el DataFrame original accidentalmente
    df_optimized = df.copy()
    
    # Identificamos columnas enteras y las comprimimos (ej. de int64 a int8)
    int_columns = df_optimized.select_dtypes(include=['int64', 'int32']).columns
    for col in int_columns:
        df_optimized[col] = pd.to_numeric(df_optimized[col], downcast='integer')
        
    # Identificamos columnas decimales y las comprimimos (ej. de float64 a float32)
    float_columns = df_optimized.select_dtypes(include=['float64']).columns
    for col in float_columns:
        df_optimized[col] = pd.to_numeric(df_optimized[col], downcast='float')
        
    # Calculamos la memoria final y el porcentaje de ahorro
    end_mem = df_optimized.memory_usage(deep=True).sum() / 1024**2
    logging.info(f"Optimized memory usage: {end_mem:.2f} MB")
    
    reduction = 100 * (start_mem - end_mem) / start_mem
    logging.info(f"Memory reduced by {reduction:.1f}%")
    
    return df_optimized

def process_large_file_in_chunks(file_path: str, chunk_size: int = 10000, sep: str = ',') -> int:
    """
    Processes a massive file in chunks to prevent RAM overflow.
    """
    logging.info(f"Starting chunk processing for {file_path} (Chunk size: {chunk_size})")
    
    total_rows = 0
    try:
        # Al usar 'chunksize', Pandas no carga todo a la RAM, crea un iterador por bloques
        chunk_iterator = pd.read_csv(file_path, sep=sep, chunksize=chunk_size)
        
        # Recorremos bloque por bloque
        for i, chunk in enumerate(chunk_iterator):
            rows_in_chunk = len(chunk)
            total_rows += rows_in_chunk
            logging.info(f"Processed chunk {i + 1}: {rows_in_chunk} rows.")
            
            # Aquí iría la lógica de transformación para cada bloque pequeño...
            
        logging.info(f"Finished processing. Total rows: {total_rows}")
        return total_rows
        
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return 0

if __name__ == "__main__":
    # Archivo de prueba
    test_file = "data/raw/bank-full.csv"
    
    # Prueba 1: Leer en bloques (simulación para archivos inmensos)
    process_large_file_in_chunks(test_file, chunk_size=15000, sep=';')
    
    # Prueba 2: Reducción de tipos de datos en memoria (Downcasting)
    try:
        df_test = pd.read_csv(test_file, sep=';')
        optimize_memory_usage(df_test)
    except FileNotFoundError:
        pass