import os
import re
import sys
from pathlib import Path
from datetime import datetime

def get_title_from_md(md_file):
    """Extract title from markdown file (first # heading)"""
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if match:
                return match.group(1)
            return os.path.basename(md_file)[:-3]  # Fallback to filename without .md
    except Exception as e:
        print(f"Error reading {md_file}: {e}", file=sys.stderr)
        return os.path.basename(md_file)[:-3]

def get_date_from_md(md_file):
    """Extract date from markdown frontmatter"""
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Simple frontmatter date extraction
            match = re.search(r'---\s*\ndate:\s*(\d{4}-\d{2}-\d{2})', content)
            if match:
                return datetime.strptime(match.group(1), '%Y-%m-%d')

            # Fallback to file modification time
            return datetime.fromtimestamp(os.path.getmtime(md_file))
    except Exception as e:
        print(f"Error getting date for {md_file}: {e}", file=sys.stderr)
        return datetime.now()

def create_index_html(markdown_files, output_dir):
    """Create index.html file listing all comment pages"""

    # Sort files by date (newest first)
    sorted_files = sorted(
        [(f, get_date_from_md(f), get_title_from_md(f)) for f in markdown_files if not f.name.startswith('_')],
        key=lambda x: x[1],
        reverse=True
    )

    html_content = """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Comments - Elozor's Blog</title>
        <link rel="stylesheet" href="/smol.css">
    </head>
    <body id="blog">
        <header class="text-center">
            <h1 class="text-2xl font-bold mt-2">Comments - Elozor's Blog</h1>
            <span>Comment pages for blog posts</span>
            <hr />
        </header>
        <main>
            <section class="posts group mt-2">"""

    for md_file, date, title in sorted_files:
        html_content += f"""
                <article>
                    <div class="flex items-center">
                        <time datetime="{date.strftime('%Y-%m-%dT00:00:00Z')}" class="text-sm post-date">{date.strftime('%Y-%m-%d')}</time>
                        <span class="text-md flex-1 m-0 transform-none">
                            <a href="/{md_file.stem}.html">{title}</a>
                        </span>
                    </div>
                </article>"""

    html_content += """
            </section>
        </main>
        <footer>
            <hr />
            <p><a href="https://blog.ebruce.dev">← Back to blog</a></p>
        </footer>
    </body>
</html>"""

    try:
        index_file = Path(output_dir) / 'index.html'
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        os.system(f'chown www-data:www-data "{index_file}"')
        print(f"Created {index_file}")
    except Exception as e:
        print(f"Error creating index.html: {e}", file=sys.stderr)

def create_comments_html(md_file, output_dir):
    """Create HTML file with comments section for a markdown file"""
    title = get_title_from_md(md_file)
    output_file = Path(output_dir) / f"{Path(md_file).stem}.html"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comments for {title}</title>
    <link rel="stylesheet" href="/smol.css">
</head>
<body>
    <header class="text-center">
        <h1 class="text-2xl font-bold">{title}</h1>
    </header>
    <p><a href="https://blog.ebruce.dev/{md_file.stem}">&larr; Back to content</a></p>
    <script src="https://giscus.app/client.js"
        data-repo="coolcoder613eb/blog"
        data-repo-id="R_kgDONmVM8w"
        data-category="Announcements"
        data-category-id="DIC_kwDONmVM884Clv4l"
        data-mapping="pathname"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="bottom"
        data-theme="preferred_color_scheme"
        data-lang="en"
        crossorigin="anonymous"
        async>
    </script>
</body>
</html>"""

    try:
        os.makedirs(output_dir, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        os.system(f'chown www-data:www-data "{output_file}"')
        print(f"Created {output_file}")
    except Exception as e:
        print(f"Error creating {output_file}: {e}", file=sys.stderr)

def process_markdown_files(input_dir, output_dir):
    """Process all markdown files in input_dir and create comment pages in output_dir"""
    try:
        input_path = Path(input_dir)
        if not input_path.exists():
            raise FileNotFoundError(f"Input directory {input_dir} does not exist")

        # Ensure output directory exists and set ownership
        os.makedirs(output_dir, exist_ok=True)
        os.system(f'chown www-data:www-data "{output_dir}"')

        # Collect markdown files
        markdown_files = [f for f in input_path.glob('*.md') if not f.name.startswith('_')]

        # Create index page
        create_index_html(markdown_files, output_dir)

        # Create individual comment pages
        count = 0
        for md_file in markdown_files:
            create_comments_html(md_file, output_dir)
            count += 1

        print(f"Successfully processed {count} markdown files")

    except Exception as e:
        print(f"Error processing markdown files: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    # Example usage
    input_directory = '.'  # Directory containing markdown files
    output_directory = '/var/www/html/comments.ebruce.dev'  # Directory for comment HTML files

    # Check if running as root (needed for chown)
    if os.geteuid() != 0:
        print("This script needs to be run as root to set proper ownership", file=sys.stderr)
        sys.exit(1)

    process_markdown_files(input_directory, output_directory)
