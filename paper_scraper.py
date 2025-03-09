import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

def get_arxiv_abstracts():
    # Base URL for arXiv CS.CR recent papers
    base_url = "https://arxiv.org"
    list_url = "https://arxiv.org/list/cs.CR/recent?skip=0&show=25"
    
    try:
        # Step 1: Get the listing page
        response = requests.get(list_url)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Step 2: Find all links with href containing "/abs/"
        abs_links = []
        for link in soup.find_all('a', href=True):
            if "/abs/" in link['href']:
                full_url = base_url + link['href']
                if full_url not in abs_links:  # Avoid duplicates
                    abs_links.append(full_url)
        
        # Step 3 & 4: Visit each abstract page and extract abstract
        results = []
        for abs_url in abs_links:
            try:
                # Get the abstract page
                abs_response = requests.get(abs_url)
                abs_response.raise_for_status()
                
                # Parse the abstract page
                abs_soup = BeautifulSoup(abs_response.text, 'html.parser')
                
                # Find the abstract element
                abstract_elem = abs_soup.find('blockquote', class_='abstract mathjax')
                if abstract_elem:
                    # Extract text, removing "Abstract" prefix if present
                    abstract_text = abstract_elem.get_text(strip=True)
                    if abstract_text.startswith('Abstract'):
                        abstract_text = abstract_text[len('Abstract'):].strip()
                    
                    # Append URL and abstract to results
                    results.append(f"URL: {abs_url}\nAbstract: {abstract_text}\n")
                else:
                    results.append(f"URL: {abs_url}\nAbstract: Not found\n")
                    
            except requests.RequestException as e:
                results.append(f"URL: {abs_url}\nAbstract: Error fetching abstract: {str(e)}\n")
        
        # Step 5: Save to file in a new dated folder
        current_date = datetime.now().strftime('%Y%m%d')
        base_path = r"C:\Users\------------------------YOUR PATH HERE!!--------------------------------------------------"
        folder_path = os.path.join(base_path, current_date)
        
        # Create the folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)
        
        # Define the full file path
        filename = os.path.join(folder_path, f"{current_date}_arxiv_cyber.txt")
        
        # Write results to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(results))
        
        return f"Results saved to {filename}"
    
    except requests.RequestException as e:
        return f"Error fetching listing page: {str(e)}"
    except Exception as e:
        return f"Error processing data: {str(e)}"

# Execute and print confirmation
result = get_arxiv_abstracts()
print(result)