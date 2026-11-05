with open('D:/Project/peta_pondokrejo_main/main.go', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    '//go:embed *.png *.JPG PONDOKREJO.geojson *.md residents.json',
    '//go:embed *.png *.JPG *.jpg PONDOKREJO.geojson *.md residents.json'
)

bg_route = '''\tr.GET("/background.jpg", func(c *gin.Context) {
\t\tdata, err := assetsFS.ReadFile("background.JPG")
\t\tif err != nil {
\t\t\tc.String(http.StatusNotFound, "File not found")
\t\t\treturn
\t\t}
\t\tc.Data(http.StatusOK, "image/jpeg", data)
\t})'''

bg_and_login = '''\tr.GET("/background.jpg", func(c *gin.Context) {
\t\tdata, err := assetsFS.ReadFile("background.JPG")
\t\tif err != nil {
\t\t\tc.String(http.StatusNotFound, "File not found")
\t\t\treturn
\t\t}
\t\tc.Data(http.StatusOK, "image/jpeg", data)
\t})
\tr.GET("/login.jpg", func(c *gin.Context) {
\t\tdata, err := assetsFS.ReadFile("login.jpg")
\t\tif err != nil {
\t\t\tc.String(http.StatusNotFound, "File not found")
\t\t\treturn
\t\t}
\t\tc.Data(http.StatusOK, "image/jpeg", data)
\t})'''

content = content.replace(bg_route, bg_and_login)

with open('D:/Project/peta_pondokrejo_main/main.go', 'w', encoding='utf-8') as f:
    f.write(content)

print("Embedded login.jpg added and route registered!")

