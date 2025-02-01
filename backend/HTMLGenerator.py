class HTMLGenerator:
    def __init__(self):
        self.base_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f0f0f0;
        }
        .greeting {
            padding: 20px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
    </style>
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
