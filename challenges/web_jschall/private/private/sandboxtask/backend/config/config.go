package config

import (
	"github.com/kelseyhightower/envconfig"
	"log"
	"time"
)

var Config *config

func init() {
	var s config
	err := envconfig.Process("", &s)
	if err != nil {
		log.Fatal(err.Error())
	}
	Config = &s
}

type config struct {
	RequestTimeout time.Duration `default:"50s" split_words:"true"`
}
