# """
# Memory Optimization Module.
# Reduces DataFrame memory footprint and processes large files in chunks.
# """

import pandas as pd
import numpy as np

def optimize_memory(df):
    """
    Reduces the memory usage of a DataFrame by downcasting numeric types.
    Includes exception handling to skip problematic columns safely.
    """
    try:
        original_mem = df.memory_usage(deep=True).sum() / 1024**2
        print(f"💾 Original memory usage: {original_mem:.2f} MB")
        
        df_opt = df.copy()
        
        for col in df_opt.select_dtypes(include=['int', 'float']).columns:
            try:
                orig_type = df_opt[col].dtype
                c_min = df_opt[col].min()
                c_max = df_opt[col].max()
                
                # Conversión de enteros
                if str(orig_type).startswith('int'):
                    if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                        df_opt[col] = df_opt[col].astype(np.int8)
                    elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                        df_opt[col] = df_opt[col].astype(np.int16)
                    elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                        df_opt[col] = df_opt[col].astype(np.int32)
                        
                # Conversión de decimales
                elif str(orig_type).startswith('float'):
                    if c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                        df_opt[col] = df_opt[col].astype(np.float32)
                        
            except BaseException as e:
                # Si una columna falla, advertimos pero el ciclo for continúa
                print(f"⚠️ WARNING: Could not optimize column '{col}': {e}")
                continue

        final_mem = df_opt.memory_usage(deep=True).sum() / 1024**2
        savings = 100 * (original_mem - final_mem) / original_mem
        
        print(f"🚀 Optimized memory usage: {final_mem:.2f} MB")
        print(f"📉 Total savings: {savings:.1f}%")
        return df_opt
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR in memory optimization: {e}")
        # En caso de fallo total, devolvemos el dataframe original intacto
        return df
