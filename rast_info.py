# Discover and print raster attributes using GDAL

try:
    #assume osgeo is installed
    from osgeo import gdal
    from osgeo.gdalconst import *
    print 'imported gdal from osgeo'
except ImportError:
    #if can't import from osgeo, maybe we're using FWTools or some other
    import gdal
    from gdalconst import *
    print 'imported gdal'

fileName = r'C:\Users\ciurro\Downloads\NLCD\nlcd_2011\nlcd60mclip01'

dataset = gdal.Open(fileName) #defaults to readonly access

if dataset is None:
    print "Couldn't open",fileName
    exit(1)

print 'Opened',fileName,'with driver',dataset.GetDriver().ShortName



geoT = dataset.GetGeoTransform()
if geoT is not None:
    print '\nUpper left corner: (',geoT[0], ',',geoT[3],')'
    if geoT[2] == 0 and geoT[4] == 0:
        print ' Pixel Size: (',geoT[1], ' by ',geoT[5], ')'
    else:
        print 'Geo transform is:'
        print 'X = %f + %f*U + %f*V' % (geoT[0],geoT[1],geoT[2])
        print 'Y = %f + %f*U + %f*V' % (geoT[3],geoT[4],geoT[5])

for i in xrange(0,dataset.RasterCount):
    band = dataset.GetRasterBand(i+1)
    print '\nWorking on band',i+1
    print 'Band Type=',gdal.GetDataTypeName(band.DataType)

    min = band.GetMinimum()
    max = band.GetMaximum()
    if min is None or max is None:
        (min,max) = band.ComputeRasterMinMax(1)
    print 'Min=%.3f, Max=%.3f' % (min,max)

    if band.GetOverviewCount() > 0:
        print 'Band has ', band.GetOverviewCount(), ' overviews.'

    if band.GetRasterColorTable() is not None:
        print 'Band has a color table with ', \
        band.GetRasterColorTable().GetCount(), ' entries.'
