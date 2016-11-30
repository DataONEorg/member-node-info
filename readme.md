This repository contains information about DataONE Member Nodes that can be used for presentations, web sites, and other fora where Member Nodes are being presented.

## Files and Folders

```
.
└── production          Content for the production environment
    └── graphics        Folder with Member Node icons / logos
        ├── originals   Original images. The image names should start with the node Id, 
        |               but may have a suffix to clarify image characteristics.
        ├── web         Images to be used in Web interfaces. Should be .png, minimum of 
        |               125 wide x 40 high, and with transparency where appropriate.
        └── working     Images in between original and web. Assume web images are generated 
                        automatically from these.
```
Image files are named with the node Id minues the "urn:node:" portion. So for example, the member node:

```
  urn:node:KNB
```

Has web image file named:

```
  production/graphics/web/KNB.png
```
which can be directly linked to from GitHub using the URL:

  https://raw.githubusercontent.com/DataONEorg/member-node-info/master/production/graphics/web/KNB.png

[The wiki](https://github.com/DataONEorg/member-node-info/wiki) has a couple of pages showing the images and their basic info.

## Tools

A couple of handy tools for image introspection and manipulation:

* [exiftool](http://www.sno.phy.queensu.ca/~phil/exiftool/)
* [Imagemagick convert](https://www.imagemagick.org/script/index.php)

Quickly determine the dimensions of an image:

```bash
exiftool -ImageSize FILENAME
```

Generate a list of images with dimensions:

```bash
# cd to the folder with the images
for img in $(ls {*.png,*.jpg}); do \
  SZ=$(exiftool -s -s -s -ImageSize ${img}); \
  printf "%15s %10s\n" ${img} ${SZ}; \
  done
```

Create a copy of an image, resizing with dimensions no smaller than 125 wide by 40 high and saving as a .png:

```bash
IMAGE="IMAGE_FILE"; \
convert working/${IMAGE_FILE} -resize 125x40^ "web/$(basename ${IMAGE_FILE%.*}).png"
```

To create web ready copies of all images in the working folder and place them in the web folder. The resulting images have dimensions of no smaller than 125 pixels wide by 40 pixels high while preserving preserving aspect ratio and saving as .png:

```bash
# cd to the graphics folder
for img in $(ls working/{*.jpg,*.png}); do echo ${img}; \
  convert working/${img} -resize 125x40^ "web/$(basename ${img%.*}).png"; \
  done
```

To generate a wiki page that lists images, their file size and pixel dimensions:

```bash
#cd to the folder containing the images
URL="https://raw.githubusercontent.com/DataONEorg/member-node-info/master/production/graphics/$(basename $(pwd))/";\
IMGS=($(ls {*.png,*.jpg}));\
echo ' ` ` | ` ` | ` `';\
echo "--- | --- | ---"; \
for I in $(seq 0 3 $(expr ${#IMGS[@]} - 1)); do LNK=$(echo ${IMGS[$I]//.} | tr '[:upper:]' '[:lower:]'); \
  printf "[${IMGS[$I]}](#${LNK}) | "; \
  LNK=$(echo ${IMGS[$I + 1]//.} | tr '[:upper:]' '[:lower:]'); \
  printf "[${IMGS[$I + 1]}](#${LNK}) | "; \
  LNK=$(echo ${IMGS[$I + 2]//.} | tr '[:upper:]' '[:lower:]'); \
  printf "[${IMGS[$I + 2]}](#${LNK})\n"; \
  done; \
for img in ${IMGS[@]}; do FSZ=$(exiftool -s -s -s -FileSize ${img}); \
  ISZ=$(exiftool -s -s -s -ImageSize ${img}); \
  printf "## %s\n\n" ${img}; echo "File Size: ${FSZ}"; echo; \
  echo "Image Dimensions: ${ISZ}"; echo; printf '![](%s%s)\n\n---\n' ${URL} ${img}; \
  done
```

Check that a web graphic is available for each current Member Node (requires [xmlstarlet](http://xmlstar.sourceforge.net/) installed as `xml`):

```bash
#cd to the web folder
NODES=($(curl -s "https://cn.dataone.org/cn/v2/node" | \
 xml sel -t -m "//node[@type='mn']" -v "identifier" -n)); \
for node in ${NODES[@]}; do N=${node#*:*:}; \
  if [ -e "${N}.png" ]; then printf "%20s  OK\n" ${node}; \
  else printf "%20s  \e[1;41mWARNING: ${N}.png not found\e[0m\n" ${node}; fi; \
  done
```

## A Note on Image Sizes

Several of the original images that were being served up were rather large, even though they rendered with correct size and placement in the browser because the image size is specified in the containing HTML. This is very inefficient for larger images as each client must download a large image and downscale it for rendering. It is good practice to resize images appropriately before serving.

