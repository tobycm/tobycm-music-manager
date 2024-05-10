---
runme:
  id: 01HPYYYEASPQ5PRVQGW7DN8ZGY
  version: v3
---

use [runme.dev](https://runme.dev) for the best experience with this readme xd

# [Happy Coding Music](https://www.youtube.com/playlist?list=PLSQmKW3jS_HRPnGo1cv9W6IH7Z_-3oAn_) Manager

## Prerequisites

```sh {"id":"01HPYZ4JQQJW20ANETRMWTJZP1"}
pip install -U -r requirements.txt

```

## How to use

`[]` are mandatory arguments

`()` are optional arguments

### Downloader

1. Copy `.example.env` to `.env`

```sh {"id":"01HPYZDSY7HW0N587WWDW9N2Z5"}
cp .example.env .env

```

2. Add values to `.env`

```sh {"id":"01HPYZF5Z2YAYYZANV0JS7QBM6"}
nano .env

```

3. Run `main.py`

```sh {"id":"01HPYZ7J74EMGT2DM1QK0AXT8J"}
python main.py (playlist_id) (output_dir) (yt_dlp_exe)

```

4. Wait :))))

### Replicator

`[src_folder]` should be the same as output dir

```sh {"id":"01HPYZHXF0EMTZDHW6G7RXDA05"}
python replicate.py [src_folder] [dst_folder]

```
