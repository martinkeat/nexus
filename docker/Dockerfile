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
    s6-overlay \
    icu-libs \
    krb5-libs \
    libgcc \
    libintl \
    libssl3 \
    libstdc++ \
    zlib \
    gcompat

# Install FFmpeg and other media tools
RUN apk add --no-cache \
    ffmpeg \
    qbittorrent-nox \
    sabnzbd

# Install Arr Suite and Indexing tools
# We'll use the latest stable releases (x64)
RUN mkdir -p /opt && \
    # Sonarr
    curl -L "https://services.sonarr.tv/v1/download/main/latest?version=4&os=linux&arch=x64" -o /tmp/sonarr.tar.gz && \
    tar -xzf /tmp/sonarr.tar.gz -C /opt && \
    rm /tmp/sonarr.tar.gz && \
    # Radarr
    curl -L "https://radarr.servarr.com/v1/update/master/updatefile?os=linux&runtime=netcore&arch=x64" -o /tmp/radarr.tar.gz && \
    tar -xzf /tmp/radarr.tar.gz -C /opt && \
    rm /tmp/radarr.tar.gz && \
    # Lidarr
    curl -L "https://lidarr.servarr.com/v1/update/master/updatefile?os=linux&runtime=netcore&arch=x64" -o /tmp/lidarr.tar.gz && \
    tar -xzf /tmp/lidarr.tar.gz -C /opt && \
    rm /tmp/lidarr.tar.gz && \
    # Prowlarr
    curl -L "https://prowlarr.servarr.com/v1/update/master/updatefile?os=linux&runtime=netcore&arch=x64" -o /tmp/prowlarr.tar.gz && \
    tar -xzf /tmp/prowlarr.tar.gz -C /opt && \
    rm /tmp/prowlarr.tar.gz && \
    # Whisparr
    curl -L "https://whisparr.servarr.com/v1/update/develop/updatefile?os=linux&runtime=netcore&arch=x64" -o /tmp/whisparr.tar.gz && \
    tar -xzf /tmp/whisparr.tar.gz -C /opt && \
    rm /tmp/whisparr.tar.gz && \
    # Overseerr (We'll use the prebuilt binary from sctx/overseerr if possible, but for Alpine we might need to build or use the node-build stage)
    # For now, we'll use a placeholder or pull from a reliable source
    mkdir -p /opt/Overseerr && \
    curl -L "https://github.com/sctx/overseerr/releases/latest/download/overseerr-linux-x64" -o /opt/Overseerr/overseerr && \
    chmod +x /opt/Overseerr/overseerr && \
    # FlareSolverr
    mkdir -p /opt/FlareSolverr && \
    curl -L "https://github.com/FlareSolverr/FlareSolverr/releases/latest/download/flaresolverr_linux_x64.tar.gz" -o /tmp/flaresolverr.tar.gz && \
    tar -xzf /tmp/flaresolverr.tar.gz -C /opt/FlareSolverr --strip-components=1 && \
    rm /tmp/flaresolverr.tar.gz

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
