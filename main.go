package main

import (
	"embed"
	"encoding/json"
	"flag"
	"fmt"
	"html/template"
	"io/fs"
	"log"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
)

//go:embed templates/*
var templateFS embed.FS

//go:embed layers/*
var layersFS embed.FS

//go:embed *.png *.JPG *.jpg PONDOKREJO.geojson *.md residents.json
var assetsFS embed.FS

func main() {
	// Parse CLI flags
	genStatic := flag.Bool("gen", false, "Generate static JSON files for deployment")
	clipGeoJSON := flag.String("clip-geojson", "", "Clip input GeoJSON to Pondokrejo boundary and write output")
	clipOut := flag.String("clip-out", "", "Output GeoJSON file path for -clip-geojson")
	clipBoundary := flag.String("clip-boundary", "DEFAULT_VIEW", "Boundary GeoJSON file for -clip-geojson")
	flag.Parse()

	if *clipGeoJSON != "" {
		if err := ClipGeoJSONToPondokrejoBoundary(*clipGeoJSON, *clipBoundary, *clipOut); err != nil {
			log.Fatalf("Error clipping geojson: %v", err)
		}
		fmt.Println("Clipped GeoJSON written successfully")
		return
	}

	// Parse Data (Excel or Embedded JSON)
	var households []Household
	var err error

	jsonFile := "residents.json"
	excelFile := "1 KK_ART Pondokrejo.xlsx"

	// 1. Prioritize pre-normalized residents.json if exists
	if _, statErr := os.Stat(jsonFile); statErr == nil {
		fmt.Println("Loading from normalized residents.json...")
		if data, readErr := os.ReadFile(jsonFile); readErr == nil {
			if jsonErr := json.Unmarshal(data, &households); jsonErr == nil && len(households) > 0 {
				fmt.Printf("Loaded %d households from %s\n", len(households), jsonFile)
			}
		}
	}

	// 2. Fallback to Excel parsing if residents.json not found
	if len(households) == 0 {
		if _, statErr := os.Stat(excelFile); statErr == nil {
			fmt.Println("Loading from Excel...")
			households, err = ParseExcel(excelFile)
			if err != nil {
				log.Fatalf("Error parsing excel: %v", err)
			}
		} else if len(EmbeddedResidentsData) > 0 {
			fmt.Println("Excel not found. Loading from embedded residents.json...")
			if err := json.Unmarshal(EmbeddedResidentsData, &households); err != nil {
				log.Fatalf("Error unmarshaling embedded residents.json: %v", err)
			}
		} else {
			log.Fatalf("Error: No data file found")
		}
	}

	editorStore := NewEditorStore("editor_state.json")
	if err := editorStore.Load(); err != nil {
		log.Fatalf("Error loading editor state: %v", err)
	}

	// Generate Static Files Mode
	if *genStatic {
		fmt.Println("Generating static files...")

		// 1. residents.json
		jsonData, err := json.MarshalIndent(households, "", "  ")
		if err != nil {
			log.Fatal(err)
		}
		if err := os.WriteFile("residents.json", jsonData, 0644); err != nil {
			log.Fatal(err)
		}
		fmt.Println("Created residents.json")

		// 2. boundary.geojson (Copy)
		boundaryData, err := os.ReadFile("PONDOKREJO.geojson")
		if err != nil {
			log.Printf("Warning: Could not read PONDOKREJO.geojson: %v", err)
		} else {
			if err := os.WriteFile("boundary.geojson", boundaryData, 0644); err != nil {
				log.Fatal(err)
			}
			fmt.Println("Created boundary.geojson")
		}

		fmt.Println("Static build complete. You can now upload 'index.html', 'residents.json', and 'boundary.geojson' to a static host.")
		return
	}

	// Server Mode
	r := gin.Default()

	// Load HTML templates from embed.FS
	templ := template.Must(template.New("").ParseFS(templateFS, "templates/*.html"))
	r.SetHTMLTemplate(templ)

	// Routes (LOGIN REQUIRED - Proteksi Penuh)
	r.GET("/", RequireAdmin(), func(c *gin.Context) {
		c.HTML(http.StatusOK, "index.html", nil)
	})

	r.GET("/login", func(c *gin.Context) {
		if IsAdmin(c) {
			c.Redirect(http.StatusFound, "/")
			return
		}
		c.HTML(http.StatusOK, "login.html", nil)
	})

	// Authentication API
	type LoginRequest struct {
		Username string `json:"username" form:"username"`
		Password string `json:"password" form:"password"`
	}

	r.POST("/api/login", func(c *gin.Context) {
		var req LoginRequest
		if err := c.ShouldBind(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"ok": false, "error": "Format permintaan tidak valid"})
			return
		}
		if req.Username == AdminUser && req.Password == AdminPassword {
			SetSessionCookie(c, req.Username)
			c.JSON(http.StatusOK, gin.H{
				"ok":      true,
				"message": "Login berhasil",
				"user":    req.Username,
			})
			return
		}
		c.JSON(http.StatusUnauthorized, gin.H{
			"ok":    false,
			"error": "Username atau password salah",
		})
	})

	r.GET("/logout", func(c *gin.Context) {
		ClearSessionCookie(c)
		c.Redirect(http.StatusFound, "/login")
	})

	r.POST("/api/logout", func(c *gin.Context) {
		ClearSessionCookie(c)
		c.JSON(http.StatusOK, gin.H{"ok": true})
	})

	r.GET("/api/auth/status", func(c *gin.Context) {
		user, ok := GetSessionUser(c)
		c.JSON(http.StatusOK, gin.H{
			"is_authenticated": ok,
			"username":         user,
		})
	})

	// Protected Editor Routes (RequireAdmin middleware)
	r.GET("/editor", RequireAdmin(), func(c *gin.Context) {
		c.HTML(http.StatusOK, "editor.html", nil)
	})

	r.GET("/editor/layers", RequireAdmin(), func(c *gin.Context) {
		c.JSON(http.StatusOK, editorStore.GeoLayersSnapshot())
	})

	r.GET("/editor/layers/:name", func(c *gin.Context) {
		name := c.Param("name")
		if name == "" {
			c.Data(http.StatusOK, "application/json", []byte(`{"type":"FeatureCollection","features":[]}`))
			return
		}
		if raw, ok := editorStore.GeoLayer(name); ok {
			c.Data(http.StatusOK, "application/json", raw)
			return
		}
		c.Data(http.StatusOK, "application/json", []byte(`{"type":"FeatureCollection","features":[]}`))
	})

	// Serve residents.json (RequireAdmin: Hanya untuk Petugas Terautentikasi)
	r.GET("/residents.json", RequireAdmin(), func(c *gin.Context) {
		c.JSON(http.StatusOK, editorStore.Apply(households))
	})

	// Protected Editor Mutation Endpoint
	r.POST("/editor/save", RequireAdmin(), func(c *gin.Context) {
		var req EditorSaveRequest
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"ok": false, "error": err.Error()})
			return
		}
		if err := editorStore.UpdateAndSave(req); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"ok": false, "error": err.Error()})
			return
		}
		c.JSON(http.StatusOK, gin.H{"ok": true})
	})

	// Serve boundary.geojson from embedded assets
	r.GET("/boundary.geojson", func(c *gin.Context) {
		data, err := assetsFS.ReadFile("PONDOKREJO.geojson")
		if err != nil {
			c.String(http.StatusNotFound, "File not found")
			return
		}
		c.Data(http.StatusOK, "application/json", data)
	})

	// Serve Layers (GeoJSON) from embedded layersFS
	layersSub, _ := fs.Sub(layersFS, "layers")
	r.StaticFS("/layers", http.FS(layersSub))

	// Serve Images from embedded assetsFS
	r.GET("/logo.png", func(c *gin.Context) {
		data, err := assetsFS.ReadFile("logo.png")
		if err != nil {
			c.String(http.StatusNotFound, "File not found")
			return
		}
		c.Data(http.StatusOK, "image/png", data)
	})
	r.GET("/veda-logo.png", func(c *gin.Context) {
		data, err := assetsFS.ReadFile("veda-logo.png")
		if err != nil {
			c.String(http.StatusNotFound, "File not found")
			return
		}
		c.Data(http.StatusOK, "image/png", data)
	})
	r.GET("/clasnet-logo.png", func(c *gin.Context) {
		data, err := assetsFS.ReadFile("clasnet-logo.png")
		if err != nil {
			c.String(http.StatusNotFound, "File not found")
			return
		}
		c.Data(http.StatusOK, "image/png", data)
	})
	r.GET("/background.jpg", func(c *gin.Context) {
		data, err := assetsFS.ReadFile("background.JPG")
		if err != nil {
			c.String(http.StatusNotFound, "File not found")
			return
		}
		c.Data(http.StatusOK, "image/jpeg", data)
	})
	r.GET("/background.JPG", func(c *gin.Context) {
		data, err := assetsFS.ReadFile("background.JPG")
		if err != nil {
			c.String(http.StatusNotFound, "File not found")
			return
		}
		c.Data(http.StatusOK, "image/jpeg", data)
	})
	r.GET("/login.jpg", func(c *gin.Context) {
		data, err := assetsFS.ReadFile("login.jpg")
		if err != nil {
			c.String(http.StatusNotFound, "File not found")
			return
		}
		c.Data(http.StatusOK, "image/jpeg", data)
	})

	// Recommendations Page
	r.GET("/recommendations", RequireAdmin(), func(c *gin.Context) {
		rek, err1 := assetsFS.ReadFile("rekomendasi-hasil-analitik.md")
		if err1 != nil {
			rek = []byte("# Error loading recommendation file")
		}

		act, err2 := assetsFS.ReadFile("action-plan.md")
		if err2 != nil {
			act = []byte("# Error loading action plan file")
		}

		gis, err3 := assetsFS.ReadFile("gis-desa.md")
		if err3 != nil {
			gis = []byte("# Error loading GIS file")
		}

		c.HTML(http.StatusOK, "recommendations.html", gin.H{
			"Rekomendasi": string(rek),
			"ActionPlan":  string(act),
			"GISDesa":     string(gis),
		})
	})

	// Analytics Dashboard Page
	r.GET("/analytics", RequireAdmin(), func(c *gin.Context) {
		// Calculate on the fly (or cache it)
		data := CalculateAnalytics(households)

		// Convert to JSON for injection
		jsonData, err := json.Marshal(data)
		if err != nil {
			c.String(http.StatusInternalServerError, "Error processing data")
			return
		}

		c.HTML(http.StatusOK, "analytics.html", gin.H{
			"AnalyticsData": string(jsonData),
		})
	})

	// Bansos Dashboard Page
	r.GET("/bansos", RequireAdmin(), func(c *gin.Context) {
		data := CalculateBansos(households)
		jsonData, err := json.Marshal(data)
		if err != nil {
			c.String(http.StatusInternalServerError, "Error processing bansos data")
			return
		}
		c.HTML(http.StatusOK, "bansos.html", gin.H{
			"BansosData": string(jsonData),
		})
	})

	// Bansos JSON API
	r.GET("/bansos/data", RequireAdmin(), func(c *gin.Context) {
		data := CalculateBansos(households)
		c.JSON(http.StatusOK, data)
	})

	// Start server
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	log.Println("Server starting on :" + port)
	if err := r.Run(":" + port); err != nil {
		log.Fatal(err)
	}
}
