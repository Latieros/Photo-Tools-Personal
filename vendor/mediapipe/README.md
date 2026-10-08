# Background remover files

Used by Video Layers' **Remove background**. Loaded only when it's turned on, then kept on the device.

| File | What it is |
|---|---|
| `vision_bundle.mjs` | [@mediapipe/tasks-vision](https://www.npmjs.com/package/@mediapipe/tasks-vision) 1.1.0, Google's on-device vision library |
| `wasm/` | The library's WebAssembly engine (the `nosimd` copy is for older browsers) |
| `models/selfie_segmenter.tflite` | Finds people (upright videos and pictures) |
| `models/selfie_segmenter_landscape.tflite` | Finds people (wide videos and pictures) |
| `models/deeplab_v3.tflite` | Finds animals and other things, used for **People and animals** |

**One change from Google's copy:** `vision_bundle.mjs` normally sends usage reports to `odml.pa.googleapis.com` every minute. That is switched off here (its first line says so), so nothing leaves your device.

MediaPipe and these models are © Google, under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). Newer copies can be fetched with the `Fetch cut-out model files` workflow in the Actions tab.
