import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib.patches import Circle

img = Image.open("target.jpg")
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

fig, ax = plt.subplots(figsize=(img.size[0] / 100, img.size[1] / 100), facecolor="black")
fig.subplots_adjust(left=0, bottom=0, right=1, top=1)
plt.imshow(img, cmap="gray", interpolation="none")

ax.set_xlim(0, img.size[0])
ax.set_ylim(img.size[1], 0)
ax.set_axis_off()

center_x = img.size[0] / 2
center_y = img.size[1] / 2
center_coords = (center_x, center_y)
max_radius = min(img.size[0], img.size[1]) / 2

radii = np.linspace(0, max_radius, 7)
radii = radii[1:]

center_circle_area = np.pi * radii[0] ** 2
previous_circle_area = center_circle_area

zone_angles_list = []
number_of_zones_list = []
for ii, radius in enumerate(radii):
    circle = Circle(
        center_coords,
        radius=radius,
        edgecolor="white",
        facecolor="none",
        linewidth=5,
    )
    ax.add_patch(circle)
    if ii == 0:
        ax.text(
            center_x,
            center_y,
            alphabet[ii],
            color="white",
            ha="center",
            va="center",
            fontsize=50,
            fontweight="bold",
        )
        continue
    circle_area = np.pi * radius**2
    segment_area = circle_area - previous_circle_area
    number_of_zones = np.ceil(segment_area / center_circle_area)
    number_of_zones_list.append(number_of_zones)
    zone_angles = np.linspace(0, 2 * np.pi, int(number_of_zones), endpoint=False)
    if number_of_zones % 2 == 0:
        zone_angles += np.pi
    elif ii % 2 == 0:
        zone_angles += np.pi / 2
    else:
        zone_angles -= np.pi / 2
    zone_angles_list.append(zone_angles)
    text_angles = zone_angles + np.pi / number_of_zones
    for angle in zone_angles:
        x_range = [
            center_x + radius * np.cos(angle),
            center_x + radii[ii - 1] * np.cos(angle),
        ]
        y_range = [
            center_y + radius * np.sin(angle),
            center_y + radii[ii - 1] * np.sin(angle),
        ]
        ax.plot(x_range, y_range, color="white", linewidth=5)
    for jj, angle in enumerate(text_angles):
        x_text = center_x + (radius + radii[ii - 1]) / 2 * np.cos(angle)
        y_text = center_y + (radius + radii[ii - 1]) / 2 * np.sin(angle)
        ax.text(
            x_text,
            y_text,
            f"{alphabet[ii]}{jj}",
            color="white",
            ha="center",
            va="center",
            fontsize=50,
            fontweight="bold",
        )
    previous_circle_area = circle_area

plt.savefig("grid.png", facecolor="None")
