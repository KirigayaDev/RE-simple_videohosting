import subprocess
import asyncio


async def scan_video(video_path, timeout=1800) -> bool:
    cmd = [
        "clamscan", "--no-summary", "--infected",
        "--detect-pua", video_path
    ]

    try:
        result = await asyncio.to_thread(subprocess.run,
                                         cmd, capture_output=True, text=True,
                                         timeout=timeout, check=False
                                         )
        return result.returncode == 0

    except subprocess.TimeoutExpired:
        return False

    except Exception as e:
        return False
