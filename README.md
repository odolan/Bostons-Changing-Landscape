# Boston's Changing Landscape
#### **Project Goal:** Studying the extent to which a 1965-75 General Use Plan for Boston has been fulfilled, and how it has impacted the city landscape
#### Project [live demo link](https://odolan.github.io/Bostons-Changing-Landscape/)   <------------- This link lets you try it out for yourself!

### Main Features
1. This project lets you interact with [this 1965-75 General Use Plan](https://collections.leventhalmap.org/search/commonwealth:6q185466n) for Boston
where you can hover over neighborhoods to view more information about how the residents and community of the neighborhoods have and how they have 
developed both the way the general plan provides and not.
2. You can turn on and off map layers, to see the individual contributions of each of 5 zoned areas in Boston:
    - **Residential**
    - **Commercial**
    - **Industrial**
    - **Institutional**
    - **Public/Open Space**
<div>
  <img src="/project_images_for_documentation/screenshot7.png" width="500">
  <img src="/project_images_for_documentation/screenshot8.png" width="500">
</div>

##### ____________________________________________________________________________________________________
## Project Progression

### 1. Two image preperation tasks: taking the original map image and editing out extra areas using photoshop + georeferencing the image using [QGIS](https://qgis.org/en/site/)
<div>
  <img src="/project_images_for_documentation/screenshot6.png" width="200">
  <img src="/project_images_for_documentation/screenshot2.png" width="200">
  <img src="/project_images_for_documentation/screenshot4.png" width="200">
  <img src="/project_images_for_documentation/screenshot1.png" width="200">
</div>

### 2. Image masking techniques
```
#bluring the image, to smooth over photo imperfections
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
kernel = np.ones((15,15),np.float32)/25
gray = cv2.filter2D(gray,-1,kernel)

#detect contours/shapes in the image   
ret, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_OTSU)
#find the contours in the image
contours, heirarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
#creates all black image --> changes it to have white pixels equal color of choice 
threshold_shape = thresh.shape
color_img = np.zeros((threshold_shape[0], threshold_shape[1], 3), dtype = np.uint8)
color_img[np.where(thresh == 255)] = bgr_color
```
Using python image processing to create masks for different pixel values. This let me exctract each of the color values masks. 
```
#sets a low and high range color value to isolate for in mask
low = np.array(color_bounds_low)
high = np.array(color_bounds_high)
mask = cv2.inRange(hsv, low, high)
result_image = cv2.bitwise_and(img, img, mask=mask)
```
<div>
  <img src="/isolated_color_masks/blue_mask.tif" width="180">
  <img src="/isolated_color_masks/green_mask.tif" width="180">
  <img src="/isolated_color_masks/orange_mask.tif" width="180">
  <img src="/isolated_color_masks/purple_mask.tif" width="180">
  <img src="/isolated_color_masks/red_mask.tif" width="180">
</div>

### 3. Adding the georefferenced points to each of the masks, making each raster a stand-alone and geo-rich

### 4. Using [display_maps.py](display_maps.py) we read in each of the masks one by one adding a folium layer
```
# Define function to add GeoTIFF image overlay to folium map
def add_raster_to_map(src, color, layer_name, m):
    # Get image dimensions and coordinates
    xmin, ymin, xmax, ymax = src.bounds

    # Read image data
    raster = src.read(1)

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
```
read in each of the masks and apply the above code
```
image_names = ['public open space', 'institutional/public', 'commercial', 'industrial', 'residential']
geotiff_colors = [(0, 128, 0), (0, 0, 128), (0, 128, 128), (128, 0, 0), (128, 128, 0)]
image_paths = ['geo_color_masks/geo_green_mask.tif', 
                 'geo_color_masks/geo_blue_mask.tif', 
                 'geo_color_masks/geo_red_mask.tif', 
                 'geo_color_masks/geo_purple_mask.tif', 
                 'geo_color_masks/geo_orange_mask.tif']
```

### 5. Add neighborhood layer on top of folium as new layer
```
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
```

One of the nice things I have foind working with folium is that it produces an html site automatically as an output. Once processing the images the rest of the project
inovolved adding information on hover with the tooltip argument seen above. This produces different values from the neighborhood JSON.

In conclusion this was a very valuable project for me. I learned several new techiniques including:
  - **Parsing python strings as html**
  - **Producing folium webpages with intractive map layers**
  - **How to georeference data**

