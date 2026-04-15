import geopandas as gpd
import numpy as np
from shapely.geometry import box
import pandas as pd

# Add webservice or dataset to automatically get the parcel boundaries
# Connect rate to class
# Only output the rates and class
# Smoothen out how did i do it?
# IDW --> Contour polygons? could be a simple solution 
class Core:
    def __init__(self, data, boundary=None):
        self.data = gpd.read_file(data).set_crs(epsg=4326)
        self.boundary = gpd.read_file(boundary).to_crs(epsg=28992)
    
    def create_grid(self):
        cell_size = 1
        
        minx, miny, maxx, maxy = self.boundary.total_bounds
        
        x_coords = np.arange(minx, maxx, cell_size)
        y_coords = np.arange(miny, maxy, cell_size)
        
        cells = []
        for x in x_coords:
            for y in y_coords:
                cells.append(box(x, y, x + cell_size, y + cell_size))
        
        self.grid = gpd.GeoDataFrame(geometry=cells, crs=self.boundary.crs)
        return 

    def join_by_nearest(self, zones, data):
        data = data.to_crs(epsg=28992)
        self.zones = gpd.sjoin_nearest(zones, data, how="left")
        self.zones = self.zones.clip(self.boundary)
        return self.zones
    
    def get_target_columns(self):
        target_columns = self.data.columns
        # insert tkinter pop up to choose target column and classes

        self.target_column = "Org._stof"

    def create_classes(self):
        # insert standard options comparable to dacom equal interval, etc and 5% increase add variable amount of classes
        amount_of_classes = 5
        min_value = self.data[self.target_column].min()
        max_value = self.data[self.target_column].max()

        bins = np.linspace(min_value, max_value, 6)

        self.zones["class"] = pd.cut(
            self.zones[self.target_column],
            bins=bins,
            labels=[1, 2, 3, 4, 5],
            include_lowest=True
        )

    def dissolve_per_class(self):
        gdf = self.zones.dissolve(by='class')
        gdf.to_crs(epsg=4326).to_file(r"C:\Users\adria\Downloads\jef deelen tegenover erf bestanden\Data\kaartje.shp")

    def create_taskmap(self):
        self.create_grid()
        self.join_by_nearest(self.grid, self.data)
        self.get_target_columns()
        self.create_classes()
        self.dissolve_per_class()

data_path = r"C:\Users\adria\Downloads\jef deelen tegenover erf bestanden\Data\data.shp"
boundary_path = r"C:\Users\adria\Downloads\cropfields_49058_20260410_194726\export.shp"
test = Core(data_path, boundary_path)

test.create_taskmap()