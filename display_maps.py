import rasterio
import folium
import json



def create_popup():
    popup_text = f"""
        <h1>Hello World🐒</h1>
    """
    popup_html = folium.Html(popup, script=True)
    popup = folium.GeoJsonPopup(popup_html, max_width=500)
    return popup_text

# function to add neighborhoods to folium map
def add_neighborhoods(m):
    with open('Boston_Neighborhoods.geojson', 'r') as f:
        geojson_data = json.load(f)

        folium.GeoJson(
            geojson_data,
            tooltip = folium.features.GeoJsonTooltip(
                fields=['Name', 'People', 'Changing_Times', 'Map_Changes'], 
                aliases=['Neighborhood', '🧍Community', '⏱️Changes', '🗺️Changes'], 
                labels=True, 
                feature='mouseover', 
                style=("background-color: white; color: #333333; font-family: arial; font-size: 16px; padding: 5px; border-radius:10px; width: 500px; white-space: pre-wrap; z-index: 1500;")
            ),
            name='Boston Neighborhoods',
            style_function=lambda feature: {
                'fillColor': '#008080', 
                'color': '#000000', 
                'weight': 1, 
                'fillOpacity': 0.4
            },
            highlight_function=lambda feature: {
                'fillColor': '#00FF00',
                'color': '#000000',
                'weight': 2,
                'fillOpacity': 0.1
            },
        ).add_to(m)

# Define function to add GeoTIFF image overlay to folium map
def add_raster_to_map(src, color, layer_name, m):
    # Get image dimensions and coordinates
    xmin, ymin, xmax, ymax = src.bounds

    # Read image data
    raster = src.read(1)
    #rgb_raster = np.dstack((raster, raster, raster, raster))

    #colormap=lambda x: (128, 0, 128, x), 

    # Add GeoTIFF image overlay to map
    folium.raster_layers.ImageOverlay(
        image=raster,
        bounds=[[ymin, xmin], [ymax, xmax]],
        opacity=0.8,
        interactive=True,
        cross_origin=False,
        colormap=lambda x: (color[0], color[1], color[2], x), 
        name=layer_name
    ).add_to(m)

# Define array of image paths

image_names = ['public open space', 'institutional/public', 'commercial', 'industrial', 'residential']
geotiff_colors = [(0, 128, 0), (0, 0, 128), (0, 128, 128), (128, 0, 0), (128, 128, 0)]
image_paths = ['geo_color_masks/geo_green_mask.tif', 
                 'geo_color_masks/geo_blue_mask.tif', 
                 'geo_color_masks/geo_red_mask.tif', 
                 'geo_color_masks/geo_purple_mask.tif', 
                 'geo_color_masks/geo_orange_mask.tif']

# image_names = ['public open space',]
# geotiff_colors = [(128, 128, 0)]
# image_paths = ['geo_color_masks/geo_green_mask.tif', ]

# Create folium map centered on first image coordinates
with rasterio.open(image_paths[0]) as src:
    m = folium.Map(location=[(src.bounds[1]+src.bounds[3])/2, (src.bounds[0]+src.bounds[2])/2], zoom_start=10)

# Add GeoTIFF image overlays to map
for i, path in enumerate(image_paths):
    with rasterio.open(path) as src:
        add_raster_to_map(src, geotiff_colors[i], image_names[i], m)  

add_neighborhoods(m)
folium.LayerControl().add_to(m)

#creates title card at the top 
html = """
<div style="position: absolute; width:100%; z-index:1000; text-align:center;">">
    <div style="display:inline-block; justify-content:center; background-color:white; margin-top:10px; width:50%; border-radius:10px;">
        <h3>Boston's Changing Landscape</h3>
        <p>To what extent has a<a href="https://collections.leventhalmap.org/search/commonwealth:6q185466n">1965-75 General Use Plan</a> for Boston been fulfilled, and how has it changed the city landscape</p>
    </div>
</div>
"""
card_div = folium.Element(html)
m.get_root().html.add_child(card_div)

html = """
<div style="position: absolute; bottom: 20px; right: 10px; width: 400px; height: 300px; margin: 10px; border-radius: 10px; background-color: white; padding:10px; overflow: hidden; z-index: 1000; overflow-y:auto">
    <h3>Information</h3>
    <p style="font-weight: 500;">A project for Bostonography by Owen Dolan<p>
    <div style="padding-left:10px;">
        <p>⭐️ Hover over a neighborhood to see its name, community features, changes since 1960, and differences on general use map</p>
        <p>⭐️ I highly suggest playing around with addding or removing different layers (press the layer button in the top right of the screen)</p>
        <p style="font-weight: 500;">Credit</p>
        <div style="padding-left:10px;">
            <p>-<a href="https://collections.leventhalmap.org/search/commonwealth:6q185466n">1965-75 General Use Plan</a></p>
            <p>-<a href="https://python-visualization.github.io/folium/">Folium for Python</a></p>
            <p>-<a href="https://pypi.org/project/osgeo/">Python Geo Data</a></p>
            <p>-<a href="https://www.boston.gov/neighborhoods">Boston Neighborhood Descriptions</a></p>
            <p>-<a href="https://data.boston.gov/dataset/boston-neighborhoods/resource/60b0a93d-ac1a-4caa-9cc0-91c23717d84f">Boston GeoJson Neighborhoods</a></p>
            <p>-<a href="https://theculturetrip.com/north-america/usa/massachusetts/boston/articles/a-guide-to-bostons-23-neighborhoods/">A guide to Boston's neighborhoods</a></p>
            <p>-<a href="https://www.bostonbackbay.com/about-back-bay/history/">Back Bay info</a></p>
            <p>-<a href="https://localhistories.org/a-history-of-dorchester/">Dorchester Info</a></p>
            <p>-<a href="https://globalboston.bc.edu/index.php/home/immigrant-places/roxbury/">Roxbury Info</a></p>
            <p>-<a href="https://globalboston.bc.edu/index.php/home/immigrant-places/east-boston/">East Boston Info</a></p>
            <p>-<a href="https://globalboston.bc.edu/index.php/home/immigrant-places/east-boston/">Roslindale Info</a></p>
            <p>-<a href="https://globalboston.bc.edu">Rest of the Boston neighborhoods</a></p>
        </div>
    </div>
</div>
"""
card_div = folium.Element(html)
m.get_root().html.add_child(card_div)

# Display map
m.save('map.html')  # Save map to HTML file
