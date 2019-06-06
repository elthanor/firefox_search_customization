#!/bin/env bash
set -x
MOZPATH=${HOME}/.mozilla/firefox/*.default
./unmozlz4 ${MOZPATH}/search.json.mozlz4 ./temp
#sed 's/duckduckgo.com\/?q={searchTerms}/&\&kaj=m\&k1=-1\&kam=osm\&kae=t\&kg=p\&k5=1/' ./temp > ./temp2
#cat temp | sed 's/"duckduckgo.com","params":\[{"name":"q","value":"{searchTerms}"}/"duckduckgo.com","params":\[{"name":"q","value":"{searchTerms}"},{"name":"kaj","value":"m"},{"name":"k1","value":"-1"},{"name":"kam","value":"osm"},{"name":"kae","value":"t"},{"name":"kg","value":"p"},{"name":"k5","value":"1"}/' > temp2
cat temp | sed 's|{"template":"https://duckduckgo.com/?q={searchTerms}\&t=canonical","rels":\[\],"resultDomain":"duckduckgo.com","params":\[\]}|{"template":"https://duckduckgo.com","rels":\[\],"resultDomain":"duckduckgo.com","method":"POST","params":\[{"name":"q","value":"{searchTerms}"},{"name":"kae","value":"t"},{"name":"k1","value":"-1"},{"name":"kam","value":"osm"},{"name":"kg","value":"p"},{"name":"k5","value":"1"},{"name":"kaj","value":"m"}\]}|g' > temp2
./mozlz4 ./temp2 ./search.json.mozlz4
mv search.json.mozlz4 ${MOZPATH}
rm temp temp2
