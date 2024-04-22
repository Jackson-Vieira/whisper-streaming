# Whisper streaming

Todo
- [X] - Fast API Server
- [X] - Dockerizer
- [ ] - Docker compose
- [ ] - Refact code (Split code, best practices, logging, env variables ...)
- [X] - Deploy
- [ ] - SSL (TLS)
- [ ] - Proxy service free (POC) using deepgram e um frontend simples consumindo (SEGUNDA FEIRA) (Whisper and deepgram choice what service to use as design pattern)

Pesquisa
- [X] Pesquisa de availabilidade usando outros serviços (Azure, Google, ...)

Melhorias
```
# TODO: handle inputs has base64 (start with base64) [X]
# TODO: Dockerize this
# TODO: handle exceptions like vad
# TODO: Log all process time to monitor performance (justificative)
# TODO: Otimize this process to be faster and not need encode base64 (maybe this is slow) and remove
# external depedency like whisper load audio from pip
# TODO: maybe run transcription in a separate thread
# TODO: maybe put a queue to process multiple requests
```
