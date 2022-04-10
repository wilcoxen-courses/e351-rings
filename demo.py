"""
demo.py
Spring 2022 PJW

Demonstrate spatial joins using geopandas.
"""

import geopandas as gpd
import matplotlib.pyplot as plt

#
#  Set up a function for generating quick plots showing results
#

def plot_it(geodf,col,title,show_inter=False):

    #  Summarize the join
    
    print( geodf[col].value_counts(dropna=False) )
    
    #  Set up the figure
    
    fig,ax1 = plt.subplots(dpi=300)
    
    #  Plot the data using the given column for coloring 
    
    geodf.plot(col,edgecolor='black',linewidth=0.5,ax=ax1)
    
    #  Plot the count background and county and zip boundaries for reference
    
    county.plot(color='xkcd:ivory',alpha=0.4,ax=ax1)
    county.boundary.plot(color='black',linewidth=0.25,ax=ax1)
    zip_all.boundary.plot(color='black',linewidth=0.25,ax=ax1)
    
    #  Plot the interstates for reference
    
    if show_inter:
        inter.plot(color='black',ax=ax1)
    
    #  Add a title and turn off the axis
    
    ax1.set_title(title)
    ax1.axis('off')
    
    fig.tight_layout()
    
#%%
#
#  Now read the data
#

demo_file = 'demo.gpkg'

zips = gpd.read_file('demo.gpkg',layer='zips')
county = gpd.read_file('demo.gpkg',layer='county')
inter = gpd.read_file('demo.gpkg',layer='interstates')

print( 'Zips:', len(zips) )

#
#  Make a dissolved version of the zip layer for plotting
#

zip_all = zips.dissolve()

#%%
#
#  Intersects
#

z_intersect_c = zips.sjoin(county,how='left',predicate='intersects')
plot_it(z_intersect_c,'COUNTYFP','Z intersects C')

#%%
#
#  Overlaps
#

z_overlaps_c = zips.sjoin(county,how='left',predicate='overlaps')
plot_it(z_overlaps_c,'COUNTYFP','Z overlaps C')

#%%
#
#  Contains
#

c_contains_z = county.sjoin(zips,how='right',predicate='contains')
plot_it(c_contains_z,'COUNTYFP','C contains Z')

#%%
#
#  Within
#

z_within_c = zips.sjoin(county,how='left',predicate='within')
plot_it(z_within_c,'COUNTYFP','Z within C')

#%%     
#
#  Touches
#

z_touch_c = zips.sjoin(county,how='left',predicate='touches')
plot_it(z_touch_c,'COUNTYFP','Z touches C')

#%%
#
#  Crosses
#

i_crosses_z = inter.sjoin(zips,how='right',predicate='crosses')
plot_it(i_crosses_z,'RTTYP','I crosses Z',show_inter=True)
