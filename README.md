# DA231X_master_thesis

Master Thesis at KTH and Remote.aero.

## Setup

This project is meant to replicate the setup [remote.aero](remote.aero) uses in their drone setup, but in a more simpler way.

### Server

The server is a Python server that takes a video feed as input (live or virtual camera), optionally performs object detection, and then streams the video to a client. The server is meant to run a Raspberry Pi, but can of course be run anywhere.

### Client

The client is a simple interface meant to run in a web browser. It connects to the server, displays the video feed, and optionally performs object detection.
