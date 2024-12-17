from ydata_profiling import ProfileReport

def generate_ydata_profiling_report(df, detailed_report_content, quality_summary_content, output_path="ydata_profiling_report.html"):
    try:
        # Generate the YData Profiling report
        profile = ProfileReport(df, title="YData Profiling Report", explorative=True)

        # Save the profiling report to a temporary file
        temp_path = "temp_report.html"
        profile.to_file(temp_path)

        with open(temp_path, "r", encoding="utf-8") as f:
            report_html = f.read()

        # Extract just the body content of the YData Profiling report
        start_body = report_html.find("<body>") + len("<body>")
        end_body = report_html.find("</body>")
        profile_body_content = report_html[start_body:end_body]

        custom_sections = f"""
<style>
    /* General Reset */
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    body {{
        font-family: 'Poppins', Arial, sans-serif;
        background-color: #f4f7fb;
        color: #333;
        line-height: 1.8;
    }}
    html {{
        scroll-behavior: smooth;
    }}

    /* Navbar Styling */
    .navbar {{
        display: flex;
        justify-content: center;
        align-items: center;
        background: linear-gradient(120deg, #004e92, #000428);
        color: #fff;
        padding: 15px 20px;
        position: sticky;
        top: 0;
        z-index: 1000;
        width: 100%;
    }}
    .navbar a {{
        color: #fff;
        text-decoration: none;
        font-size: 16px;
        font-weight: 600;
        margin: 0 20px;
        padding: 8px 12px;
        border-radius: 5px;
        transition: all 0.3s ease;
    }}
    .navbar a:hover {{
        background-color: rgba(255, 255, 255, 0.1);
    }}

    /* Sections */
    .section-content {{
        display: none;
        padding: 25px;
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        animation: fadeIn 0.5s ease-in-out;
        margin: 20px auto;
        max-width: 95%;
    }}
    .section-content.active {{
        display: block;
    }}
    .section-title {{
        font-size: 28px;
        font-weight: 700;
        text-align: center;
        color: #004e92;
        margin-bottom: 15px;
    }}
    .quality-summary {{
        padding: 30px;
        background: #e8f0fe;
        border-radius: 12px;
        text-align: center;
        font-size: 20px;
        color: #555;
    }}
    @keyframes fadeIn {{
        from {{
            opacity: 0;
            transform: translateY(10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
</style>

<!-- Navbar -->
<div class="navbar">
    <a href="#" onclick="showSection('overview')"><i class="fas fa-chart-pie"></i> Overview</a>
    <a href="#" onclick="showSection('detailed-report')"><i class="fas fa-list"></i> Detailed Report</a>
    <a href="#" onclick="showSection('quality-summary')"><i class="fas fa-check-circle"></i> Quality Summary</a>
</div>

<!-- Sections -->
<div id="overview" class="section-content active">
    {profile_body_content}
</div>

<div id="detailed-report" class="section-content">
    <h2 class="section-title">Detailed Quality Report</h2>
    {detailed_report_content}
</div>

<div id="quality-summary" class="section-content">
    <h2 class="section-title">Quality Summary</h2>
    <div class="quality-summary">{quality_summary_content}</div>
</div>

<script>
    function showSection(sectionId) {{
        const sections = document.querySelectorAll('.section-content');
        sections.forEach(section => section.classList.remove('active'));
        document.getElementById(sectionId).classList.add('active');
    }}
</script>

<script src="https://kit.fontawesome.com/a076d05399.js" crossorigin="anonymous"></script>
"""

        # Replace <body> tag to include the custom sections
        report_html = report_html[:start_body] + custom_sections + report_html[end_body:]

        # Write the final report to the output file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report_html)
        print(f"Report saved successfully to {output_path}")
    except Exception as e:
        print(f"Error generating YData profiling report: {e}")
