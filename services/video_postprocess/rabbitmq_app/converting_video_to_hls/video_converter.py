import os

import asyncio
import subprocess

import orjson

_resolutions = [
    2160,  # 4K
    1440,  # 2k
    1080,
    720,
    480,
    360,
    240,
    144,
]

_bitrates = {
    2160: 12000,
    1440: 8000,
    1080: 5000,
    720: 2800,
    480: 1500,
    360: 1000,
    240: 700,
    144: 400
}


async def _get_encoder() -> str:
    encoder = await asyncio.to_thread(subprocess.run, ['ffmpeg', '-encoders'],
                                      capture_output=True, text=True)

    if 'h264_nvenc' in encoder.stdout:
        return 'h264_nvenc'

    if 'h264_vaapi' in encoder.stdout:
        return 'h264_vaapi'

    return 'libx264'


async def _get_video_resolution(video_path: str) -> tuple[int, int]:
    cmd = [
        'ffprobe', '-v', 'quiet', '-print_format', 'json',
        '-show_streams', video_path
    ]

    result = await asyncio.to_thread(
        subprocess.run, cmd, capture_output=True, check=True, text=True
    )

    data = orjson.loads(result.stdout)
    video_stream = next((s for s in data['streams'] if s['codec_type'] == 'video'), None)
    if not video_stream:
        raise ValueError(f"No video stream in {video_path}")

    width = int(video_stream['width'])
    height = int(video_stream['height'])

    return width, height


async def convert_video_to_hls(unprocessed_path: str, output_path: str):
    width, height = await _get_video_resolution(unprocessed_path)
    main_size = min(width, height)
    resolutions = [i for i in _resolutions if i <= main_size]

    await asyncio.to_thread(os.makedirs, output_path, exist_ok=True)

    tasks = []
    for i, res in enumerate(resolutions):
        target_w = res if width >= height else int(width * res / height) // 2 * 2
        target_h = int(height * res / width) // 2 * 2 if width >= height else res

        cmd = [
            'ffmpeg', '-i', unprocessed_path,
            '-vf', f'scale={target_w}:{target_h}:force_original_aspect_ratio=decrease',
            '-c:v', 'libx264', '-preset', 'medium',
            f'-b:v', f'{_bitrates.get(res, 1000)}k',
            '-c:a', 'aac', '-b:a', f'{96 + i * 8}k',  # Разные битрейты аудио
            '-f', 'hls',
            '-hls_time', '6', '-hls_list_size', '0',
            '-y', f'{output_path}/{i}.m3u8'
        ]
        tasks.append(asyncio.to_thread(subprocess.run, cmd, check=True, capture_output=True))

    await asyncio.gather(*tasks, return_exceptions=True)

    master_content = "#EXTM3U\n#EXT-X-VERSION:3\n"
    for i, res in enumerate(resolutions):
        target_w = res if width >= height else int(width * res / height) // 2 * 2
        target_h = int(height * res / width) // 2 * 2 if width >= height else res
        bitrate = _bitrates.get(res, 1000)
        master_content += f"#EXT-X-STREAM-INF:BANDWIDTH={bitrate * 1000},RESOLUTION={target_w}x{target_h}\n{i}.m3u8\n"

    await asyncio.to_thread(os.makedirs, f"{output_path}/", exist_ok=True)
    with open(f"{output_path}/master.m3u8", 'w') as f:
        f.write(master_content)

    return True
