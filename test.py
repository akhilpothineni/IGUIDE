import re
import numpy as np
import nltk
import spacy
import locationtagger
import geograpy
 
# essential entity models downloads
# nltk.downloader.download('maxent_ne_chunker')
# nltk.downloader.download('words')
# nltk.downloader.download('treebank')
# nltk.downloader.download('maxent_treebank_pos_tagger')
# nltk.downloader.download('punkt')
# nltk.download('averaged_perceptron_tagger')


def regLoc(text):
    regex= r'[0-9A-Za-z]+\s(KeyWest|rd|ave|Street|Avenue|Road|Yard|Lane|Court|Hill|Highwalk|Way|Square|Walk|Park|Underground|Passage|Alley|Close|Gardens|Hall|Circle|Row|Buildings|Crescent|Market|Drive|Arcade|Esplanade|Grove|Garden|Bridge|Ridge|Terrace|Boulevard|Inn|Wharf|St|St.|Ave|Rd|Yd|Ct|Pl|Sq|Bld|Blvd|Cres|Dr|Esp|Grn|Gr|Tce|Bvd|street|avenue|road|yard|lane|court|square|park|underground|building|Wall|wall|crescent|drive|esplanade|garden|bridge|ridge|terrace|boulevard|Building|grove|underground)\b'

    locations = re.finditer(regex,text)
    
    # remove some general references, e.g., "his street", "empty streets", that do not refer to specific locations
    listOfStrings = ['his' , 'the', 'a', 'my', 'never', 'from','in',r'that''s','called','for','to',
                    'at','with','of','minor','own','against','front','that','make','grave','were',
                    'busy','apartment','not','worst','watering','temporary','are','is','and','about',
                    'know','flooded','your','access','service','secret','gotta','whole','this','their',
                    'shit','save','reports','posted','possible','parallel','outside','our','or','observe',
                    'one','on','no','neighbours','multiple','localized','like','its','impacted','her',
                    'hazardous','every','empty','dear','come','by','gotta','of','stop','much','don\'t','reported','before','after']
    
    loc = []
    for m in locations:
        if m.group(0).partition(' ')[0].lower() not in listOfStrings:
            loc.append(m.group().title())
    
    return loc

temp = "I-45 & North Main St A Category 4 #hurricane passed 40 miles South of Key West #otd 1919. The barometric pressure measured at Dry Tortugas was 27.37” and some Some places in the #flkeys had over 13” of rain. The steamer Valbanera was… https://t.co/493hzjrYbR 33 St Texas state"

places = locationtagger.find_locations(text=temp)
# places = geograpy.get_geoPlace_context(text=temp)
hi = regLoc(temp)
splithi = []
for val in hi:
    splithi += val.split()

countries = places.countries
regions = places.regions
cities = places.cities
# print(places.address_strings)

locations = countries + regions + cities
split_locations = []
# for val in locations:
#     split_locations += val.spilt()

tokens = temp.split()
tagged_tokens = [tokens, [0 for i in range(len(tokens))]]

for i, token in enumerate(tokens):
    if token in splithi or token in locations:
        tagged_tokens[1][i] = 1

if tagged_tokens[1][0] == 1:
    tokens[0] = tokens[0] + '   B-Location'

for i in range(1, len(tagged_tokens[0])):
    if tagged_tokens[1][i-1] == 1:
        tokens[i] = tokens[i] + '   I-Location'
    elif tagged_tokens[1][i] == 1:
        tokens[i] = tokens[i] + '   B-Location'

print(np.matrix(tagged_tokens))
print(splithi)
print(locations)
print(tokens)