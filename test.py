import urllib.request, csv, pgeocode
nomi = pgeocode.Nominatim("us")

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTQ8bNIWD28VlL1RrDLiXcjPUT0GJwcnWg8A7HU0vff9r7QXU_VqJvNy1ucKxgvLQQnbajovpDc4xOH/pub?output=csv"
response = urllib.request.urlopen(url)
lines = [line.decode('utf-8') for line in response.readlines()]

reader = csv.DictReader(lines)
mapped_data = []
for row in enumerate(reader):
    zip_code = str(row[1]["Postal Code"]).strip()
    location = nomi.query_postal_code(zip_code)
    current = row[1]
    current.pop("City / Town")
    current["County"] = location.county_name
    mapped_data.append(current)
print(mapped_data)