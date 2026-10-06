# Photo Tools

A small set of personal browser tools for dressing up photos, making short videos and cleaning up image files.

**Open it:** https://latieros.github.io/Photo-Tools-Personal/

- **Everything runs in your browser.** Photos, videos and sounds never leave your device, and nothing is uploaded anywhere.
- **Your work is kept automatically.** Each tool saves its work in the browser (videos and photos included), so you can close the page or switch tools and pick up where you left off.
- **It works offline.** Install it as an app on your phone or computer and it runs without internet.
- **Search engines are asked not to list it** (every page has `noindex, nofollow`).

| Tool | What it does |
|---|---|
| [Photo Frame Studio](#photo-frame-studio) | Puts a photo inside a frame: social posts, phone screens, chats, camera screens, prints, comics and covers. Exports an image, or a video for the chat frames. |
| [Chat Reel](#chat-reel) | Turns a text conversation into a video, timing every message on a timeline. |
| [Metadata Scrubber](#metadata-scrubber) | Strips prompts, settings and hidden data out of images and saves clean copies under random names. |
| [Video Layers](#video-layers) | Puts pictures, videos, text and music together and exports a new video. |

Every tool has a switcher at the top to jump to another tool. Your work is saved before it switches.

---

## Photo Frame Studio

Pick a frame, add a photo, change the words, drag things into place, export.

### Frames

**Social & phone**
- **Story caption:** a full-screen story with a see-through caption bar you can slide, a big sticker word and a profile header.
- **Social post:** a feed post with username, location, likes, caption, comments and time. Light or dark.
- **Short video (TikTok-style):**
  - The For You and Following tabs, plus the like, comment, save and share rail with a spinning sound disc.
  - Caption with bold hashtags, the sound line and a link pill.
  - Text on the video in four styles.
  - Phone or video-only layout.
- **Phone camera:** a phone viewfinder with camera modes, zoom buttons, grid, recording timer and last-photo thumbnail.
- **Gallery viewer:** an Android-style photo view with date header and share, edit, favorite and delete buttons.
- **iPhone messages, Android messages, Social DM (Instagram-style):** text threads.
  - Write one message per line, starting your own with `me:`.
  - Add time dividers with `--`.
  - Place up to three chat photos with `[1]`, `[2]`, `[3]`. Each one can show as a photo, a video or a shared post.
  - Choose bubble colors, status lines and light or dark mode.
- **Video page (YouTube-style):** a player with chapter progress bar, title, channel, subscribe button, likes and description.
- **Microblog post (X-style):**
  - Verified badge, post text, optional link and photo, time, views and counts.
  - The photo can be landscape, square, portrait or its original shape.
  - Dark, dim or light.

**Cameras**
- **Camera viewfinder:** Fuji-, Canon- or Nikon-style live view.
  - Shutter, aperture, ISO, exposure compensation, shots left and battery.
  - Grid or crop overlay, and a focus box you can drag.
- **Security camera:**
  - Single, split or quad view, with a photo of your choice for each camera.
  - Night vision, color or black and white.
  - Timestamp, camera names, REC light and a motion box.

**Prints**
- **Polaroid:** a handwritten caption and date, frame colors and film looks.
- **Instax:** mini, square or wide, with plain, striped or confetti borders.

**Covers & comics**
- **Manga panel:** an inked look, plus four kinds of text, each with its own shapes:
  - a speech bubble (round, box, jagged or whisper);
  - a thought bubble (cloud, puffy, soft or narration box);
  - a shout (rays, burst, spiky or electric);
  - a sound effect in four lettering styles.
- **Magazine cover:**
  - Masthead, cover star, cover lines, a right-hand column, issue date and price.
  - Several font choices for each block.
  - A barcode you can randomize.
- **Movie poster:** Blockbuster, Festival (with laurel), Horror or Retro styles, with cast, tagline, credits block and release line.
- **Book cover:** Thriller or Literary styles, with title, tagline, author and a review quote.

### Editing
- **Add a photo:** with the button, by dropping it on the preview, or by pasting it.
- **Move things:** zoom and drag the photo, drag text and bubbles where you want them, or reset everything with **Re-center**.
- **Second photo:** frames with a profile or contact picture can take one, and it's shared by every frame that uses one.

### Animated chats
- **Play it:** the iPhone, Android and Social DM frames can play like a real conversation, with typing dots and messages popping in. At the end, a photo can be tapped open full screen.
- **Settings:** speed, typing dots, which photo opens, how long to hold at the end, and looping.
- **Make video:** saves it as **WebM**, **MP4** or **GIF**, at best quality, half size, or under a size limit you choose (for example, under 5 MB).

### Saving
- **Export image:** saves a PNG. **Copy image** puts it on the clipboard.
- **Save project / Open project:** keeps everything, photos included, in a `.json` file you can open again on any device.

---

## Chat Reel

A timeline editor for text conversations that you export as a video.

### Messages
- **Adding:** add their messages, your messages, photos and time dividers.
- **Editing each message:** reorder it, duplicate it or switch who sent it.
- **Photo messages:** can show as a photo, a video or a shared post (with an account name). They can be tapped open full screen after they arrive.

### Timing
- **Per message:**
  - the pause before it;
  - typing dots, with the typing time set by hand or worked out from the message length;
  - for your own messages, typing it out on the on-screen keyboard, with the time set by keyboard speed (slow, normal or fast).
- **Overall:** a pause at the start and a hold at the end.
- **Timeline:** drag the blocks to change the pauses, how long typing lasts, and how long a photo stays open.

### Look
- **Phone style:** iPhone, Android or Social DM, light or dark.
- **Contact:** name or username, contact photo, status line, avatar color and clock.
- **Bubbles:** your bubble color (blue, green for SMS, purple or gradient) and the line under your last message (Delivered, Read, Seen…).

### Sound
- **Built-in sounds:** for sending, replying, keyboard typing and opening a photo (Pop, Chime, Click, Tap or silent), with a volume control.
- **Per-message sounds:** any message can have its own sound.
- **My sounds:** upload your own sound files (MP3, WAV, M4A). They're kept in the browser and recorded into the video.

### Export and projects
- **Formats:** WebM, MP4 or GIF, at best quality, half size or under a size limit. Sound can be included in WebM and MP4.
- **Projects:** save and open them as files. Work is also kept automatically.

---

## Metadata Scrubber

Removes everything from an image except the picture itself, then saves it under a new random name.

### What it removes
- **AI image data:** prompts, undesired content, seed, model and every generation setting from NovelAI, Stable Diffusion and ComfyUI.
- **NovelAI's hidden copy:** the copy of the settings NovelAI hides inside the image's transparency layer.
- **Camera and file data:** EXIF details (camera, date, **GPS location**), XMP, color profiles, Photoshop info, comments and Content Credentials.
- **The original file name.**

### How it works
- **Adding images:** drop in as many PNG, JPG or WebP images as you like, or pick or paste them.
- **What it found:** each image shows what was in the original (with copy buttons for the prompt and seed). The new file is checked again to confirm nothing is left.
- **Format:** save in the same format, or as PNG, JPG or WebP, with a quality slider.
- **New names:** random letters or photo-style names (like `IMG_20261006_142233`). Edit any name or roll new ones.
- **Pixel shuffle (optional):** scrambles the invisible lowest bit of every pixel to wipe data other tools hide in the pixels themselves. It turns on automatically when hidden pixel data is found.
- **Download:** one at a time, or all at once as a ZIP.

---

## Video Layers

Puts pictures, videos, text and music together and makes a new video. The first picture or video you add fills the frame. Anything after it goes on top as an overlay, and each layer gets its own bar on the timeline.

### Pictures and videos
- **Move and resize:**
  - Drag a layer to move it. It snaps to the edges and middle of the video and to other layers.
  - Drag a corner to resize (the shape is kept unless you hold Shift).
  - Untick **Keep its shape** to stretch it with the side handles.
- **Exact numbers:** type the position, width and height in pixels.
- **Fit, Fill or Stretch** to the whole video, or snap the layer to any of 9 spots.
- **Crop:**
  - Open the crop tool and drag the corners or edges, freely or locked to a shape (1:1, 4:5, 9:16, 16:9, 4:3, 3:4, the video's shape, or another layer's shape).
  - There are also quick-crop buttons and a slider for each side.
  - Cropping keeps what's left the same size and in the same place.
- **Turn and flip:** a rotate handle (snaps to 45° steps), 90° buttons, mirror and upside down.
- **Match another layer:**
  - Same width, same height, fit inside it, or cover it.
  - **Crop to match** or **Stretch to match** puts it exactly on top of the other layer at the same size and shape.
  - Or place it on any of 9 spots of that layer, such as a picture in the corner of the video.
- **Look:**
  - Opacity, and square, rounded or circle shape.
  - A border, and a drop shadow that follows the outline of see-through PNGs.
- **Blend:** **Screen** hides black backgrounds; **Multiply** hides white ones.
- **Color:**
  - Filters: B&W, Vintage, Warm, Cool, Vivid, Faded, Noir, Dramatic and Dreamy.
  - Sliders for brightness, contrast, saturation, warmth, hue, black and white, blur and dark edges.
- **Slow movement:** a slow zoom in or out, or a drift in any direction, over the time the layer shows.

### Video and sound
- **Timeline:** trim the start and end by dragging the bar ends or with sliders.
- **Speed:** ¼× up to 4×.
- **When a video ends:** it can disappear, freeze on the last frame, or loop.
- **Sound:** volume, mute, and sound fade in and out for each video and music track.
- **Split:** cuts any layer in two at the playhead (keyboard: S).

### Text overlays
- **Styles:** 10 one-tap styles: Caption, Highlight, Meme, Title, Lower third, Subtitle, Neon, Sticky note, News bar and Typewriter.
- **Fonts:** 13 of them, including Clean, Wide, Bold, Tall, Serif, Elegant, Marker, Handwriting, Script, Comic, Rounded, Typewriter and Mono.
- **Text settings:** size, color, alignment, italic, ALL CAPS, letter and line spacing, and wrap width (drag the side handles).
- **Outline and shadow:** an outline in any color and thickness, and a soft, hard or glowing shadow.
- **Backgrounds:** a box, a box behind each line (TikTok-style) or a full-width bar, in any color and opacity.
- **Shortcut:** double-click text in the preview to edit it.

### Animation (every layer)
- **Entrances and exits:** fade, pop, zoom, or slide from or to any side.
- **For text only:** typewriter and word by word.

### Video size
- **Exact pixels:** type any width and height (up to 4096) and the video is exactly that size. A link button keeps the shape while you type if you want it to.
- **Quick sizes:** Auto (follows the bottom layer), 9:16, 1:1, 4:5, 16:9, 4:3, 3:4, and a button to turn it sideways.
- **Stretch to this size:** squeezes the main video to fill any size you pick.
- **Empty space:** a blurred copy of the video or a solid color.

### Editing comforts
- **Undo and redo:** Ctrl+Z and Ctrl+Shift+Z.
- **Quick-edit bar** under the preview: Crop, Fit, Fill, Stretch, Flip, 90°, Split and Duplicate.
- **Keyboard:** arrow keys nudge (Shift for bigger steps), Delete removes, Ctrl+D duplicates, Space plays and pauses.

### Export
- **Formats:** **MP4** or **WebM**, with sound, at best quality, half size or under a size limit.
- **Recording runs in real time,** so a 20-second video takes about 20 seconds. Keep the tab in front while it records.

---

## Install it as an app (works offline)

- **Android (Chrome):** open the site, tap **⋮** and choose **Install app** or **Add to Home screen**.
- **iPhone (Safari):** open the site, tap **Share** and choose **Add to Home Screen**.
- **Computer (Chrome or Edge):** click the install icon in the address bar, or use **Install app** on the start page.

Open each tool once while you're online so everything, fonts included, is saved for offline use. Updates download on their own the next time you open the app online.

## Browser notes

- **Chrome and Edge** support everything, including video export with sound.
- **Safari:**
  - Video export depends on the Safari version; MP4 is the format to try.
  - Color filters in Video Layers need a recent version.
- **GIFs** are silent and limited to 256 colors.

## Files

| File | What it is |
|---|---|
| `index.html` | Start page with links to every tool and the install button |
| `photo-frame-studio.html` | Photo Frame Studio |
| `chat-reel.html` | Chat Reel |
| `metadata-scrubber.html` | Metadata Scrubber |
| `video-layers.html` | Video Layers |
| `manifest.webmanifest` | App name, icons and shortcuts for installing |
| `sw.js` | Offline support: keeps the tools and fonts on your device |
| `icons/` | App icons |

Each tool is a single self-contained HTML file with no build step and no server code.
