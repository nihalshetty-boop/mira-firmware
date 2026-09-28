# Car Thing firmware

This fork builds a Car Thing image that shows the [MacThing](https://github.com/srcurran/MacThing) page instead of Mira's Spotify screens. The clock is on whenever the device has power. A missing Mac is a normal state, not a failure: the page keeps the last forecast and the day's events. The Mac bridge reaches Chromium's debug port over USB. This image does not start the Spotify daemon and has no `adb`. After a minute with no input, or when the Mac display sleeps, the page asks `auto_brightness` on the device to drop the backlight. That does not need a shell.

The two git repos stay separate. This repo is the image builder. MacThing is the UI, cloned beside it. The build checks out both, zips MacThing's `dist/ui`, and serves that zip at `http://localhost:80`.

## Credit

- [Mira](https://github.com/mira-thing) by [MustakimK](https://github.com/MustakimK). This builder is a fork of [mira-firmware](https://github.com/mira-thing/mira-firmware), Apache 2.0. It keeps that license and the image's clock, display, USB, and Bluetooth chip services, and it leaves out Mira's Spotify daemon, UI, and voice stack.
- [Sean Curran](https://github.com/srcurran), author of [MacThing](https://github.com/srcurran/MacThing), MIT. The page in the image is that project, including this fork's clock change.
- Earlier builder and kernel credits are in [Attributions](#attributions) below.

## Flash a release

Each successful run of the Image build action publishes a GitHub Release on this repo. The attached file is `mira_firmware_v1.1.0.zip`. Push MacThing first if the release should include a new page, then push this repo or run the workflow by hand. A push to MacThing alone does not start the image build.

Flash with [Terbium](https://terbium.app/) in a Chromium browser such as Chrome. Flashing wipes the Car Thing. On a Mac, do not install Terbium's Windows driver. Bricking is unlikely. Holding buttons 1 and 4 while plugging in USB puts the device back in flash mode.

1. Hold buttons **1** and **4** while you plug in a data USB-C cable. A black screen means it is ready.
2. Open [terbium.app](https://terbium.app/) and follow it until the firmware step.
3. Choose **Local archive**, not **Mira**. The Mira choice is [Mira's Spotify release](https://github.com/mira-thing/mira-releases). Select `mira_firmware_v1.1.0.zip`. Do not unzip it.
4. Wait about 5–10 minutes. If the progress bar stalls, start again from step 1.
5. When Terbium finishes, unplug the cable and plug it back in.

First boot should be the MacThing clock, not a Spotify sign-in. The time can be wrong until the device has reached a network once, because that is when `clock_sync` sets the clock.

## Build the image yourself

Keep the repos as siblings. The UI directory must be named `MacThing`:

```bash
git clone https://github.com/srcurran/MacThing.git MacThing
git clone https://github.com/mira-thing/mira-firmware.git
```

Use your own forks if that is where the clock change and this builder live. On a Mac, Docker has to be running and `just` installed (`brew install just`). Do not use `just run` here. That path expects Void Linux tools on the host.

```bash
cd mira-firmware
just docker-run
```

That builds the MacThing page, zips `dist/ui` to `ui.zip`, and writes `output/mira_firmware_v1.1.0.zip`. The first run downloads the Thing Labs base system inside the container and takes a long time. Flash that zip with the Terbium steps above.

`BUNDLE_VOICE` defaults to `0`. The Spotify binary is installed only if `go-librespot-armv6` and `go-librespot-config.yml` are already in this directory. This fork's `just prepare` does not produce them.

## Attributions

This firmware builder was forked from [mira-thing/mira-firmware](https://github.com/mira-thing/mira-firmware), which was forked from [usenocturne/nocturne](https://github.com/usenocturne/nocturne). Credit to Brandon Saldan, shadow, Dominic Frye, and bbaovanc for the Nocturne builder.

That builder was itself based on:

- [raspi-alpine/builder](https://gitlab.com/raspi-alpine/builder) by Benjamin Böhmke and Duncan Bellamy
- [JoeyEamigh/nixos-superbird](https://github.com/JoeyEamigh/nixos-superbird)
- [bishopdynamics' superbird-tool](https://github.com/bishopdynamics/superbird-tool) and modified [aml-imgpack](https://github.com/bishopdynamics/aml-imgpack)
- [Thing Labs' superbird-tool fork](https://github.com/thinglabsoss/superbird-tool)

The bundled kernel (`resources/kernel/boot_custom.dump`) is a patched fork of Thing Labs' / spsgsb [kernel-common](https://github.com/thinglabsoss).

## License

This firmware builder is **Apache 2.0**.

The MacThing page packed into the image is **MIT**, copyright Sean Curran. See that repo's `LICENSE`.

The bundled kernel image is **GPL-2.0** (Linux), a patched fork of Thing Labs' / spsgsb kernel-common. The complete corresponding source is available to any third party on request for at least three years from distribution of an image that contains that kernel.

> "Spotify" and "Car Thing" are trademarks of Spotify AB. This software is not affiliated with or endorsed by Spotify AB.
