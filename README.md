# Camera Obstruction Detector

Detects when a camera is physically covered by a finger, paper, tape, etc.

Uses FFT frequency analysis:

- clear image: more high-frequency details
- covered image: blurry or flat image, lower ratio

Works with semi-transparent covers too.

## Install

```bash
bash install.sh
```

## Usage

```bash
cam-guard
cam-guard 1 0.15

cam-private
cam-private 0 0.12
```

Skips silently if the camera is already used by another app.

Requires `notify-send` for desktop notifications.


Exit codes:

```text
0 clear
1 camera error
2 obstructed
```

Pick a threshold between clear and obstructed values.

## Cron

```bash
* * * * * DISPLAY=:0 cam-guard 0 0.15
* * * * * DISPLAY=:0 cam-private 0 0.15
```