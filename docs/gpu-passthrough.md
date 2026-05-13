# GPU Passthrough

## Overview

Nexus supports hardware-accelerated transcoding via GPU passthrough. GPU availability is detected at runtime and is never assumed.

## Detection Process

On startup and on-demand via the GPU Capability panel, Nexus runs detection for:

1. **Device availability**: Check `/dev/dri` for Intel/AMD VAAPI devices
2. **NVIDIA runtime**: Check for NVIDIA container runtime and `nvidia-smi`
3. **FFmpeg capabilities**: Query available encoders, decoders, and hardware acceleration methods
4. **Specific encoder support**: Test availability of each hardware encoder

## Detection Commands

```bash
# List hardware acceleration methods
ffmpeg -hwaccels

# List available encoders
ffmpeg -encoders 2>/dev/null | grep -E '(nvenc|qsv|vaapi|amf)'

# List available decoders
ffmpeg -decoders 2>/dev/null | grep -E '(cuvid|qsv|vaapi)'

# Check /dev/dri devices
ls -la /dev/dri/

# Check NVIDIA
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader
```

## Capability Cards

The GPU panel displays:

| Card                    | Content                                          |
|-------------------------|--------------------------------------------------|
| Detected GPU Vendor     | NVIDIA / Intel / AMD / None                      |
| Detected Devices        | List of GPU devices visible to the container      |
| Available Encoders      | Green badges for supported hardware encoders      |
| Unavailable Encoders    | Grey badges for unsupported encoders              |
| Driver/Runtime          | Version info if available                         |
| Test Transcode          | Result of a tiny test encode                      |
| Recommended Profile     | Suggested codec based on detected capabilities    |
| Warnings                | Missing devices, driver issues, fallback notices  |

## Hardware Selection in Profiles

Users choose from:

| Option              | Behaviour                                                |
|---------------------|----------------------------------------------------------|
| Auto-detect         | Use best available hardware; fall back to CPU             |
| NVIDIA              | Use NVENC; fail if unavailable                            |
| Intel               | Use QSV or VAAPI; fail if unavailable                     |
| AMD                 | Use AMF or VAAPI; fail if unavailable                     |
| CPU (software)      | Always use software encoders (libx264, libx265, etc.)     |
| Disable transcoding | Skip all transcoding for this profile                     |

## Safety Guards

- If a user selects AV1 encoding but the hardware does not support it, Nexus blocks the save with a clear error message.
- The user can override to CPU/software AV1 with explicit confirmation.
- If a user selects NVIDIA but no NVIDIA runtime is detected, Nexus shows a warning and prevents activation until resolved or overridden to CPU.
- All hardware encoder selections are validated against detected capabilities before saving.

## Unraid-Specific Notes

### Intel Arc / iGPU

Most Intel CPUs with integrated graphics support QSV. Intel Arc GPUs support QSV and may support AV1 encoding.

Pass through: `--device /dev/dri:/dev/dri`

### NVIDIA

Requires the Unraid NVIDIA plugin or manual NVIDIA Container Runtime setup.

Pass through: `--runtime=nvidia --gpus all` or specific device passthrough.

### AMD

AMD GPUs typically expose via VAAPI through `/dev/dri`.

Pass through: `--device /dev/dri:/dev/dri`

### No GPU

Nexus runs without any GPU. The capability panel will show "No hardware acceleration detected" and all profiles will use CPU software encoding. This is fully functional, just slower.

## Test Transcode

The GPU panel includes a "Run Test" button that:

1. Uses a tiny built-in test clip (a few seconds, low resolution)
2. Attempts to encode it with the selected hardware encoder
3. Reports success/failure, encoding speed, and output file validity
4. Does not touch user media
