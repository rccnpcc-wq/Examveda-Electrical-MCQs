import requests
from bs4 import BeautifulSoup
import time
import os
import re

def fetch_all_electrical_mcqs():
    base_url = "https://www.examveda.com"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    output_file = "Final_Electrical_MCQs_with_Images.txt"
    image_folder = "mcq_images"

    # Ensure the image folder exists
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    try:
        # Step 1: Get the master list of topics
        response = requests.get(f"{base_url}/mcq-question-on-electrical-engineering/", headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')

        found_topics = []
        all_links = soup.find_all('a', href=True)
        for l in all_links:
            href = l.get('href')
            if '/electrical-engineering/practice-mcq-question-on-' in href:
                text = l.text.strip()
                full_url = href if href.startswith('http') else f"{base_url}{href}"
                if text and full_url not in [t[1] for t in found_topics]:
                    found_topics.append((text, full_url))

        # --- RESUME SETTINGS ---
        # Set to 40 to resume from Topic 41. Set to 0 to start a brand new file.
        start_from = 0  
        mode = "w" if start_from > 0 else "w"

        print(f"Starting Process at Topic {start_from + 1}...")
        print("Note: Command line will only show a summary when a topic is fully complete.\n")

        with open(output_file, mode, encoding="utf-8") as f:
            for topic_idx, (topic_name, topic_base_url) in enumerate(found_topics[start_from:], start_from + 1):
                # Sanitize topic name for image filenames
                clean_topic_name = re.sub(r'[^\w\s-]', '', topic_name).replace(' ', '_')
                
                f.write(f"\n{'='*80}\nTOPIC {topic_idx}: {topic_name}\n{'='*80}\n\n")

                current_page = 1
                total_questions_in_topic = 0

                while True:
                    page_url = topic_base_url if current_page == 1 else f"{topic_base_url}?page={current_page}"
                    
                    try:
                        page_resp = requests.get(page_url, headers=headers, timeout=15)
                        page_soup = BeautifulSoup(page_resp.text, 'html.parser')
                    except:
                        break # Skip to next topic on network error

                    questions = page_soup.find_all('article', class_='question')
                    if not questions: break # Topic is finished

                    valid_qs_on_page = 0
                    for q in questions:
                        try:
                            q_text_div = q.find('div', class_='question-main')
                            if not q_text_div or not q_text_div.get_text(strip=True): continue

                            total_questions_in_topic += 1
                            valid_qs_on_page += 1
                            
                            # 1. Write Question Text
                            f.write(f"Q{total_questions_in_topic}: {q_text_div.get_text(strip=True)}\n")

                            # 2. Image Downloader Logic
                            all_imgs = q.find_all('img')
                            for img_idx, img in enumerate(all_imgs, 1):
                                img_src = img.get('src')
                                if img_src:
                                    if img_src.startswith('/'): img_src = f"{base_url}{img_src}"
                                    
                                    # Orderly naming: TopicName_Q#_Img#.png
                                    img_filename = f"{clean_topic_name}_Q{total_questions_in_topic}_Img{img_idx}.png"
                                    img_save_path = os.path.join(image_folder, img_filename)
                                    
                                    try:
                                        img_data = requests.get(img_src, headers=headers, timeout=10).content
                                        with open(img_save_path, 'wb') as handler:
                                            handler.write(img_data)
                                        f.write(f"   [IMAGE_ID: {img_filename}]\n")
                                    except:
                                        f.write(f"   [IMAGE_ERROR: {img_src}]\n")

                            # 3. Extract Options
                            for opt in q.find_all('p'):
                                opt_text = opt.get_text(strip=True)
                                if opt_text and any(opt_text.startswith(p) for p in ['A.', 'B.', 'C.', 'D.', 'E.']):
                                    f.write(f"   {opt_text}\n")

                            # 4. Extract Answer & Explanation
                            ans_container = q.find('div', class_='answer_container')
                            if ans_container:
                                ans_tag = ans_container.find('strong')
                                if ans_tag:
                                    f.write(f"   >> Correct Answer: {ans_tag.get_text(strip=True)}\n")
                                
                                # Safety conversion to string for complex math formatting
                                raw_ans = str(ans_container.get_text(" ", strip=True))
                                if "Solution:" in raw_ans:
                                    f.write(f"   >> Explanation: {raw_ans.split('Solution:')[1].strip()}\n")
                            
                            f.write("-" * 40 + "\n")
                        except:
                            continue

                    if valid_qs_on_page == 0: break
                    current_page += 1
                    time.sleep(1) # Delay to be safe and steady

                # Output topic summary to CMD
                print(f"Topic {topic_idx}: {topic_name} ; Pages: {current_page-1}, Questions: {total_questions_in_topic}  Complete.")
                f.write(f"\nTotal Questions in {topic_name}: {total_questions_in_topic}\n\n")

        print(f"\nMISSION COMPLETE! File saved as: {output_file}")

    except Exception as e:
        print(f"A Fatal error occurred: {e}")

if __name__ == "__main__":
    fetch_all_electrical_mcqs()