# yt-clip
Download via yt-dlp and then clip and remux in one command.

## Getting Started

### Requirements

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) in path
- [ffmpeg](https://ffmpeg.org/) in path
- [Python](https://www.python.org/) >= v3.12.3

### Installation

Install by cloning the repository and running `python3 -m pip install .`.

## Running

Run using the `yt-clip` command or `python3 -m ytclip`. See usage guide below:

```
usage: yt-clip [-h] [-o OUTPUT] [-s START] [-t END] url

Download via yt-dlp and then clip and remux in one command.

positional arguments:
  url                   URL to downloadable video.

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Path to output file to.
  -s START, --start START
                        Start time for clipping.
  -t END, --to END      End time for clipping.

Requires yt-dlp and ffmpeg to be accessible via the system's PATH.
```

## Authors

- Willow Ciesialka

## License

This project is licensed under GNU GENERAL PUBLIC LICENSE v3. See [LICENSE](LICENSE) for details.