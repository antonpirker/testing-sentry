package main

import (
	"os"
	"fmt"
	"net/http"
	sentry "github.com/getsentry/sentry-go"
	sentrygin "github.com/getsentry/sentry-go/gin"
	"github.com/gin-gonic/gin"
)

func main() {
	if err := sentry.Init(sentry.ClientOptions{
		Dsn: os.Getenv("SENTRY_DSN"),
		EnableTracing: true,
		// Set TracesSampleRate to 1.0 to capture 100%
		// of transactions for tracing.
		// We recommend adjusting this value in production,
		TracesSampleRate: 1.0,
		Environment: "potel",
		Debug: true,
	}); err != nil {
		fmt.Printf("Sentry initialization failed: %v\n", err)
	}

	app := gin.Default()

	app.Use(sentrygin.New(sentrygin.Options{}))

	app.GET("/", func(c *gin.Context) {
		// transaction := sentry.TransactionFromContext(c)
		// span := sentry.StartSpan(transaction.Context(), "function")
		// span.Description = "test-span"
		// span.Finish()

		c.JSON(http.StatusOK, gin.H{
			"content": "Go (webservice)",
		})
	})

	app.Run(":9000")
}