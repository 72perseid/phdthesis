#!/bin/sh
# Builds the database from nothing, loads the three pilot papers and runs every check.
# Output: out/fieldwork.sqlite, out/*.ttl, out/view/*.csv. Run from any folder.
cd "$(dirname "$0")"
PY=../.venv/bin/python
DB=out/fieldwork.sqlite
mkdir -p out
echo "== build"
$PY db/fieldwork_db.py init $DB
echo "== load the three papers"
$PY db/from_v1.py $DB ../v1/cidoc/data/seleukeia_sidera_2024.json ../v1/cidoc/data/yumuktepe_2024.json ../v1/cidoc/data/sinekkaya_2024.json
echo "== check"
$PY db/fieldwork_db.py check $DB
echo "== audit"
$PY db/fieldwork_db.py audit $DB
echo "== levels, own codes not linked"
$PY db/fieldwork_db.py levels $DB
echo "== levels, after linking own codes to standard codes"
$PY db/fieldwork_db.py link $DB db/pilot_links.csv
$PY db/fieldwork_db.py levels $DB
echo "== graphs and views"
for d in seleukeia-sidera-2024 yumuktepe-2024 sinekkaya-2024; do
  $PY db/fieldwork_db.py graph $DB -d $d -o out/$d.ttl
  $PY db/fieldwork_db.py view $DB $d -o out/view
done
echo "== tests on a fresh copy"
$PY db/test_db.py
