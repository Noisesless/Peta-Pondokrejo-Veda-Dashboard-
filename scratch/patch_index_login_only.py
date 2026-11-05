import re

with open('D:/Project/peta_pondokrejo_main/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

pattern_script = r'<script>\s*// Sync sessionStorage with server auth status[\s\S]*?</script>'
repl_script = """<script>
        // Double Protection: Alihkan langsung ke /login jika tidak ada sesi login
        if (sessionStorage.getItem('isLoggedIn') !== 'true') {
            window.location.href = '/login';
        }
    </script>"""

pattern_topbar = r'<div class="flex items-center pr-4 space-x-2">[\s\S]*?</div>\s*</div>'
repl_topbar = """<div class="flex items-center pr-4 space-x-2">
            <a href="/editor" class="bg-slate-100 hover:bg-white text-blue-800 font-bold py-1 px-3 rounded text-sm shadow transition">
                <i class="fa fa-pen-to-square mr-1"></i> Editor
            </a>
            <a href="/bansos" target="_blank" class="bg-green-500 hover:bg-green-400 text-white font-bold py-1 px-3 rounded text-sm shadow transition">
                <i class="fa fa-hand-holding-heart mr-1"></i> Bansos
            </a>
            <a href="/analytics" target="_blank" class="bg-indigo-500 hover:bg-indigo-400 text-white font-bold py-1 px-3 rounded text-sm shadow transition">
                <i class="fa fa-chart-bar mr-1"></i> Analitik
            </a>
            <a href="/logout" onclick="sessionStorage.removeItem('isLoggedIn');" class="bg-red-600 hover:bg-red-700 text-white font-bold py-1 px-3 rounded text-sm shadow transition">
                <i class="fa fa-sign-out-alt mr-1"></i> Logout
            </a>
        </div>
    </div>"""

if re.search(pattern_script, content):
    content = re.sub(pattern_script, repl_script, content, count=1)
    print("Script restored to strict login-only check")
else:
    print("Script pattern NOT found")

if re.search(pattern_topbar, content):
    content = re.sub(pattern_topbar, repl_topbar, content, count=1)
    print("Topbar restored to clean officer layout")
else:
    print("Topbar pattern NOT found")

with open('D:/Project/peta_pondokrejo_main/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

