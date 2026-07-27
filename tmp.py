import json, addfips
af = addfips.AddFIPS()

with open("static/data/radon_zones-spreadsheet.json", "r") as file:
    data = json.load(file)

for state, counties in data["filtered-raw-data"].items():
    mapped_counties = []
    for county in counties:
        county["FIPS"] = af.get_county_fips(county["COUNTY LABEL"].strip().replace("COUNTY", ""), state=state)
        mapped_counties.append(county)
    data["filtered-raw-data"][state] = mapped_counties

with open("static/data/radon_zones-spreadsheet.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)

