This repository contains information about DataONE Member Nodes that can be used for presentations, web sites, and other fora where Member Nodes are being presented.

## Files and Folders

```
.
└── production          Content for the production environment
    └── graphics        Folder with Member Node icons / logos
        ├── originals   Original images
        └── web         Images to be used in Web interfaces
```

Image files are named with the node Id minues the "urn:node:" portion. So for 
example, the member node:

```
  urn:node:KNB
```

Has web image files named:

```
  production/graphics/web/KNB.png
```


## Tools

A couple of handy tools for image introspection and manipulation:

* exiftool
* Imagemagick convert

To generate a list of images with dimensions:

```bash
for img in $(ls .); do SZ=$(exiftool -s -s -s -ImageSize ${img}); \
  printf "%15s %10s\n" ${img} ${SZ}; done
```

To create copies of images with dimensions of no smaller than 125 pixels wide by
40 pixels high while preserving preserving aspect ratio and saving as .png:

```bash
for img in $(ls originals/*.jpg); do echo ${img}; \
  convert ${img} -resize 125x40^ "$(basename ${img%.*}).png"; \
  done
```

