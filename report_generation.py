from ydata_profiling import ProfileReport
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

def generate_detailed_report(df, detailed_scores_df, overall_score):
    try:
        html_content = []

        # Section 1: Detailed Quality Scores
        html_content.append("<h1>Detailed Data Quality Scores</h1>")
        html_content.append(f"<h2>Overall Data Quality Score: {overall_score:.2f}</h2>")
        html_content.append("<table>")
        html_content.append("<tr><th>Column</th><th>Completeness</th><th>Uniqueness</th><th>Validity</th>"
                            "<th>Timeliness</th><th>Consistency</th><th>Accuracy</th><th>Reliability</th></tr>")
        for col, scores in detailed_scores_df.iterrows():
            html_content.append(
                f"<tr><td>{col}</td><td>{scores.get('Completeness', 0):.2f}%</td>"
                f"<td>{scores.get('Uniqueness', 0):.2f}%</td>"
                f"<td>{scores.get('Validity', 0):.2f}%</td><td>{scores.get('Timeliness', 0):.2f}%</td>"
                f"<td>{scores.get('Consistency', 0):.2f}%</td>"
                f"<td>{scores.get('Accuracy', 0):.2f}%</td><td>{scores.get('Reliability', 0):.2f}%</td></tr>"
            )
        html_content.append("</table>")

        # Section 2: Quality Metrics Visualizations (Separate Container)
        html_content.append("<div id='visualization-container' style='margin: 30px 0; padding: 20px; border: 1px solid #ccc; border-radius: 10px; background-color: #f9f9f9;'>")
        html_content.append("<h2>Visualizations for Quality Metrics</h2>")
        html_content.append("<div class='dropdown-container' style='margin: 20px;'>")
        html_content.append("<select id='column-select' onchange='showColumnCharts(this.value)' style='padding: 10px; width: 100%; max-width: 300px;'>")
        html_content.append("<option value=''>Select a Column</option>")
        charts_data = {}

        # Generate Visualizations
        for col, scores in detailed_scores_df.iterrows():
            html_content.append(f"<option value='{col}'>{col}</option>")

            metrics = ['Completeness', 'Uniqueness', 'Validity', 'Timeliness', 'Consistency', 'Accuracy', 'Reliability']
            values = [scores.get(metric, 0) for metric in metrics]

            # Bar chart
            plt.figure(figsize=(5, 3))
            plt.bar(metrics, values, color='skyblue')
            plt.title(f"Bar Chart for {col}", fontsize=12)
            plt.xticks(rotation=45, ha='right', fontsize=8)
            plt.ylabel("Percentage (%)", fontsize=10)
            plt.tight_layout()

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=100)
            buffer.seek(0)
            bar_chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            plt.close()

            # Radar chart
            angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
            values += values[:1]
            angles += angles[:1]

            plt.figure(figsize=(4, 4))
            ax = plt.subplot(111, polar=True)
            ax.fill(angles, values, color='skyblue', alpha=0.5)
            ax.plot(angles, values, color='skyblue', linewidth=2)
            ax.set_yticks([20, 40, 60, 80, 100])
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(metrics, fontsize=8)
            plt.title(f"Radar Chart for {col}", fontsize=12, pad=20)

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=100)
            buffer.seek(0)
            radar_chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            plt.close()

            # Pie chart
            plt.figure(figsize=(4, 4))
            plt.pie(values[:-1], labels=metrics, autopct='%1.1f%%', colors=plt.cm.Paired.colors)
            plt.title(f"Pie Chart for {col}", fontsize=12)

            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=100)
            buffer.seek(0)
            pie_chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            plt.close()

            charts_data[col] = {
                'bar_chart': bar_chart,
                'radar_chart': radar_chart,
                'pie_chart': pie_chart,
            }

        html_content.append("</select>")
        html_content.append("</div>")

        # Charts container
        html_content.append("<div id='charts-container' style='display: none; margin-top: 20px;'>")
        for col, charts in charts_data.items():
            html_content.append(f"""
            <div id='{col}-charts' class='chart-section' style='display: none;'>
                <h3>{col} Visualizations</h3>
                <div style='display: flex; justify-content: space-evenly; flex-wrap: wrap;'>
                    <div style='margin: 10px;'>
                        <h4>Bar Chart</h4>
                        <img src='data:image/png;base64,{charts['bar_chart']}' style='max-width: 100%; height: auto;' />
                    </div>
                    <div style='margin: 10px;'>
                        <h4>Radar Chart</h4>
                        <img src='data:image/png;base64,{charts['radar_chart']}' style='max-width: 100%; height: auto;' />
                    </div>
                    <div style='margin: 10px;'>
                        <h4>Pie Chart</h4>
                        <img src='data:image/png;base64,{charts['pie_chart']}' style='max-width: 100%; height: auto;' />
                    </div>
                </div>
            </div>
            """)

        html_content.append("</div>")  # Close charts-container
        html_content.append("</div>")  # Close visualization-container

        # JavaScript for interactivity
        html_content.append("""
<script>
    function showColumnCharts(column) {
        // Hide all chart sections
        const chartSections = document.querySelectorAll('.chart-section');
        chartSections.forEach(section => section.style.display = 'none');

        // Show selected column's charts
        if (column) {
            const selectedSection = document.getElementById(`${column}-charts`);
            if (selectedSection) {
                document.getElementById('charts-container').style.display = 'block';
                selectedSection.style.display = 'block';
            }
        } else {
            document.getElementById('charts-container').style.display = 'none';
        }
    }
</script>
""")

        return "\n".join(html_content)
    except Exception as e:
        print(f"Error generating report with dropdown visualizations: {e}")
        return ""

def generate_quality_summary(df, scores_df):
    try:
        # Initialize the HTML content
        html_content = []
        html_content.append("<h1>Quality Summary Report</h1>")

        # Start the outer container for horizontal alignment
        html_content.append('<div style="display: flex; flex-wrap: wrap; gap: 20px;">')

        for metric in scores_df.columns:
            # Get columns passing the quality metric
            columns_passing = scores_df[scores_df[metric] >= 80].index.tolist()
            passing_percentage = (len(columns_passing) / len(scores_df)) * 100

            # Add each metric section
            html_content.append('<div style="flex: 1; min-width: 200px;">')
            html_content.append(f"<h2>{metric} ({passing_percentage:.2f}% Passing)</h2>")

            if columns_passing:
                # List of columns passing the metric
                html_content.append("<ul>")
                for col in columns_passing:
                    html_content.append(f"<li>{col}</li>")
                html_content.append("</ul>")
            else:
                html_content.append("<p>No columns passed this metric.</p>")

            html_content.append('</div>')  # Close the metric container

        html_content.append('</div>')  # Close the outer container
        return "\n".join(html_content)
    except Exception as e:
        print(f"Error generating quality summary report: {e}")
        return ""


def generate_ydata_profiling_report(df, detailed_report_content, quality_summary_content, output_path="ydata_profiling_report.html"):
    try:
        # Generate the YData Profiling report
        profile = ProfileReport(df, title="YData Profiling Report", explorative=True)

        # Save the profiling report to a temporary file
        temp_path = "temp_report.html"
        profile.to_file(temp_path)

        with open(temp_path, "r", encoding="utf-8") as f:
            report_html = f.read()

        # Extract just the body content of the YData Profiling report (to avoid duplication)
        start_body = report_html.find("<body>") + len("<body>")
        end_body = report_html.find("</body>")
        profile_body_content = report_html[start_body:end_body]

        # Generate navbar and styling
        custom_sections = f"""
<style>
    body {{
        font-family: Arial, sans-serif;
        background-color: #f4f4f9;
        margin: 0;
        padding: 0;
    }}
    .navbar {{
    display: flex;
    justify-content: flex-start; /* Align links to the left */
    align-items: center;
    background-color: #ffffff;
    color: #333;
    padding: 10px 20px; /* Reduced padding */
    position: sticky;
    top: 0;
    z-index: 1000;
    border-bottom: 1px solid #ddd;
    }}
    .navbar a {{
    color: #007bff;
    text-decoration: none;
    padding: 5px 10px; /* Smaller padding for tighter spacing */
    margin-right: 10px; /* Reduce spacing between links */
    border-radius: 5px;
    font-size: 16px;
    transition: background-color 0.3s ease;
    }}
    .navbar a:hover {{
        background-color: #f0f0f0;
    }}
    .section-content {{
        display: none;
        margin: 20px auto;
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 8px;
        background-color: #ffffff;
        width: 90%;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    .section-content.active {{
        display: block;
    }}
    .section-title {{
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 15px;
        color: #333;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
    }}
    th, td {{
        border: 1px solid #ddd;
        padding: 12px;
        text-align: center;
    }}
    th {{
        background-color: #007bff;
        color: white;
    }}
    tr:nth-child(even) {{
        background-color: #f9f9f9;
    }}
    tr:hover {{
        background-color: #f1f1f1;
    }}
    ul {{
        list-style-type: disc;
        margin: 20px;
        padding-left: 40px;
    }}
    li {{
        margin: 5px 0;
    }}
    .quality-summary {{
        font-family: 'Arial', sans-serif;
        background-color: #f9f9f9;
        color: #333;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #ddd;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    .quality-summary h1, .quality-summary h2 {{
        text-align: center;
        color: #333;
        margin-bottom: 15px;
    }}
</style>

<div class="navbar">
    <a href="#" onclick="showSection('overview')">Overview</a>
    <a href="#" onclick="showSection('detailed-report')">Detailed Quality Report</a>
    <a href="#" onclick="showSection('quality-summary')">Quality Summary</a>
</div>

<div id="overview" class="section-content active">
    <h2 class="section-title">Overview</h2>
    {profile_body_content}
</div>
<div id="detailed-report" class="section-content">
    <h2 class="section-title">Detailed Quality Report</h2>
    {detailed_report_content}
</div>
<div id="quality-summary" class="section-content quality-summary">
    <h2 class="section-title">Quality Summary</h2>
    {quality_summary_content}
</div>

<script>
    function showSection(sectionId) {{
        // Hide all sections
        const sections = document.querySelectorAll('.section-content');
        sections.forEach(section => section.classList.remove('active'));

        // Show the selected section
        const selectedSection = document.getElementById(sectionId);
        if (selectedSection) {{
            selectedSection.classList.add('active');
        }}
    }}
</script>
"""

        # Replace <body> tag to include the custom sections
        report_html = report_html[:start_body] + custom_sections + report_html[end_body:]

        # Write the final report to the output file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report_html)

        print(f"YData Profiling Report generated successfully: {output_path}")
    except Exception as e:
        print(f"Error generating YData profiling report: {e}")

