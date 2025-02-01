from IPython.display import HTML, Image
import pandas as pd
class DisplayUtil:
    def __init__(self):
        pass

    def display(self, data):
        if isinstance(data, pd.DataFrame):
            # Basic CSS styling
            style = """
            <style>
                .table {
                    width: 100%;
                    margin-bottom: 1rem;
                    color: #212529;
                    border-collapse: collapse;
                }
                .table-striped tbody tr:nth-of-type(odd) {
                    background-color: rgba(0,0,0,.05);
                }
                .table-bordered {
                    border: 1px solid #dee2e6;
                }
                .table th, .table td {
                    padding: 0.75rem;
                    border: 1px solid #dee2e6;
                }
                .table thead th {
                    background-color: #f8f9fa;
                    border-bottom: 2px solid #dee2e6;
                }
            </style>
            """
            
            html_table = data.to_html(
                classes='table table-striped table-bordered',
                index=False,
                float_format=lambda x: '{:.2f}'.format(x) if isinstance(x, float) else x
            )
            return style + html_table
        
        elif isinstance(data, Image):
            html_img = f"""
            <style>
                .responsive-img {{
                    max-width: 100%;
                    height: auto;
                    display: block;
                    margin: 0 auto;
                }}
            </style>
            <img src="{data.url}" class="responsive-img" alt="Generated Image">
            """
            return html_img

        elif isinstance(data, (dict, list)):
            # JSON styling
            style = """
            <style>
                .json-container {
                    font-family: monospace;
                    background-color: #f8f9fa;
                    padding: 1rem;
                    border-radius: 4px;
                    border: 1px solid #dee2e6;
                }
                .json-key {
                    color: #d63384;
                }
                .json-string {
                    color: #198754;
                }
                .json-number {
                    color: #0d6efd;
                }
                .json-boolean {
                    color: #dc3545;
                }
                .json-null {
                    color: #6c757d;
                }
            </style>
            """

            html_json = f"""
            <div class="json-container">
                <pre>{self.json_to_html(data)}</pre>
            </div>
            """
            return style + html_json
        else:
            return "<p>Not a valid DataFrame or Image object</p>"

    def json_to_html(self, data, indent=0):
        padding = '    ' * indent
        
        if isinstance(data, dict):
            if not data:
                return '{}'
            lines = ['{\n']
            items = list(data.items())
            for i, (key, value) in enumerate(items):
                lines.append(f'{padding}    <span class="json-key">"{key}"</span>: {self.json_to_html(value, indent + 1)}')
                if i < len(items) - 1:
                    lines[-1] += ','
                lines[-1] += '\n'
            lines.append(f'{padding}}}')
            return ''.join(lines)
            
        elif isinstance(data, list):
            if not data:
                return '[]'
            lines = ['[\n']
            for i, item in enumerate(data):
                lines.append(f'{padding}    {self.json_to_html(item, indent + 1)}')
                if i < len(data) - 1:
                    lines[-1] += ','
                lines[-1] += '\n'
            lines.append(f'{padding}]')
            return ''.join(lines)
            
        elif isinstance(data, str):
            return f'<span class="json-string">"{data}"</span>'
        elif isinstance(data, (int, float)):
            return f'<span class="json-number">{data}</span>'
        elif isinstance(data, bool):
            return f'<span class="json-boolean">{str(data).lower()}</span>'
        elif data is None:
            return f'<span class="json-null">null</span>'
        else:
            return str(data)
