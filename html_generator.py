import os
import re
import time

def text_to_professional_html():
    input_file = "Final_Electrical_MCQs_with_Images.txt"
    output_file = "Electrical_Engineering_Bank.html"
    image_folder = "mcq_images"

    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    topics_raw = re.split(r'={20,}', content)
    
    topic_data = []
    total_mcqs = 0
    
    for i in range(1, len(topics_raw), 2):
        title = topics_raw[i].strip()
        body = topics_raw[i+1] if i+1 < len(topics_raw) else ""
        mcq_count = len(re.findall(r'Q\d+:', body))
        total_mcqs += mcq_count
        topic_data.append({
            'title': title,
            'body': body,
            'count': mcq_count,
            'id': f"topic_{i}"
        })

    html_start = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Electrical Engineering MCQ Bank - Rising Engineer</title>
        
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        
        <style>
            :root {{ --primary: #2c3e50; --accent: #3498db; --success: #27ae60; }}
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f0f2f5; line-height: 1.6; color: #333; margin: 0; padding: 0; }}
            .container {{ max-width: 1000px; margin: auto; padding: 20px; }}
            
            .cover-page {{ height: 95vh; display: flex; flex-direction: column; justify-content: center; align-items: center; 
                         background: white; border: 15px solid var(--primary); margin: 20px; text-align: center; border-radius: 8px; box-sizing: border-box; }}
            .cover-title {{ font-size: 3.5em; color: var(--primary); margin-bottom: 10px; }}
            .author {{ font-size: 1.8em; color: var(--accent); font-weight: bold; margin-bottom: 50px; }}
            .stats-box {{ display: flex; gap: 30px; background: #eee; padding: 20px; border-radius: 10px; }}
            
            .toc-section {{ background: white; padding: 30px; border-radius: 8px; margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            .toc-list {{ columns: 2; column-gap: 40px; list-style: none; padding: 0; }}
            .toc-list li {{ margin-bottom: 10px; break-inside: avoid; }}
            .toc-list a {{ text-decoration: none; color: var(--accent); font-weight: 500; }}

            .topic-header {{ background: var(--primary); color: white; padding: 15px; border-radius: 5px; margin-top: 50px; scroll-margin-top: 20px; }}
            .question-card {{ background: white; border-left: 5px solid var(--accent); padding: 20px; margin: 20px 0; border-radius: 0 5px 5px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
            .img-box {{ text-align: center; margin: 15px 0; padding: 10px; background: #fff; }}
            .img-box img {{ max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; }}
            
            .btn-ans {{ background: var(--success); color: white; border: none; padding: 10px 20px; cursor: pointer; border-radius: 4px; margin-top: 15px; font-weight: bold; }}
            .ans-panel {{ display: none; background: #eef9f1; padding: 15px; margin-top: 10px; border-radius: 4px; border-left: 4px solid var(--success); }}
            
            /* MathJax scaling for small screens */
            .mjx-chtml {{ font-size: 110% !important; }}

            @media (max-width: 600px) {{ .toc-list {{ columns: 1; }} .cover-title {{ font-size: 2.2em; }} }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="cover-page">
                <div class="cover-title">Electrical Engineering<br>Comprehensive MCQ Bank</div>
                <div class="author">By: Rising Engineer</div>
                <div class="stats-box">
                    <div><b>Total Topics:</b> {len(topic_data)}</div>
                    <div><b>Total MCQs:</b> {total_mcqs}</div>
                </div>
            </div>

            <div class="toc-section">
                <h2>Table of Contents</h2>
                <ul class="toc-list">
    """

    for topic in topic_data:
        html_start += f'<li><a href="#{topic["id"]}">{topic["title"]} ({topic["count"]} Qs)</a></li>'

    html_start += "</ul></div>"

    content_html = ""
    for topic in topic_data:
        content_html += f'<h2 id="{topic["id"]}" class="topic-header">{topic["title"]}</h2>'
        
        qs = topic['body'].split("-" * 40)
        for q_idx, q_block in enumerate(qs):
            q_block = q_block.strip()
            if not q_block: continue
            
            lines = q_block.split('\n')
            q_text = lines[0]
            
            content_html += '<div class="question-card">'
            content_html += f'<div class="q-main"><b>{q_text}</b></div>'
            
            img_match = re.search(r'\[IMAGE_ID: (.*?)\]', q_block)
            if img_match:
                content_html += f'<div class="img-box"><img src="{image_folder}/{img_match.group(1)}"></div>'
            
            content_html += '<ul style="list-style:none; padding-left:15px; margin-top:10px;">'
            for line in lines:
                if any(line.strip().startswith(p) for p in ['A.', 'B.', 'C.', 'D.', 'E.']):
                    content_html += f'<li style="margin-bottom:8px;">{line.strip()}</li>'
            content_html += '</ul>'
            
            ans_m = re.search(r'>> Correct Answer: (.*)', q_block)
            exp_m = re.search(r'>> Explanation: (.*)', q_block)
            
            if ans_m:
                ans_v = ans_m.group(1)
                exp_v = exp_m.group(1) if exp_m else "No further explanation available."
                q_uid = f"ans_{topic['id']}_{q_idx}"
                
                content_html += f"""
                <button class="btn-ans" onclick="toggleAns('{q_uid}')">Show/Hide Answer & Solution</button>
                <div id="{q_uid}" class="ans-panel">
                    <b style="color:var(--success)">Correct Answer: {ans_v}</b><br>
                    <div style="margin-top:10px;"><b>Detailed Solution:</b><br>{exp_v}</div>
                </div>
                """
            content_html += '</div>'

    html_end = """
        </div>
        <script>
            function toggleAns(id) {
                var el = document.getElementById(id);
                if (el.style.display === "block") {
                    el.style.display = "none";
                } else {
                    el.style.display = "block";
                    // Trigger MathJax to re-render if it was hidden
                    if (window.MathJax) {
                        MathJax.typesetPromise([el]);
                    }
                }
            }
        </script>
    </body>
    </html>
    """

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_start + content_html + html_end)
    
    print(f"Success! Math-enabled HTML Created: {output_file}")

if __name__ == "__main__":
    text_to_professional_html()