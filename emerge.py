import pandas as pd
primary = pd.read_excel("DOB Primary.xlsx")
parking = pd.read_excel("Parking Structure Inspection_2025.xlsx")
local88 = pd.read_excel("Local Law 88_2025.xlsx")
local97 = pd.read_excel("Local Law 97_2025.xlsx")

primary = primary[[
    "CYCLE", "SUBCYCLE", "BIN", "HOUSE_NO", "STREET_NAME", "BOROUGH", "BLOCK", "# Floors", 
    "Year Built", "Approx. SF", "Landmark", "Parking Garage", "CURRENT_STATUS", "OWNER_NAME",
    "PRIOR_CYCLE_FILING_DATE", "PRIOR_STATUS", "COMMENTS"
]]

parking = parking[[
    "Filing Status", "House Number", "Street Name", "BIN", "Block", "Borough", "Owner Name", 
    "UNSAFE / SREM Completion Date", "Effective Filing Date", "DOF Bldg Classification Description",
    "Report Status", "Filing Name", "DOF Owner Name", "Initial Filing Status"
]]

# renaming the columns especially BIN so we can merge on it
local88 = local88[["BIN (DOB Records)"]].rename(columns={"BIN (DOB Records)": "BIN"})
local88["LL88 Compliance Status"] = "Covered"
local88["LL88 Filing Due"] = ""
local88["LL88 Notes"] = ""

local97 = local97[["Preliminary BIN"]].rename(columns={"Preliminary BIN": "BIN"})
local97["LL97 Compliance Status"] = "Covered"
local97["LL97 Filing Due"] = ""
local97["LL97 Next Steps"] = ""

# Rename Parking columns
parking = parking.rename(columns={
    "DOF Bldg Classification Description": "Use Type",
    "Filing Status": "LL126 Compliance Status",
    "Initial Filing Status": "LL126 Previous Filing Status",
    "UNSAFE / SREM Completion Date": "LL126 SREM Recommended Date",
    "Effective Filing Date": "LL126 Filing Window",
    "Report Status": "LL126 Next Steps",
    "Filing Name": "LL126 Notes / Budget Request",
    "Owner Name": "Building Owner/Manager",
    "House Number": "HOUSE_NO",
    "Street Name": "STREET_NAME",
    "Block": "BLOCK",
    "Borough": "BOROUGH"
})

# Merge files on BIN ---
merged = primary.merge(parking, on="BIN", how="left")
merged = merged.merge(local88, on="BIN", how="left")
merged = merged.merge(local97, on="BIN", how="left")
