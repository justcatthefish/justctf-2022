package app

import (
	"encoding/json"
	"github.com/valyala/fasthttp"
	"backend/log"
)

var lastComment Comment
var dbComments []Comment

func init() {
	dbComments = make([]Comment, 0, 100)
}

type Comment struct {
	ID       int    `json:"id"`
	Nickname string `json:"nickname"`
	Message  string `json:"comment"`
}

func HandleComments() fasthttp.RequestHandler {
	return func(ctx *fasthttp.RequestCtx) {
		SendData(ctx, dbComments)
	}
}

func HandleCommentAdd() fasthttp.RequestHandler {
	type request struct {
		Nickname string `json:"nickname"`
		Comment  string `json:"comment"`
	}

	return func(ctx *fasthttp.RequestCtx) {
		var v request
		if err := json.Unmarshal(ctx.Request.Body(), &v); err != nil {
			// invalid json
			ctx.SetStatusCode(400)
			return
		}

		if len(v.Nickname) > 64 || len(v.Comment) > 2048 {
			// big values
			ctx.SetStatusCode(400)
			return
		}

		if len(dbComments) > 100 {
			// comments limit hit
			ctx.SetStatusCode(400)
			return
		}

        commentx := Comment{
			Nickname: v.Nickname,
			Message:  v.Comment,
		}
        lastComment = commentx
		dbComments = append(dbComments, commentx)
		ctx.SetStatusCode(201)
	}
}

func HandleMemeReport() fasthttp.RequestHandler {
	return func(ctx *fasthttp.RequestCtx) {
		err := BotRunUrl("http://127.0.0.1/admin/")
		if err != nil {
			// bot not working
			log.Log.WithError(err).Error("bot err")
			ctx.SetStatusCode(500)
			return
		}
		// im fine
		ctx.SetStatusCode(201)
	}
}

func HandleLastNickname() fasthttp.RequestHandler {
	return func(ctx *fasthttp.RequestCtx) {
		SendJson(ctx, 200, map[string]map[string]string{
			"response": {
				"nickname": lastComment.Nickname,
			},
		})
	}
}
