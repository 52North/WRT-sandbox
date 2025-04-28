import os
import json
from ipyleaflet import Map, GeoJSON, Popup
from IPython.display import display
import matplotlib.pyplot as plt
from map_marker_popup import add_geojson_to_map

'''colours = ['#0072B2', '#D55E00', '#009E73', '#CC79A7', '#F0E442',
               '#56B4E9', '#006BA4', '#ABABAB', '#595959', '#FFBC79']

def plot_power_vs_dist(rp_list, rp_str_list, scenario_str, power_type='fuel'):
    fig, ax = plt.subplots(figsize=(12, 8), dpi=96)
    for irp in range(0, len(rp_list)):
        rp_list[irp].plot_power_vs_dist(colours[irp], rp_str_list[irp], power_type, ax)

    ax.legend(loc='upper left', frameon=False)
    # ax.tick_params(top=True, right=True)
    ax.tick_params(labelleft=False, left=False, top=True)   # hide y labels
    ax.text(0.95, 0.96, scenario_str, verticalalignment='top', horizontalalignment='right',
            transform=ax.transAxes)
    plt.savefig('Images-WRT' + '/' + power_type + '_vs_dist.png')

filename1="min_time_route.json"
rp_read1 = RouteParams.from_file(filename1)
rp_str1 ='speedy isobased' 
scenario_str = 'scenario: Mediterranean Sea'
rp_list=[rp_read1]
rp_str_list=[rp_str1]

plot_power_vs_dist(rp_list, rp_str_list, scenario_str, power_type='fuel')'''
m = Map(center=[39.926688, 7.930542], zoom=5.5)

with open("min_time_route.json") as f:
    data = json.load(f)

add_geojson_to_map(data, m)

display(m)