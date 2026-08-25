# Fonts

**Lora** by Cyreal, from [Google Fonts](https://fonts.google.com/specimen/Lora), under the SIL
Open Font License. The woff2 files are served from here rather than from Google's CDN so the
site has no runtime dependency on it.

Two files, and they are **variable**: one axis, `wght`, from 400 to 700, upright and italic.
That covers every weight the site asks for in 78KB total — the CSS declares each face with a
`font-weight: 400 700` range rather than one file per weight.

Lora tops out at 700, so the 800 set on the title and the deck resolves to 700.
