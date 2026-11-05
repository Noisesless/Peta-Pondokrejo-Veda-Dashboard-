import re

with open('D:/Project/peta_pondokrejo_main/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace client-side redirect script with session sync
pattern_script = r'<script>\s*// Simple Client-side Auth Check[\s\S]*?window\.location\.href = \'/login\';\s*\}\s*</script>'
repl_script = """<script>
        // Sync sessionStorage with server auth status
        fetch('/api/auth/status')
            .then(res => res.json())
            .then(data => {
                if (data.is_authenticated) {
                    sessionStorage.setItem('isLoggedIn', 'true');
                } else {
                    sessionStorage.removeItem('isLoggedIn');
                }
            })
            .catch(() => {});
    </script>"""

# Replace top bar actions
pattern_topbar = r'<div class="flex items-center pr-4 space-x-2">[\s\S]*?<a href="/editor"[\s\S]*?</div>\s*</div>'
repl_topbar = """<div class="flex items-center pr-4 space-x-2">
            {{if .IsAdmin}}
                <span class="hidden md:inline-flex bg-blue-900/60 text-white text-xs px-2.5 py-1 rounded border border-blue-400/40 mr-1 items-center">
                    <i class="fa fa-user-shield mr-1.5 text-emerald-300"></i> Mode Petugas (Data Lengkap)
                </span>
                <a href="/editor" class="bg-slate-100 hover:bg-white text-blue-800 font-bold py-1 px-3 rounded text-sm shadow transition">
                    <i class="fa fa-pen-to-square mr-1"></i> Editor
                </a>
            {{else}}
                <span class="hidden md:inline-flex bg-blue-900/40 text-blue-100 text-xs px-2.5 py-1 rounded border border-blue-400/30 mr-1 items-center" title="Data NIK & No KK disamarkan sesuai UU Perlindungan Data Pribadi (UU PDP)">
                    <i class="fa fa-shield-halved mr-1.5 text-blue-300"></i> Mode Publik (Data Disensor)
                </span>
                <a href="/login?redirect=/" class="bg-blue-600 hover:bg-blue-500 text-white font-bold py-1 px-3 rounded text-sm shadow transition">
                    <i class="fa fa-arrow-right-to-bracket mr-1"></i> Masuk Petugas
                </a>
            {{end}}
            <a href="/bansos" target="_blank" class="bg-green-500 hover:bg-green-400 text-white font-bold py-1 px-3 rounded text-sm shadow transition">
                <i class="fa fa-hand-holding-heart mr-1"></i> Bansos
            </a>
            <a href="/analytics" target="_blank" class="bg-indigo-500 hover:bg-indigo-400 text-white font-bold py-1 px-3 rounded text-sm shadow transition">
                <i class="fa fa-chart-bar mr-1"></i> Analitik
            </a>
            {{if .IsAdmin}}
                <a href="/logout" onclick="sessionStorage.removeItem('isLoggedIn');" class="bg-red-600 hover:bg-red-700 text-white font-bold py-1 px-3 rounded text-sm shadow transition">
                    <i class="fa fa-sign-out-alt mr-1"></i> Keluar
                </a>
            {{end}}
        </div>
    </div>"""

if re.search(pattern_script, content):
    content = re.sub(pattern_script, repl_script, content, count=1)
    print("Script replaced successfully")
else:
    print("Script pattern NOT found")

if re.search(pattern_topbar, content):
    content = re.sub(pattern_topbar, repl_topbar, content, count=1)
    print("Topbar replaced successfully")
else:
    print("Topbar pattern NOT found")

with open('D:/Project/peta_pondokrejo_main/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

