# Nexus Transcoding

## Overview

The Nexus Regulariser is an FFmpeg-based subsystem that processes media files after download completion but before Arr application import. Its purpose is to ensure all media in the final library conforms to user-defined quality and format profiles.

## Processing Flow

```
Download completes in /downloads/complete
        ↓
nexus-worker detects completion
        ↓
nexus-worker pauses/blocks Arr import (where possible)
        ↓
File is copied or moved to /transcode/working
        ↓
ffprobe analyses the media file
        ↓
Profile engine selects the appropriate transcoding profile
        ↓
FFmpeg processes the file according to profile settings
        ↓
Output is verified (codec, resolution, integrity)
        ↓
Processed file is placed back in the completed-download folder
        ↓
Arr app imports the processed result into the library
        ↓
nexus-transcoder records success/failure in history
```

## Key Principles

1. **Never bypass Arr apps**: Nexus does not place files directly into `/tv`, `/movies`, `/music`, or `/adult`. The Arr apps handle final library organisation.
2. **Non-destructive by default**: The original download is preserved until verification is complete and the user's profile settings allow deletion.
3. **Profile-based**: Each library type (TV, Movies, Music, Adult) has its own transcoding profile with independent settings.
4. **Skip-if-compliant**: If a file already matches the target profile, transcoding is skipped to save time and resources.

## Per-Library Profiles

### Video Profiles (TV, Movies, Adult)

Each video profile supports:

| Setting                    | Options                                       |
|----------------------------|-----------------------------------------------|
| Enable/disable profile     | On / Off                                      |
| Video transcode            | On / Off                                      |
| Audio transcode            | On / Off                                      |
| Subtitle handling          | Keep all / Keep selected languages / Strip     |
| Hardware device            | Auto / NVIDIA / Intel / AMD / CPU / Disabled   |
| Video codec                | H.264 / H.265 (HEVC) / AV1 / Copy (remux)    |
| Video encoder              | Auto-selected based on codec + hardware        |
| Quality mode               | CRF / CBR / VBR / Auto                        |
| Quality level              | Numeric (codec-dependent)                      |
| Bitrate cap                | Optional maximum bitrate                       |
| Resolution                 | Source / 720p / 1080p / 1440p / 2160p / Custom |
| Container                  | MKV / MP4                                      |
| HDR behaviour              | Preserve / Tonemap to SDR / Strip              |
| Frame rate                 | Source / 23.976 / 24 / 25 / 29.97 / 30 / 60   |
| Deinterlace                | Off / Auto-detect / Always                     |
| Keep original              | Yes / No                                       |
| Delete original after verify| Yes / No                                      |
| Skip if compliant          | Yes / No                                       |

### Audio Profiles (Music)

| Setting                    | Options                                       |
|----------------------------|-----------------------------------------------|
| Enable/disable profile     | On / Off                                      |
| Target codec               | FLAC / ALAC / MP3 / AAC / Opus / Copy         |
| Quality / bitrate          | Codec-dependent                                |
| ReplayGain analysis        | On / Off                                      |
| Metadata preservation      | On / Off                                      |
| Artwork preservation       | On / Off                                      |
| Container                  | FLAC / M4A / MP3 / Original                   |
| Skip if compliant          | Yes / No                                       |

## Supported Codecs

### Video Codecs

| Codec   | Software Encoder | NVIDIA (NVENC)     | Intel (QSV)        | AMD (AMF/VAAPI)    |
|---------|------------------|--------------------|--------------------|--------------------|
| H.264   | libx264          | h264_nvenc         | h264_qsv           | h264_amf / h264_vaapi |
| H.265   | libx265          | hevc_nvenc         | hevc_qsv           | hevc_amf / hevc_vaapi |
| AV1     | libsvtav1        | av1_nvenc          | av1_qsv (if avail) | av1_amf (if avail) |

### Audio Codecs

| Codec   | Encoder    |
|---------|------------|
| AAC     | aac        |
| AC3     | ac3        |
| EAC3    | eac3       |
| Opus    | libopus    |
| FLAC    | flac       |
| MP3     | libmp3lame |

### Containers

| Extension | Type        |
|-----------|-------------|
| .mkv      | Matroska    |
| .mp4      | MPEG-4      |
| .m4a      | MPEG-4 Audio|
| .flac     | FLAC        |
| .mp3      | MPEG Audio  |

## Queue Management

- `/transcode/queue/` — Files waiting to be processed
- `/transcode/working/` — Currently being transcoded (one at a time by default)
- `/transcode/completed/` — Output verified and ready for Arr import
- `/transcode/failed/` — Files that failed transcoding, kept for review
- `/transcode/logs/` — Per-file FFmpeg command and output logs

## Error Handling

- If FFmpeg returns a non-zero exit code, the file is moved to `/transcode/failed/`
- The full FFmpeg stderr output is saved to `/transcode/logs/<filename>.log`
- Failed files are surfaced in the Nexus dashboard with the error details
- A retry button allows re-processing with the same or modified profile
- Corrupt or unreadable source files are detected by ffprobe and reported immediately

## Dry-Run Mode

- All transcoding profiles support a dry-run mode
- Dry-run generates the FFmpeg command without executing it
- Useful for verifying profile settings before processing real media
- Required for all test fixtures
