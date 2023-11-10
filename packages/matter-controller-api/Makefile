all: setup generate

generate:
	buf generate --template ./src/proto/buf.gen.yaml ./src/proto -o ./src

setup:
	buf mod update ./src/proto
