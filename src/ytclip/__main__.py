import subprocess
from typing import Optional
from pathlib import Path
from sys import stderr
from ytclip.cli import parse_args

def download(url: str) -> bytes:
    process = subprocess.run(["yt-dlp", "--quiet", "-o", '-', url], 
                             capture_output=True)
    if process.returncode == 0:
        return process.stdout
    print(process.stderr, file=stderr)
    raise RuntimeError("Download subprocess failed.")

def trim_and_convert(video: bytes, *, start:Optional[str] = None, end:Optional[str] = None):
    # Remux to 720p H.264 MP4
    commands = ['ffmpeg', '-loglevel', 'error']
    if start:
        commands.extend(['-ss', start])
    if end:
        commands.extend(['-to', end])
    commands.extend(['-i', 'pipe:0'])
    commands.extend([
        '-vcodec', 'libx264',
        '-acodec', 'aac',
        '-movflags', 'frag_keyframe+empty_moov',
        '-f', 'mp4',
        'pipe:1'
    ])
    process = subprocess.run(commands, 
                             input=video, 
                             capture_output=True)
    if process.returncode == 0:
        return process.stdout
    print(process.returncode)
    print(process.stdout)
    print(process.stderr, file=stderr)
    raise RuntimeError("Conversion subprocess failed.")

def main():
    args = parse_args()
    output = args.output
    url = args.url
    start = args.start
    end = args.end
    print("Downloading video...")
    video = download(url)
    print("Trimming and converting...")
    converted_video = trim_and_convert(video, start=start, end=end)
    print("Writing...")
    if isinstance(output, Path):
        with open(output, "wb") as f:
            f.write(converted_video)
    else:
        output.write(converted_video)
    print("Done!")

if __name__ == "__main__":
    main()