# 3DSlicer_open_mrb_extract_markup_info
Example functions to retrieve markup information from 3D Slicer .mrb files

# Functions available:

1. open_file_get_points_fcsv
    - extracts **point coordinates** if file in .mrb is .fcsv
 
2. open_file_get_points
    - extracts **point coordinates** from .mrk.json
 
3. open_file_get_length
    - extracts **length** from .mrk.json
  
4. open_file_get_area
    - extracts **area** from .mrk.json

5. open_file_get_angle
    - extracts **angle** from .mrk.json
    
## Example code
open_mrb_get_markup_info_pseudocode.py

Has example with for loop that opens all .mrb files in folder and saves markup information into dictionary and dataframe
