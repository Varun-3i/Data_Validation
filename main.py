from data_loader import load_dataset
from data_quality_metrics import calculate_scores, overall_quality_score
from report_generation import generate_detailed_report, generate_quality_summary, generate_ydata_profiling_report
import matplotlib
matplotlib.use("Agg")

if __name__ == "__main__":
    dataset_path = "detail_ds.csv"
    df = load_dataset(dataset_path)

    detailed_scores_df = calculate_scores(df)
    overall_score = overall_quality_score(detailed_scores_df)

    detailed_report_content = generate_detailed_report(df, detailed_scores_df, overall_score)
    quality_summary_content = generate_quality_summary(df, detailed_scores_df)

    generate_ydata_profiling_report(df, detailed_report_content, quality_summary_content)