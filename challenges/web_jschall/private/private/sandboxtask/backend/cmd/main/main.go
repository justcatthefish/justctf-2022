package main

import (
	"backend/app"
	"backend/log"
	"github.com/fasthttp/router"
	"github.com/valyala/fasthttp"
	"net/http"
	"os"
)

func run() error {
	log.Log.Info("server starting")

	r := router.New()
	r.PanicHandler = func(ctx *fasthttp.RequestCtx, err interface{}) {
		log.Log.WithField("err", err).WithField("url", string(ctx.RequestURI())).Error("panic from http handler")
		ctx.Error("internal_error", http.StatusInternalServerError)
	}

	r.GET("/api/v1/comments", app.TimeoutMiddleware(app.UserMiddleware(app.HandleComments())))
	r.POST("/api/v1/add_comment", app.TimeoutMiddleware(app.UserMiddleware(app.HandleCommentAdd())))
	r.POST("/api/v1/report", app.TimeoutMiddleware(app.UserMiddleware(app.HandleMemeReport())))
	r.GET("/admin/api/v1/last_nickname", app.TimeoutMiddleware(app.UserMiddleware(app.HandleLastNickname())))

	s := &fasthttp.Server{
		Handler: r.Handler,
	}
	log.Log.Info("server started")

	return s.ListenAndServe(":8080")
}

func main() {
	if err := run(); err != nil {
		log.Log.WithError(err).Error("server closed with err")
		os.Exit(1)
	}
}
