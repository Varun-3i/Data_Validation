import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io
import base64

def generate_detailed_report(df, detailed_scores_df, overall_score):
    try:
        # Define the metrics list
        metrics = ['Completeness', 'Uniqueness', 'Validity', 'Timeliness', 'Consistency', 'Accuracy', 'Reliability']

        html_content = []

        # General Styling for the Report (with increased visualization size)
        html_content.append("""
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f7f9;
                color: #2c3e50;
            }
            h1, h2, h3 {
                text-align: center;
                margin-top: 10px;
                color: #2c3e50;
            }
            .container {
                width: 90%;
                margin: 20px auto;
                padding: 20px;
                background-color: #ffffff;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                border-radius: 10px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                background: #fff;
                border-radius: 8px;
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
            }
            th, td {
                padding: 12px;
                border: 1px solid #ddd;
                text-align: center;
            }
            th {
                background-color: #2c3e50;
                color: white;
                text-transform: uppercase;
            }
            tr:nth-child(even) {
                background-color: #f8f9fa;
            }
            tr:hover {
                background-color: #eaf4f9;
            }
            .overall-score {
                text-align: center;
                font-size: 22px;
                color: #004e92;
                font-weight: bold;
            }
            select {
                display: block;
                margin: 20px auto;
                padding: 10px;
                width: 30%;
                text-align: center;
                border: 1px solid #ccc;
                border-radius: 6px;
            }
            .chart-container {
                display: none;
                text-align: center;
                margin-top: 20px;
            }
            .chart-container img {
                max-width: 80%;
                width: 80%;
                margin: auto;
                border-radius: 10px;
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
            }
            /* Added styling for side-by-side layout of charts */
            .charts-side-by-side {
                display: flex;
                justify-content: space-around;
                gap: 40px;
            }
            .chart {
                max-width: 60%; /* Increase the size of visualizations */
            }
        </style>
        """)

        # Start of Content
        html_content.append("<div class='container'>")

        # Overall Score Section
        html_content.append(f"<div class='overall-score'>Overall Data Quality Score: {overall_score:.2f}%</div>")

        # Column-wise Detailed Scores
        html_content.append("<table>")
        html_content.append("<tr><th>Column</th>" + "".join(f"<th>{metric}</th>" for metric in metrics) + "</tr>")
        for col, scores in detailed_scores_df.iterrows():
            html_content.append("<tr>" + f"<td>{col}</td>" + "".join(f"<td>{scores.get(metric, 0):.2f}%</td>" for metric in metrics) + "</tr>")
        html_content.append("</table>")

        # Overall Quality Metrics Table
        html_content.append("<h4>Average Quality scores</h4>")
        html_content.append("<table>")
        html_content.append("<tr><th>Metric</th><th>Average Score (%)</th></tr>")
        for metric in metrics:
            overall_metric_score = detailed_scores_df[metric].mean()
            html_content.append(f"<tr><td>{metric}</td><td>{overall_metric_score:.2f}%</td></tr>")
        html_content.append("</table>")

        # Dropdown for Charts
        html_content.append("""
        <h4>Select a Column to View Visualizations</h4>
        <select id="column-select" onchange="showChart(this.value)">
            <option value="">Select a Column</option>
        """)

        charts_data = {}
        for col, scores in detailed_scores_df.iterrows():
            html_content.append(f"<option value='{col}'>{col}</option>")
            values = [scores.get(metric, 0) for metric in metrics]

            # Generate Bar Chart
            plt.figure(figsize=(8, 6))
            plt.bar(metrics, values, color='#3498db')
            plt.title(f"{col}")
            plt.xticks(rotation=45)
            plt.tight_layout()
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=100)
            buffer.seek(0)
            bar_chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            plt.close()

            # Generate Heatmap
            plt.figure(figsize=(8, 6))
            sns.heatmap(np.array(values).reshape(1, -1), annot=True, fmt=".2f", cmap="coolwarm", cbar=False, xticklabels=metrics, yticklabels=[col])
            plt.title(f"{col}")
            plt.tight_layout()
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=100)
            buffer.seek(0)
            heatmap = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            plt.close()


            charts_data[col] = {'bar_chart': bar_chart, 'heatmap': heatmap}

        html_content.append("</select>")

        # Charts Section
        html_content.append("<div class='chart-container' id='chart-container'>")
        for col, charts in charts_data.items():
            html_content.append(f"""
            <div id="{col}-charts" style="display:none;" class="charts-side-by-side">
                <div class="chart">
                    <h3>Bar Chart</h3>
                    <img src='data:image/png;base64,{charts['bar_chart']}' alt='{col} Bar Chart'>
                </div>
                <div class="chart">
                    <h3>Heatmap</h3>
                    <img src='data:image/png;base64,{charts['heatmap']}' alt='{col} Heatmap'>
                </div>
            </div>
            """)
        html_content.append("</div>")  # End Chart Container

        # JavaScript for Interactivity
        html_content.append("""
        <script>
            function showChart(column) {
                const charts = document.querySelectorAll("[id$='-charts']");
                charts.forEach(chart => chart.style.display = 'none');
                
                if (column) {
                    const selectedChart = document.getElementById(`${column}-charts`);
                    document.getElementById("chart-container").style.display = 'block';
                    selectedChart.style.display = 'flex';
                } else {
                    document.getElementById("chart-container").style.display = 'none';
                }
            }
        </script>
        """)

        # End of Container
        html_content.append("</div>")

        return "\n".join(html_content)

    except Exception as e:
        print(f"Error generating report: {e}")
        return ""