# Stage 1: Build Web Frontend
FROM node:20-alpine AS web-build
WORKDIR /app
# TODO: Install Tabler and build the static frontend
# For now, we'll just create a placeholder
RUN mkdir -p dist && echo "<h1>Nexus Web Placeholder</h1>" > dist/index.html

# Stage 2: Final Image
FROM alpine:3.20

# Metadata
LABEL maintainer="spontaneocus"
LABEL description="Nexus - Single-container media automation platform"

# Environment Variables
ENV PUID=99 \
    PGID=100 \
    TZ=Etc/UTC \
    UMASK=022 \
    PYTHONUNBUFFERED=1

# Install Base Dependencies
RUN apk add --no-cache \
    bash \
    curl \
    ca-certificates \
    python3 \
    py3-pip \
    shadow \
    tzdata \
    xz \
    s6-overlay

# Install FFmpeg and other media tools
RUN apk add --no-cache \
    ffmpeg \
    ffprobe

# Create directory structure
RUN mkdir -p \
    /app/api \
    /app/web \
    /app/worker \
    /app/transcoder \
    /config \
    /downloads/incomplete/torrents \
    /downloads/incomplete/usenet \
    /downloads/complete/torrents/tv \
    /downloads/complete/torrents/movies \
    /downloads/complete/torrents/music \
    /downloads/complete/torrents/adult \
    /downloads/complete/usenet/tv \
    /downloads/complete/usenet/movies \
    /downloads/complete/usenet/music \
    /downloads/complete/usenet/adult \
    /tv \
    /movies \
    /music \
    /adult \
    /transcode/queue \
    /transcode/working \
    /transcode/completed \
    /transcode/failed \
    /transcode/logs

# Copy web frontend from build stage
COPY --from=web-build /app/dist /app/web

# Copy Nexus application code
COPY apps/api /app/api
COPY apps/worker /app/worker
COPY apps/transcoder /app/transcoder
COPY branding /app/branding

# Copy Docker rootfs (scripts, s6-overlay configs)
COPY docker/rootfs /

# Set up virtual environment for Python
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Install API dependencies (placeholder)
RUN pip install --no-cache-dir fastapi uvicorn pydantic pyyaml aiohttp

# Permissions and User Setup
# We don't create the user here, we'll use the s6-overlay PUID/PGID mechanism

# Expose Nexus GUI/API port
EXPOSE 8080

# BitTorrent ports
EXPOSE 6881/tcp
EXPOSE 6881/udp

# Entrypoint is handled by s6-overlay
ENTRYPOINT ["/init"]
