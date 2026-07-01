```
gst-launch-1.0 \
  filesrc location=data/vtest.avi ! \
  avidemux ! \
  decodebin ! \
  videoconvert ! \
  gtksink
```

```
gst-launch-1.0 \
  filesrc location=data/vtest.avi ! \
  avidemux ! \
  decodebin ! \
  videoconvert ! \
  videorate ! \
  video/x-raw,framerate=2/1 ! \
  gtksink
```