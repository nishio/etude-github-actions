# Export from Scrapbox(/nishio to data.json)
./export_from_scrapbox.sh

# Translate (data.json to data_en.json)
python translate.py

# Make diff (data_en.json and nishio/data_en_prev.json to data_en_diff.json)
python diff_json.py

# Import to Scrapbox(data_en_diff.json to /nishio-en)
./import_to_scrapbox.sh

# store previous data
mv data.json nishio
mv data_en.json nishio/data_en_prev.json

# Commit files
./commit.sh
