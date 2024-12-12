from data_loader import load_dataset
from data_quality_metrics import calculate_scores, overall_quality_score
from report_generation import generate_detailed_report, generate_quality_summary, generate_ydata_profiling_report

# Main block to run the data pipeline and generate reports
if __name__ == "__main__":
    dataset_path = "detail_ds.csv"  # Update with your dataset path
    df = load_dataset(dataset_path)

    # Calculate data quality scores without cleaning the data
    detailed_scores_df = calculate_scores(df)
    overall_score = overall_quality_score(detailed_scores_df)

    # Generate detailed data quality report
    generate_detailed_report(df, detailed_scores_df, overall_score)

    # Generate quality summary report
    generate_quality_summary(df, detailed_scores_df)

    # Generate YData profiling report
    generate_ydata_profiling_report(df)