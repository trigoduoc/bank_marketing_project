import pandas as pd
from pathlib import Path
from src.audit import audit_data
from src.optimization import optimize_memory
from src.pipeline import build_preprocessing_pipeline

def main():
    """Main orchestration script for the Data Science project."""
    print("--- 🚀 Starting Data Pipeline ---\n")

    try:
        # 1. Auditoría
        if not audit_data():
            print("\n🛑 Pipeline stopped due to audit failure.")
            return

        # 2. Carga dinámica
        raw_dir = Path("data/raw")
        csv_file = list(raw_dir.glob("*.csv"))[0]
        
        print(f"\n📥 Loading raw data from {csv_file.name}...")
        df_raw = pd.read_csv(csv_file, sep=None, engine='python')

        # 3. Optimización
        print("\n⚙️ Optimizing memory...")
        df_opt = optimize_memory(df_raw)

        # 4. Pipeline
        print("\n🏗️ Building and applying preprocessing pipeline...")
        leakage_columns = ['duration'] if 'duration' in df_opt.columns else []
        pipeline = build_preprocessing_pipeline(df_opt, columns_to_drop=leakage_columns)
        
        processed_matrix = pipeline.fit_transform(df_opt)
        
        # 5. Guardado
        print("\n💾 Saving processed dataset...")
        feature_names = pipeline.named_steps['preprocessing'].get_feature_names_out()
        feature_names = [name.replace('num__', '').replace('cat__', '') for name in feature_names]
        
        df_processed = pd.DataFrame(processed_matrix, columns=feature_names)
        
        processed_dir = Path("data/processed")
        processed_dir.mkdir(parents=True, exist_ok=True)
        output_path = processed_dir / "processed_data.csv"
        
        df_processed.to_csv(output_path, index=False)
        print(f"✅ SUCCESS: Processed dataset saved at {output_path}")
        print(f"📊 Final dimensions: {df_processed.shape}")

    # Manejo de errores específicos de negocio
    except IndexError:
        print("\n❌ CRITICAL ERROR: No se encontró ningún archivo CSV en la carpeta 'data/raw'.")
    except FileNotFoundError as e:
        print(f"\n❌ CRITICAL ERROR: Archivo o directorio no encontrado: {e}")
    except pd.errors.EmptyDataError:
        print("\n❌ CRITICAL ERROR: El archivo CSV está completamente vacío.")
    except pd.errors.ParserError:
        print("\n❌ CRITICAL ERROR: Pandas no pudo leer el CSV. Revisa si hay comas o separadores rotos en los datos.")
    except Exception as e:
        # Captura cualquier otro error no previsto (ej. fallos en el pipeline)
        print(f"\n❌ FATAL ERROR: El pipeline falló inesperadamente: {e}")

if __name__ == "__main__":
    main()
    