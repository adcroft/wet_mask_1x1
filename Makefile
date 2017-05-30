SHELL = bash

all: wet_mask_1x1.nc
	md5sum -c check.md5

# Fetch nctools and build fregrid
FRE-NCtools:
	git clone https://github.com/NOAA-GFDL/FRE-NCtools.git
FRE-NCtools/build.mk FRE-NCtools/env.sh: | FRE-NCtools
	cd $(@D) && cp site-configs/gfdl/$(@F) .
FRE-NCtools/tools/fregrid/fregrid: FRE-NCtools/build.mk FRE-NCtools/env.sh
	cd $(@D) && . ../../env.sh && make

# Copy mosaic files to here
ocean_mosaic.nc ocean_hgrid.nc:
	cp /archive/gold/datasets/OM4_05/mosaic.v20151203.unpacked/$@ .
ocean_annual.static.nc:
	cp /archive/John.Krasting/prerelease_warsaw_20170330_mom6_2017.04.22/CM4_c96L33_am4p0_OMp5_2010_ndiff_khtr200_fk30_30d_tlt_me/gfdl.ncrc4-intel16-prod-openmp/pp/ocean_annual/$@ .

# Re-grid wet-mask to 1x1 grid
tmp_wet.nc: FRE-NCtools/tools/fregrid/fregrid ocean_mosaic.nc ocean_hgrid.nc ocean_annual.static.nc
	./FRE-NCtools/tools/fregrid/fregrid --input_mosaic ocean_mosaic.nc --nlon 360 --nlat 180 --input_file ocean_annual.static.nc --scalar_field wet --output_file tmp_wet.nc

# Create a new mask for 1x1 grid
wet_mask_1x1.nc: tmp_wet.nc Makefile new_mask.py
	python new_mask.py
