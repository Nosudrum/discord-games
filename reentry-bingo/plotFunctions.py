from matplotlib.image import imread
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


def start_earth_map():
    fig = plt.figure(figsize=(10, 5), facecolor='black')
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
    ax.set_global()
    ax.imshow(imread('NE1_50M_SR_W.tif'), origin='upper', transform=ccrs.PlateCarree(),
              extent=[-180, 180, -90, 90])
    return fig, ax


def finish_figure(fig, path, show=True):
    plt.tight_layout()
    fig.savefig(path, facecolor="None", edgecolor='none', dpi=300)
    if show:
        plt.show()


def remove_html_margins(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    with open(path, 'w') as f:
        for line in lines:
            if '<head>' in line:
                f.write(line.replace('<head>', '<head><style>body { margin: 0; }</style>'))
            else:
                f.write(line)
