package main

import (
	"fmt"
	"net/http"
	sentry "github.com/getsentry/sentry-go"
	sentrygin "github.com/getsentry/sentry-go/gin"
	"github.com/gin-gonic/gin"
)

func main() {
	if err := sentry.Init(sentry.ClientOptions{
		Dsn: "https://f1f3cf970c53209eb9db77fbc0414236@o447951.ingest.us.sentry.io/4507606077210624", // sentry-go-gin
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