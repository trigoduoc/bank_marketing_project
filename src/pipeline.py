import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from src.transformers import (
    DropColumnsTransformer,
    UnknownToNaNTransformer,
    DropHighMissingTransformer,
    SmartImputerTransformer,
    OutlierCapper,
    DropZeroVarianceTransformer
)

def build_preprocessing_pipeline(df, columns_to_drop=None):
    """
    Builds and returns a generic scikit-learn preprocessing pipeline.
    Dynamically detects numeric and categorical columns.
    """
    if columns_to_drop is None:
        columns_to_drop = []

    # 1. Ruta para números
    num_pipe = Pipeline([
        ('capper', OutlierCapper(apply_capping=True)),
        ('zero_variance', DropZeroVarianceTransformer()),
        ('scaler', StandardScaler())
    ])

    # 2. Ruta para textos
    cat_pipe = Pipeline([
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    # 3. El enrutador maestro
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_pipe, make_column_selector(dtype_include='number')),
            ('cat', cat_pipe, make_column_selector(dtype_exclude='number'))
        ], remainder='drop'
    )

    # 4. El Súper Pipeline
    full_pipeline = Pipeline([
        ('drop_leaks', DropColumnsTransformer(columns_to_drop=columns_to_drop)),
        ('clean_unknowns', UnknownToNaNTransformer()),
        ('drop_high_nan', DropHighMissingTransformer(threshold=0.8)),
        ('smart_imputer', SmartImputerTransformer(low_threshold=0.10)),
        ('preprocessing', preprocessor)
    ])

    return full_pipeline
