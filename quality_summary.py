def generate_quality_summary(df, scores_df):
    try:
        # Initialize the HTML content with inline CSS for styling
        html_content = []
        html_content.append("""
        <style>
            /* General Reset and Body Styling */
            body {
                font-family: 'Arial', sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 0;
                background-color: #f4f7f8;
                color: #333;
            }

            h1 {
                text-align: center;
                color: #2c3e50;
                font-size: 2.5rem;
                margin: 20px 0;
            }

            /* Main Container Styling */
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }

            /* Flexbox Cards for Metrics */
            .metrics-container {
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                justify-content: center;
            }

            .metric-card {
                flex: 1;
                min-width: 300px;
                background: linear-gradient(145deg, #ffffff, #e6e6e6);
                border-radius: 15px;
                box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.1);
                transition: transform 0.2s ease-in-out;
                padding: 20px;
                text-align: center;
            }

            .metric-card:hover {
                transform: translateY(-5px);
                box-shadow: 4px 6px 15px rgba(0, 0, 0, 0.2);
            }

            .metric-title {
                font-size: 1.5rem;
                color: #007bff;
                margin-bottom: 15px;
                font-weight: bold;
            }

            .passing-percentage {
                font-size: 1.2rem;
                color: #28a745;
                font-weight: bold;
                margin-bottom: 10px;
            }

            /* List of Columns */
            .columns-list {
                list-style: none;
                padding: 0;
            }

            .columns-list li {
                padding: 8px;
                margin-bottom: 5px;
                background: #f0f9ff;
                color: #333;
                border-radius: 5px;
                transition: background 0.2s ease-in-out;
            }

            .columns-list li:hover {
                background: #007bff;
                color: #fff;
            }

            /* Footer for No Columns Passed */
            .no-columns {
                color: #ff0000;
                font-style: italic;
            }
        </style>

        <div class="container">
            <div class="metrics-container">
        """)

        # Generate HTML content for each metric card
        for metric in scores_df.columns:
            columns_passing = scores_df[scores_df[metric] >= 80].index.tolist()
            passing_percentage = (len(columns_passing) / len(scores_df)) * 100

            html_content.append(f"""
            <div class="metric-card">
                <div class="metric-title">{metric}</div>
                <div class="passing-percentage">{passing_percentage:.2f}% Passing</div>
            """)

            if columns_passing:
                html_content.append("<ul class='columns-list'>")
                for col in columns_passing:
                    html_content.append(f"<li>{col}</li>")
                html_content.append("</ul>")
            else:
                html_content.append("<p class='no-columns'>No columns passed this metric.</p>")

            html_content.append("</div>")  # Closing metric-card

        # Close containers
        html_content.append("""
            </div> <!-- Closing metrics-container -->
        </div> <!-- Closing container -->
        """)

        return "\n".join(html_content)

    except Exception as e:
        print(f"Error generating quality summary report: {e}")
        return ""