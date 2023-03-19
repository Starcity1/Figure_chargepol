import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shapereader
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER

US_COUNTIES = "Figure_Dependencies/Texas_County_Boundaries_Detailed/County.shp"

def createLocationList(data):
    negPos = [[],[]] # Index 0 are all longitudes, index 1 are all latitudes
    posPos = [[],[]]

    for index, event in enumerate(data['Charge']):
        if(event[0] == 'pos'):
            posPos[0].append(float(data['Location'][index][0]))
            posPos[1].append(float(data['Location'][index][1]))
        else:
            negPos[0].append(float(data['Location'][index][0]))
            negPos[1].append(float(data['Location'][index][1]))

    return (negPos, posPos)

def withinInterval(timeInfo, timePoint) -> bool:
    return (timePoint > timeInfo[0] and timePoint < (timeInfo[0] + timeInfo[1]))

def mapHoustonData(HLMAdata = None, figurePath = None, returnFigure = False, ax = None):
    neg, pos = createLocationList(HLMAdata)

    if ax == None:
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(projection=ccrs.Mercator())

    county_lines = cfeature.ShapelyFeature(shapereader.Reader(US_COUNTIES).geometries(), ccrs.PlateCarree(),
                                           facecolor='none', edgecolor='black', lw=1)
    ax.add_feature(county_lines)

    # Zoom in on the Houston area by setting longitude/latitude parameters
    ax.set_extent(
        [-98, -92, 28, 32],
        crs=ccrs.PlateCarree()
    )

    ax.scatter(x=pos[1], y=pos[0], s=4, linewidth=.5, color=[1, 0.062, 0.019, .5],
                marker='+', transform=ccrs.PlateCarree())
    ax.scatter(x=neg[1], y=neg[0], s=4, linewidth=.5, color=[0.062, 0.019, 1, .5],
                marker='_', transform=ccrs.PlateCarree())
    if returnFigure:
        return ax

    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True)
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER

    plt.show()
    plt.savefig(figurePath + "/Houston_map.pdf")