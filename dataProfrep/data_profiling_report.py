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
<link rel="stylesheet" href="dataProfrep\\Dpr.css">

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
