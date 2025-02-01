class HTMLGenerator:
    def __init__(self):
        self.base_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome</title>
  
</head>
<body>
    <div class="greeting">
        <h1>Hello Hector!</h1>
        <p>You accessed from: {url}</p>
    </div>
</body>
</html>
"""

    def generate_html(self, url):
        """
        Generate HTML content with the given URL
        
        Args:
            url (str): The URL to include in the output
            
        Returns:
            str: The complete HTML content
        """
        return self.base_template.format(url=url)

    def save_to_file(self, url, filename="output.html"):
        """
        Generate HTML and save to a file
        
        Args:
            url (str): The URL to include in the output
            filename (str): The name of the file to save (default: output.html)
        """
        html_content = self.generate_html(url)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def __call__(self, url):
        # Implementation for generating HTML from the given URL
        return f"Generated HTML for {url}"
