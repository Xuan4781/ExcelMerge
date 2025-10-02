import pandas as pd
primary = pd.read_excel("DOB Primary")
parking = pd.read_excel("Parking Structure Inspection_2025")
local88 = pd.read_excel("Local Law 88_2025")
local97 = pd.read_excel("Local Law 97_2025")

primary = primary[[
    "CYCLE", "SUBCYCLE", "HOUSE_NO", "STREET_NAME", "BOROUGH", "BLOCK", "# Floors", "Year Built",
    "Approx. SF", "Landmark", "Parking Garage", "CURRENT_STATUS", "OWNER_NAME",
    "PRIOR_CYCLE_FILING_DATE", "PRIOR_STATUS", "COMMENTS"
]]

parking = parking[[



    
]]
