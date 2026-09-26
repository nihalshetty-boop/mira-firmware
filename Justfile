# Pack the sibling MacThing UI into ui.zip. This image does not build Spotify or voice.
prepare:
    @echo ">> building ${IMAGE_VERSION:-$(grep -m1 'IMAGE_VERSION:=' build.sh | sed 's/.*:="\(.*\)"}"*/\1/')}   (set in build.sh, or override with IMAGE_VERSION=vX.Y.Z just docker-run)"
    cd ../MacThing && npm run build:ui
    rm -f ./ui.zip
    cd ../MacThing/dist/ui && zip -r9 {{justfile_directory()}}/ui.zip .
    : > ./lp.env
    mkdir -p ./voice-artifacts

run: prepare
    sudo ./build.sh

lint:
    pre-commit run --all-files

docker-qemu:
    docker run --rm --privileged multiarch/qemu-user-static --reset -p yes

docker-build: prepare
    docker build -t firmware-builder .

docker-run: docker-build
    # IMAGE_VERSION must be forwarded or the override silently does nothing and
    # the image ships the internal version counter instead of the release name.
    # BUNDLE_VOICE defaults off so an empty voice-artifacts directory is not installed.
    docker run --rm --privileged -e BUNDLE_VOICE="${BUNDLE_VOICE:-0}" -e IMAGE_VERSION -v ./output:/work/output firmware-builder:latest
