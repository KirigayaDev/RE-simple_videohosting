FROM golang:1.25.5 AS file_upload_builder

WORKDIR /file_upload
ENV GOPATH=/go
ENV PATH=$PATH:/usr/lib/go/bin:$GOPATH/bin

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build ./cmd/server/

RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*


FROM gcr.io/distroless/static-debian12:nonroot

WORKDIR /file_upload

COPY --from=file_upload_builder /file_upload /file_upload
COPY --from=file_upload_builder /usr/bin/ffmpeg /usr/bin/ffmpeg
COPY --from=file_upload_builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
COPY --from=file_upload_builder /usr/bin/curl /usr/bin/curl

USER nonroot

EXPOSE 8050

CMD ["./server"]