import re

with open('D:/Project/peta_pondokrejo_main/main.go', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern matching routes block
pattern = r'(\t// Routes\r?\n\tr\.GET\("/", func\(c \*gin\.Context\) \{\r?\n\t\tc\.HTML\(http\.StatusOK, "index\.html", nil\)\r?\n\t\}\)[\s\S]*?r\.POST\("/editor/save"[\s\S]*?\t\}\))'

replacement = """\t// Routes
\tr.GET("/", func(c *gin.Context) {
\t\tc.HTML(http.StatusOK, "index.html", gin.H{
\t\t\t"IsAdmin": IsAdmin(c),
\t\t})
\t})

\tr.GET("/login", func(c *gin.Context) {
\t\tif IsAdmin(c) {
\t\t\tc.Redirect(http.StatusFound, "/")
\t\t\treturn
\t\t}
\t\tc.HTML(http.StatusOK, "login.html", nil)
\t})

\t// Authentication API
\ttype LoginRequest struct {
\t\tUsername string `json:"username" form:"username"`
\t\tPassword string `json:"password" form:"password"`
\t}

\tr.POST("/api/login", func(c *gin.Context) {
\t\tvar req LoginRequest
\t\tif err := c.ShouldBind(&req); err != nil {
\t\t\tc.JSON(http.StatusBadRequest, gin.H{"ok": false, "error": "Format permintaan tidak valid"})
\t\t\treturn
\t\t}
\t\tif req.Username == AdminUser && req.Password == AdminPassword {
\t\t\tSetSessionCookie(c, req.Username)
\t\t\tc.JSON(http.StatusOK, gin.H{
\t\t\t\t"ok":      true,
\t\t\t\t"message": "Login berhasil",
\t\t\t\t"user":    req.Username,
\t\t\t})
\t\t\treturn
\t\t}
\t\tc.JSON(http.StatusUnauthorized, gin.H{
\t\t\t"ok":    false,
\t\t\t"error": "Username atau password salah",
\t\t})
\t})

\tr.GET("/logout", func(c *gin.Context) {
\t\tClearSessionCookie(c)
\t\tc.Redirect(http.StatusFound, "/login")
\t})

\tr.POST("/api/logout", func(c *gin.Context) {
\t\tClearSessionCookie(c)
\t\tc.JSON(http.StatusOK, gin.H{"ok": true})
\t})

\tr.GET("/api/auth/status", func(c *gin.Context) {
\t\tuser, ok := GetSessionUser(c)
\t\tc.JSON(http.StatusOK, gin.H{
\t\t\t"is_authenticated": ok,
\t\t\t"username":         user,
\t\t})
\t})

\t// Protected Editor Routes (RequireAdmin middleware)
\tr.GET("/editor", RequireAdmin(), func(c *gin.Context) {
\t\tc.HTML(http.StatusOK, "editor.html", nil)
\t})

\tr.GET("/editor/layers", RequireAdmin(), func(c *gin.Context) {
\t\tc.JSON(http.StatusOK, editorStore.GeoLayersSnapshot())
\t})

\tr.GET("/editor/layers/:name", RequireAdmin(), func(c *gin.Context) {
\t\tname := c.Param("name")
\t\tif name == "" {
\t\t\tc.Data(http.StatusOK, "application/json", []byte(`{"type":"FeatureCollection","features":[]}`))
\t\t\treturn
\t\t}
\t\tif raw, ok := editorStore.GeoLayer(name); ok {
\t\t\tc.Data(http.StatusOK, "application/json", raw)
\t\t\treturn
\t\t}
\t\tc.Data(http.StatusOK, "application/json", []byte(`{"type":"FeatureCollection","features":[]}`))
\t})

\t// Serve residents.json dynamically (PII Masking for Public / Unmasked for Authenticated Admin)
\tr.GET("/residents.json", func(c *gin.Context) {
\t\tapplied := editorStore.Apply(households)
\t\tif IsAdmin(c) {
\t\t\t// Authenticated Admin receives full 16-digit unmasked records
\t\t\tc.JSON(http.StatusOK, applied)
\t\t\treturn
\t\t}
\t\t// Public visitors receive masked PII (UU PDP No. 27/2022 & SP-025 Compliance)
\t\tc.JSON(http.StatusOK, MaskHouseholds(applied))
\t})

\t// Protected Editor Mutation Endpoint
\tr.POST("/editor/save", RequireAdmin(), func(c *gin.Context) {
\t\tvar req EditorSaveRequest
\t\tif err := c.ShouldBindJSON(&req); err != nil {
\t\t\tc.JSON(http.StatusBadRequest, gin.H{"ok": false, "error": err.Error()})
\t\t\treturn
\t\t}
\t\tif err := editorStore.UpdateAndSave(req); err != nil {
\t\t\tc.JSON(http.StatusInternalServerError, gin.H{"ok": false, "error": err.Error()})
\t\t\treturn
\t\t}
\t\tc.JSON(http.StatusOK, gin.H{"ok": true})
\t})"""

# Match and replace
if re.search(pattern, content):
    new_content = re.sub(pattern, replacement, content, count=1)
    with open('D:/Project/peta_pondokrejo_main/main.go', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully patched main.go!")
else:
    print("Pattern not matched!")

