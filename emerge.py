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



# Creating Address from house_NO and Streename + cycle & subcycle
merged["Address"] = merged["HOUSE_NO"].astype(str) + " " + merged["STREET_NAME"]
merged["FISP Cycle"] = merged["CYCLE"].astype(str) + " / " + merged["SUBCYCLE"].astype(str)

# renamed primary 
merged = merged.rename(columns={
    "CURRENT_STATUS": "FISP Compliance Status",
    "PRIOR_STATUS": "FISP Last Filing Status",
    "PRIOR_CYCLE_FILING_DATE": "FISP Cycle Filing Window",
    "COMMENTS": "FISP Notes / Budget Request",
    "# Floors": "M Floors",
    "Approx. SF": "Approx Sq Ft",
    "OWNER_NAME": "Building Owner/Manager"
})




# For remaining headers, have empty columns
for col in [
    "LL126 Cycle", "LL126 Filing Window", "LL126 Parapet Compliance Status", "LL126 Parapet Notes",
    "LL84 Compliance Status", "LL84 Filing Due", "LL84 Next Steps",
    "LL87 Compliance Status", "LL87 Filing Due", "LL87 Compliance Year", "LL87 Next Steps",
    "Contact Email", "Contact Phone"
]:
    if col not in merged.columns:
        merged[col] = ""

# Reordering headers
final_headers = [
    "Address","Building Owner/Manager","Use Type","Block","BIN","Borough","Year Built",
    "M Floors","Approx Sq Ft","Landmark","Parking Garage","FISP Compliance Status",
    "FISP Cycle","FISP Last Filing Status","FISP Cycle Filing Window","FISP Next Steps","FISP Notes / Budget Request",
    "LL126 Compliance Status","LL126 Cycle","LL126 Previous Filing Status","LL126 SREM Recommended Date",
    "LL126 Filing Window","LL126 Next Steps","LL126 Notes / Budget Request","LL126 Parapet Compliance Status",
    "LL126 Parapet Notes","LL84 Compliance Status","LL84 Filing Due","LL84 Next Steps","LL87 Compliance Status",
    "LL87 Filing Due","LL87 Compliance Year","LL87 Next Steps","LL88 Compliance Status","LL88 Filing Due",
    "LL88 Notes","LL97 Compliance Status","LL97 Filing Due","LL97 Next Steps","Contact Email","Contact Phone"
]

merged = merged[final_headers]


merged.to_excel("final_merged.xlsx", index=False)

