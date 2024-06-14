import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs

def download_images(url, save_folder):
    # Add a user-agent header to mimic a web browser
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    # Send an HTTP request to the website with headers
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all image tags in the HTML
        img_tags = soup.find_all('img')

        # Create the save folder if it doesn't exist
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        # Download and save each image
        for img_tag in img_tags:
            img_url = img_tag.get('src')
            if img_url:
                img_url = urljoin(url, img_url)

                # Include query parameters in the image name
                img_name = os.path.join(save_folder, url_to_filename(img_url))
                
                # Download the image with headers
                with open(img_name, 'wb') as img_file:
                    img_file.write(requests.get(img_url, headers=headers).content)
                
                print(f"Downloaded: {img_name}")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

# Function to convert URL to a valid filename
def url_to_filename(url):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    # Include query parameters in the filename
    query_params = parse_qs(parsed_url.query)
    if query_params:
        filename = filename.split('.')[0] + '.png'
    
    return filename

# Example usage:
website_url = 'https://blog.99cluster.com/blog/tips/back-to-basics-part-i-elements-of-design-with-printmaking/?_ga=2.84283353.1780515130.1701429293-198057938.1701429293'
save_directory = 'D:\\Programming\\image_download'  # Use double backslashes in the path or a raw string

download_images(website_url, save_directory)
