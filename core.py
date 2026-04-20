import geopandas as gpd
import numpy as np
from shapely.geometry import box
import pandas as pd

# Add webservice or dataset to automatically get the parcel boundaries
# Smoothen out how did i do it?
# Add input field for the output file

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

        if not hasattr(self, "custom_bins"):
            min_value = self.data[self.target_column].min()
            max_value = self.data[self.target_column].max()

            self.custom_bins = np.linspace(min_value, max_value, 6)

        self.zones["class"] = pd.cut(
            self.zones[self.target_column],
            bins=self.custom_bins,
            include_lowest=True
        )
    def add_rate(self):
        """Assign rates to each row based on class intervals."""
        if not hasattr(self, "rates"):
            return
        
        intervals = self.zones["class"].cat.categories
        rate_mapping = dict(zip(intervals, self.rates))
        self.zones["rate"] = self.zones["class"].map(rate_mapping)


    def dissolve_per_class(self):
        # Ensure class and rate columns exist in original data
        if 'class' not in self.zones.columns or 'rate' not in self.zones.columns:
            raise ValueError("Missing 'class' or 'rate' column.")

        # Dissolve by class, keeping the first rate (all rates per class are identical)
        gdf = self.zones.dissolve(by='class', aggfunc={'rate': 'first'})
        
        # Explode multipolygons into single parts
        gdf = gdf.explode(ignore_index=True)
        
        # Add unique ID for each polygon (starting from 1)
        gdf['id'] = range(1, len(gdf) + 1)
        
        # Select desired columns: id, rate, geometry
        gdf = gdf[['id', 'rate', 'geometry']]
        
        # Handle CRS before export
        if gdf.crs is None:
            # Set appropriate CRS (e.g., EPSG:28992 for RD New in Netherlands)
            gdf = gdf.set_crs(epsg=28992)
        
        # Export to WGS84 shapefile
        gdf.to_crs(epsg=4326).to_file(r"C:\Users\adria\Downloads\jef deelen tegenover erf bestanden\Data\kaartje.shp")


    def create_taskmap(self):
        self.create_grid()
        self.join_by_nearest(self.grid, self.data)
        self.get_target_columns()
        self.create_classes()
        self.add_rate()
        self.dissolve_per_class()


    # Finish later for now join by nearest can work as well
    def idw_interpolation(self, known_points, known_values, query_points, power=2):
        """
        known_points: array of shape (n, 2) with x, y coordinates
        known_values: array of shape (n,) with values at known points
        query_points: array of shape (m, 2) with points to interpolate
        power: IDW power parameter (default=2)
        """
        results = []
        for qp in query_points:
            distances = np.sqrt(np.sum((known_points - qp) ** 2, axis=1))
            
            # If query point coincides with a known point, return its value
            if np.any(distances == 0):
                results.append(known_values[distances == 0][0])
                continue
            
            weights = 1 / distances ** power
            interpolated = np.sum(weights * known_values) / np.sum(weights)
            results.append(interpolated)
        
        return np.array(results)
    



# data_path = r"C:\Users\adria\Downloads\jef deelen tegenover erf bestanden\Data\data.shp"
# boundary_path = r"C:\Users\adria\Downloads\cropfields_49058_20260410_194726\export.shp"
# test = Core(data_path, boundary_path)

# test.create_taskmap()