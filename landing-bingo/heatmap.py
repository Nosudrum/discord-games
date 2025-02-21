import matplotlib.cm as cm
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

from grid import *

answers = pd.read_csv("answers.csv")
answers = pd.DataFrame([answers.iloc[:, 2], answers.iloc[:, 3]]).T
answers.columns = ["segment", "zone"]
answers["bet"] = answers["segment"] + answers["zone"].map(str)
values = answers.bet.value_counts().values

color_map = cm.get_cmap("Oranges")

for ii, radius in enumerate(radii):
    if ii == 0:
        value = (answers["segment"] == "A").sum()
        print(f"A: {value}")
        if value > 0:
            value_normalized = value / (values.max())
            color = color_map(value_normalized)
            circle = Circle(
                center_coords,
                radius=radius,
                edgecolor="none",
                facecolor=color,
                alpha=0.5,
            )
            ax.add_patch(circle)
        continue
    zone_angles = zone_angles_list[ii - 1]
    zone_angles = np.append(zone_angles, zone_angles[0] + 2 * np.pi)  # close the loop
    number_of_zones = number_of_zones_list[ii - 1]
    for jj in range(int(number_of_zones)):
        theta_range = np.linspace(zone_angles[jj], zone_angles[jj + 1], 100)
        r_range = np.linspace(radii[ii - 1], radius, 100)
        x_inner = center_x + radii[ii - 1] * np.cos(theta_range)
        y_inner = center_y + radii[ii - 1] * np.sin(theta_range)
        x_outer = center_x + radius * np.cos(theta_range)
        y_outer = center_y + radius * np.sin(theta_range)
        x_range = np.append(x_inner, x_outer[::-1])
        y_range = np.append(y_inner, y_outer[::-1])
        bet = f"{alphabet[ii]}{jj}"
        value = (answers["bet"] == bet).sum()
        print(f"{bet}: {value}")
        value_normalized = value / (values.max())
        color = color_map(value_normalized)
        if value > 0:
            ax.fill(x_range, y_range, color=color, alpha=0.5, zorder=0)

fig.set_size_inches(img.size[0] / 100, img.size[1] / 90)
fig.subplots_adjust(top=1, bottom=1 - img.size[1] / 100 / (img.size[1] / 90), left=0, right=1)

# Setup colorbar
color_map_list = np.array([color_map(i) for i in range(color_map.N)])
color_map_list[:, -1] = 0.7
custom_map = LinearSegmentedColormap.from_list(
    'Custom cmap', color_map_list.tolist(), color_map.N)
bounds = np.linspace(1, values.max() + 1, values.max() + 1)
sm = cm.ScalarMappable(cmap=custom_map, norm=plt.Normalize(vmin=0, vmax=values.max()))
sm.set_array([])
cax = ax.inset_axes([0.05, -0.07, 0.9, 0.045])
cbar = fig.colorbar(sm, orientation="horizontal", cax=cax, boundaries=bounds,
                    ticks=np.arange(0.5, values.max() + 1.5))
cbar.ax.set_xticklabels(np.arange(0, values.max() + 1))
cbar.ax.xaxis.set_tick_params(pad=30)
cbar.ax.set_facecolor('none')
cbar.ax.tick_params(length=0)
cbar.outline.set_edgecolor('white')
cbar.outline.set_linewidth(5)
plt.setp(plt.getp(cbar.ax, 'xticklabels'), color='white', fontsize=50,)


plt.savefig("heatmap.png", facecolor="None")
plt.savefig("heatmap_black.png")
