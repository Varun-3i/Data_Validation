import os
from ydata_profiling import ProfileReport

# Generate Detailed Report
def generate_detailed_report(df, detailed_scores_df, overall_score, output_path="detailed_data_quality_report.html"):
    try:
        # Use relative path for CSS
        css_path = "CSS/style.css"
        
        html_content = [
            f"<html><head><title>Detailed Data Quality Report</title><link rel='stylesheet' href='{css_path}'></head><body>"
        ]

        html_content.append("<h1>Detailed Data Quality Scores</h1>")
        html_content.append(f"<h2>Overall Data Quality Score: {overall_score:.2f}</h2>")

        html_content.append("<table>")
        html_content.append("<tr><th>Column</th><th>Completeness</th><th>Uniqueness</th><th>Validity</th><th>Timeliness</th><th>Consistency</th><th>Accuracy</th><th>Reliability</th></tr>")

        for col, scores in detailed_scores_df.iterrows():
            html_content.append(
                f"<tr><td>{col}</td><td>{scores.get('Completeness', 0):.2f}%</td><td>{scores.get('Uniqueness', 0):.2f}%</td>"
                f"<td>{scores.get('Validity', 0):.2f}%</td><td>{scores.get('Timeliness', 0):.2f}%</td><td>{scores.get('Consistency', 0):.2f}%</td>"
                f"<td>{scores.get('Accuracy', 0):.2f}%</td><td>{scores.get('Reliability', 0):.2f}%</td></tr>"
            )

        html_content.append("</table>")
        html_content.append("</body></html>")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(html_content))

        print(f"Detailed Data Quality Report generated successfully: {output_path}")

    except Exception as e:
        print(f"Error generating detailed report: {e}")


# Generate Quality Summary Report
def generate_quality_summary(df, scores_df, output_path="quality_summary_report.html"):
    try:
        # Use relative path for CSS
        css_path = "CSS/summary_style.css"
        
        html_content = [
            f"<html><head><title>Quality Summary Report</title><link rel='stylesheet' href='{css_path}'></head><body>"
        ]

        html_content.append("<h1>Quality Summary Report</h1>")

        for metric in scores_df.columns:
            columns_passing = scores_df[scores_df[metric] >= 80].index.tolist()
            passing_percentage = (len(columns_passing) / len(scores_df)) * 100
            html_content.append(f"<h2>{metric} ({passing_percentage:.2f}% Passing)</h2>")

            if columns_passing:
                html_content.append("<ul>")
                for col in columns_passing:
                    html_content.append(f"<li>{col}</li>")
                html_content.append("</ul>")
            else:
                html_content.append("<p>No columns passed this metric.</p>")

        html_content.append("</body></html>")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(html_content))

        print(f"Quality Summary Report generated successfully: {output_path}")

    except Exception as e:
        print(f"Error generating quality summary report: {e}")


# Generate YData Profiling Report
def generate_ydata_profiling_report(df, output_path="ydata_profiling_report.html"):
    try:
        profile = ProfileReport(df, title="YData Profiling Report", explorative=True)
        profile.to_file(output_path)
        print(f"YData Profiling Report generated successfully: {output_path}")
    except Exception as e:
        print(f"Error generating YData profiling report: {e}")