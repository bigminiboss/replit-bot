"""Some html templates. Will convert to jina and add to replit-bot/templates/ later"""

ORIGINAL_HTML = """<center><h1>Commands are as followed</h1></center>
<pre><code>@{} {}command-here param1:here param2:here</code></pre>
<hr><center><h1>Commands</h1></center>{}<hr>"""

HTML_LIST = """<li>{}</li>
<ul>
    <li>Description: <em style="color: red; background: black">{}</em></li>
    <li>required = {}</li>
    <li>default = {}</li>
    <li>type = {}</li>
</ul>"""

PARAM_BIO = """<center><h2>{}{}</h2></center>{}"""

BLOCKQUOTE = """<blockquote>{}</blockquote>"""

TEMPLATE = """<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/dark.css">

{{html|safe}}

<center><h5>made with ❤️ by <a href="https://replit.com/@bigminiboss">@bigminiboss</a> on replit && webpage powered by <a href="https://watercss.kognise.dev/">water.css</a></h5></center>
<center><h6>fork <a href="https://replit.com/@bigminiboss/replit-bot">me</a> on replit</h6></center>"""
