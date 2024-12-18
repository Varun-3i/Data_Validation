import pandas as pd
import re

def completeness_score(column):
    """Calculate the completeness score of a column."""
    if len(column) == 0:
        return 0.0  # Return 0% if the column is empty
    return (len(column) - column.isnull().sum()) / len(column) * 100

def uniqueness_score(column):
    """Calculate the uniqueness score of a column."""
    if len(column) == 0:
        return 0.0  # Return 0% if the column is empty
    return column.nunique() / len(column) * 100

def validity_score(column, validation_function=None):
    """Calculate the validity score of a column based on a validation function."""
    if len(column) == 0:
        return 0.0  # Return 0% if the column is empty

    if validation_function is None:
        if pd.api.types.is_numeric_dtype(column):
            validation_function = lambda x: not pd.isna(x)
        elif pd.api.types.is_datetime64_any_dtype(column):
            validation_function = lambda x: not pd.isna(x)
        else:
            validation_function = lambda x: isinstance(x, str) and x.strip() != ""
    
    valid_entries = column.apply(validation_function).sum()
    return valid_entries / len(column) * 100

def timeliness_score(column, threshold_date):
    """Calculate the timeliness score of a datetime column."""
    if pd.api.types.is_datetime64_any_dtype(column):
        if threshold_date is None:
            raise ValueError("Threshold date must be provided and cannot be None.")
        
        threshold_date = pd.to_datetime(threshold_date).tz_localize(None)
        timely_entries = (column >= threshold_date).sum()
        return timely_entries / len(column) * 100

    return 100.0  # If not a datetime column, assume 100% timeliness

def accuracy_score(column, reference_column=None, threshold=None):
    """Calculate the accuracy score of a column compared to a reference column."""
    if reference_column is None:
        return 100.0  # Assume 100% accuracy if no reference is provided
    if len(column) == 0 or len(reference_column) == 0:
        return 0.0  # Return 0% if either column is empty

    if pd.api.types.is_numeric_dtype(column):
        if threshold is None:
            raise ValueError("Threshold must be provided for numerical columns.")
        correct_entries = (abs(column - reference_column) <= threshold).sum()
    else:
        correct_entries = (column == reference_column).sum()

    return correct_entries / len(column) * 100

def consistency_score(df, column1, column2=None, consistency_rule=None, default_score=100):
    """Calculates the consistency score by comparing two columns or applying a custom rule."""
    if column1 not in df.columns:
        print(f"Warning: Column '{column1}' does not exist. Returning default score.")
        return default_score

    if column2 and column2 not in df.columns:
        print(f"Warning: Column '{column2}' does not exist. Assuming 100% consistency.")
        return default_score

    if consistency_rule:
        inconsistent_entries = df.apply(consistency_rule, axis=1).sum()
    elif column2:
        if pd.api.types.is_numeric_dtype(df[column1]) and pd.api.types.is_numeric_dtype(df[column2]):
            inconsistent_entries = (df[column1] > df[column2]).sum()
        elif pd.api.types.is_datetime64_any_dtype(df[column1]) and pd.api.types.is_datetime64_any_dtype(df[column2]):
            inconsistent_entries = (df[column1] > df[column2]).sum()
        else:
            print(f"Warning: Columns '{column1}' and '{column2}' are not comparable. Returning default score.")
            return default_score
    else:
        return default_score

    total_entries = len(df)
    consistency = (1 - inconsistent_entries / total_entries) * 100 if total_entries > 0 else default_score

    return round(consistency, 2)

def calculate_scores(df, threshold_date=None, reference_columns=None):
    """Calculates data quality scores for each column in a DataFrame."""
    if threshold_date is None:
        threshold_date = pd.to_datetime("today")

    detailed_scores = {}

    for col in df.columns:
        column_data = df[col]

        # Calculate scores for each column
        column_scores = {
            "Completeness": completeness_score(column_data),
            "Timeliness": timeliness_score(column_data, threshold_date) if pd.api.types.is_datetime64_any_dtype(column_data) else 100,
            "Validity": validity_score(
                column_data,
                lambda x: bool(
                    re.match(
                        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", str(x)
                    )
                ),
            ) if "email" in col.lower() else 100,
            "Accuracy": accuracy_score(column_data, reference_columns.get(col) if reference_columns else None),
            "Uniqueness": uniqueness_score(column_data),
            "Consistency": consistency_score(df, col)
        }

        detailed_scores[col] = column_scores

    scores_df = pd.DataFrame(detailed_scores).T
    return scores_df

def overall_quality_score(scores_df):
    """Calculate the overall quality score as the mean of all scores."""
    return scores_df.mean().mean()
