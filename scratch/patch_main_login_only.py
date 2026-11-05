with open('D:/Project/peta_pondokrejo_main/main.go', 'r', encoding='utf-8') as f:
    content = f.read()

# Make / require login
content = content.replace(
'''	// Routes
	r.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index.html", gin.H{
			"IsAdmin": IsAdmin(c),
		})
	})''',
'''	// Routes (LOGIN REQUIRED - Proteksi Penuh)
	r.GET("/", RequireAdmin(), func(c *gin.Context) {
		c.HTML(http.StatusOK, "index.html", nil)
	})'''
)

# Make /residents.json require admin directly and serve full data fast
old_residents = '''	// Serve residents.json dynamically (PII Masking for Public / Unmasked for Authenticated Admin)
	r.GET("/residents.json", func(c *gin.Context) {
		applied := editorStore.Apply(households)
		if IsAdmin(c) {
			// Authenticated Admin receives full 16-digit unmasked records
			c.JSON(http.StatusOK, applied)
			return
		}
		// Public visitors receive masked PII (UU PDP No. 27/2022 & SP-025 Compliance)
		c.JSON(http.StatusOK, MaskHouseholds(applied))
	})'''

new_residents = '''	// Serve residents.json (RequireAdmin: Hanya untuk Petugas Terautentikasi)
	r.GET("/residents.json", RequireAdmin(), func(c *gin.Context) {
		c.JSON(http.StatusOK, editorStore.Apply(households))
	})'''

content = content.replace(old_residents, new_residents)

# Also protect analytics, bansos, recommendations
content = content.replace('r.GET("/analytics", func(c *gin.Context) {', 'r.GET("/analytics", RequireAdmin(), func(c *gin.Context) {')
content = content.replace('r.GET("/bansos", func(c *gin.Context) {', 'r.GET("/bansos", RequireAdmin(), func(c *gin.Context) {')
content = content.replace('r.GET("/bansos/data", func(c *gin.Context) {', 'r.GET("/bansos/data", RequireAdmin(), func(c *gin.Context) {')
content = content.replace('r.GET("/recommendations", func(c *gin.Context) {', 'r.GET("/recommendations", RequireAdmin(), func(c *gin.Context) {')

with open('D:/Project/peta_pondokrejo_main/main.go', 'w', encoding='utf-8') as f:
    f.write(content)

print("main.go updated to strictly require login on all pages!")

