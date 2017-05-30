## wet_mask_1x1

These scripts generate a wet-mask for the 1x1 degree grid used for distributing re-gridded ocean model output.

# Usage

```bash
make
```

`make` will invoke the following steps:
 - Download FRE-NCtools
 - Build fregrid
 - Re-grid the 0.5-degree model wet mask
 - Generate a 1x1 degree wet mask
 - Check the md5sum of the final file is correct
