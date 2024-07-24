package main

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

	
func main() {
	r := gin.Default()

	r.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "Hello from Go webservice!",
		})
	})

	r.Run(":9000")
}
