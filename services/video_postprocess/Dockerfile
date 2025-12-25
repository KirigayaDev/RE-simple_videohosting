FROM python:3.12.12-alpine3.23

#для healthcheck
RUN apk add --no-cache curl clamav clamav-daemon clamav-libunrar dcron ffmpeg

RUN echo "PrivateMirror https://packages.microsoft.com/clamav/" >> /etc/clamav/freshclam.conf

RUN mkdir -p /var/lib/clamav /var/log/clamav /var/run/clamav && \
    chown -R clamav:clamav /var/lib/clamav /var/log/clamav /var/run/clamav && \
    \
    freshclam --quiet && \
    \
    echo "0 */12 * * * clamav freshclam --quiet" > /etc/crontabs/clamav && \
    chmod 0644 /etc/crontabs/clamav && \
    crontab /etc/crontabs/clamav


WORKDIR /video_postprocess

# Оптимизация пересборки проекта в случаях когда библиотеки не изменились
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

RUN addgroup -g 1000 video_postprocess && \
    adduser -u 1000 -G video_postprocess -D -s /bin/sh video_postprocess && \
    chown -R video_postprocess:video_postprocess /video_postprocess &&  chmod -R 775 /video_postprocess

USER video_postprocess

EXPOSE 8040

CMD ["python3", "main.py"]