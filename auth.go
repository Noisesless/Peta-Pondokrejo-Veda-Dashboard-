package main

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/base64"
	"fmt"
	"net/http"
	"os"
	"strconv"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
)

const SessionCookieName = "pondokrejo_session"
const SessionDuration = 7 * 24 * time.Hour // 7 days

func getEnv(key, fallback string) string {
	if val := os.Getenv(key); val != "" {
		return val
	}
	return fallback
}

var (
	AdminUser     string
	AdminPassword string
	SessionSecret []byte
)

func init() {
	// Auto-load .env file if present in workspace/runtime directory
	loadEnvFile(".env")
	AdminUser = getEnv("ADMIN_USER", "admin")
	AdminPassword = getEnv("ADMIN_PASSWORD", "pondokrejo")
	SessionSecret = []byte(getEnv("SESSION_SECRET", "pondokrejo-secure-jwt-hmac-salt-tempel-2026"))
}

// loadEnvFile reads a key=value .env file and sets environment variables if not already set
func loadEnvFile(path string) {
	data, err := os.ReadFile(path)
	if err != nil {
		return
	}
	lines := strings.Split(string(data), "\n")
	for _, line := range lines {
		line = strings.TrimSpace(line)
		if line == "" || strings.HasPrefix(line, "#") {
			continue
		}
		parts := strings.SplitN(line, "=", 2)
		if len(parts) == 2 {
			k := strings.TrimSpace(parts[0])
			v := strings.TrimSpace(parts[1])
			v = strings.Trim(v, `"'`)
			if os.Getenv(k) == "" {
				_ = os.Setenv(k, v)
			}
		}
	}
}

// Generate signed session token: base64(username|exp|signature)
func createSessionToken(username string) string {
	exp := time.Now().Add(SessionDuration).Unix()
	payload := fmt.Sprintf("%s|%d", username, exp)
	mac := hmac.New(sha256.New, SessionSecret)
	mac.Write([]byte(payload))
	sig := mac.Sum(nil)
	tokenRaw := fmt.Sprintf("%s|%s", payload, base64.RawURLEncoding.EncodeToString(sig))
	return base64.RawURLEncoding.EncodeToString([]byte(tokenRaw))
}

// Verify signed session token and return username
func verifySessionToken(tokenStr string) (string, bool) {
	rawBytes, err := base64.RawURLEncoding.DecodeString(tokenStr)
	if err != nil {
		return "", false
	}
	parts := strings.Split(string(rawBytes), "|")
	if len(parts) != 3 {
		return "", false
	}

	username := parts[0]
	expStr := parts[1]
	sigB64 := parts[2]

	exp, err := strconv.ParseInt(expStr, 10, 64)
	if err != nil || time.Now().Unix() > exp {
		return "", false // Expired
	}

	expectedSig, err := base64.RawURLEncoding.DecodeString(sigB64)
	if err != nil {
		return "", false
	}

	payload := fmt.Sprintf("%s|%d", username, exp)
	mac := hmac.New(sha256.New, SessionSecret)
	mac.Write([]byte(payload))
	actualSig := mac.Sum(nil)

	if !hmac.Equal(actualSig, expectedSig) {
		return "", false
	}

	return username, true
}

// GetSessionUser checks cookie and returns username if valid session exists
func GetSessionUser(c *gin.Context) (string, bool) {
	cookie, err := c.Cookie(SessionCookieName)
	if err != nil || cookie == "" {
		return "", false
	}
	return verifySessionToken(cookie)
}

// IsAdmin returns true if current request has a valid admin session
func IsAdmin(c *gin.Context) bool {
	user, ok := GetSessionUser(c)
	return ok && user != ""
}

// RequireAdmin middleware blocks unauthenticated requests
func RequireAdmin() gin.HandlerFunc {
	return func(c *gin.Context) {
		if !IsAdmin(c) {
			// If JSON API or POST request, return 401 Unauthorized
			if strings.HasPrefix(c.Request.URL.Path, "/editor/save") ||
				strings.HasPrefix(c.Request.URL.Path, "/api/") ||
				c.GetHeader("Accept") == "application/json" {
				c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{
					"ok":    false,
					"error": "Akses ditolak: Diperlukan autentikasi administrator.",
				})
				return
			}
			// If HTML page (like /editor), redirect to login with return path
			redirectURL := "/login?redirect=" + c.Request.URL.Path
			c.Redirect(http.StatusFound, redirectURL)
			c.Abort()
			return
		}
		c.Next()
	}
}

// SetSessionCookie sets HttpOnly Secure session cookie
func SetSessionCookie(c *gin.Context, username string) {
	token := createSessionToken(username)
	maxAge := int(SessionDuration.Seconds())
	isSecure := c.Request.TLS != nil || c.GetHeader("X-Forwarded-Proto") == "https"
	c.SetCookie(SessionCookieName, token, maxAge, "/", "", isSecure, true)
}

// ClearSessionCookie clears the session cookie
func ClearSessionCookie(c *gin.Context) {
	isSecure := c.Request.TLS != nil || c.GetHeader("X-Forwarded-Proto") == "https"
	c.SetCookie(SessionCookieName, "", -1, "/", "", isSecure, true)
}

// MaskIdentifier masks 16-digit NIK or NoKK (UU PDP Compliance)
// e.g. 3404141811140007 -> 340414******0007
func MaskIdentifier(s string) string {
	s = strings.TrimSpace(s)
	if len(s) == 0 {
		return ""
	}
	if len(s) < 8 {
		return "******"
	}
	if len(s) == 16 {
		return s[:6] + "******" + s[12:]
	}
	// Fallback for different length strings
	p := len(s) / 4
	if p < 2 {
		p = 2
	}
	return s[:p] + "******" + s[len(s)-p:]
}

// MaskHouseholds returns a deep copy of households with masked PII
func MaskHouseholds(households []Household) []Household {
	out := make([]Household, len(households))
	for i, hh := range households {
		mHH := hh
		mHH.NoKK = MaskIdentifier(hh.NoKK)
		if len(hh.Members) > 0 {
			mMembers := make([]Resident, len(hh.Members))
			for j, m := range hh.Members {
				mM := m
				mM.Nik = MaskIdentifier(m.Nik)
				// Sanitize individual sensitive medical conditions for public view
				mM.Pregnant = ""
				mM.Disability = ""
				mMembers[j] = mM
			}
			mHH.Members = mMembers
		}
		out[i] = mHH
	}
	return out
}
