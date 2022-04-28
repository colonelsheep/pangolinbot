import sys
import pywikibot
from pywikibot import pagegenerators

#property to update
p = sys.argv[1]
#old property value to look for
old_v = sys.argv[2]
#new property value to replace with
new_v = sys.argv[3]

print("Replacing " + p + " = " + old_v + " with " + new_v)
wd_connect = pywikibot.Site('wikidata', 'wikidata')

wd = wd_connect.data_repository()
wd_old_v = pywikibot.ItemPage(wd, old_v)
wd_new_v = pywikibot.ItemPage(wd, new_v)

#creates query to find all items with property has incorrect value
def property_finder_query(p, v):
    query = 'SELECT distinct ?item WHERE {?item wdt:' + p + ' wd:' + v + '.}'
    return query

#gets all articles with property and incorrect value
def get_articles(query):
    generator = pagegenerators.WikidataSPARQLPageGenerator(query, site=wd)
    for page in generator:
        replace_property(page)

#replaces old property value with new property value
def replace_property(page):
    wd_info = page.get()
    print('Replacing property in: ' + page.title() + ' (' + wd_info['labels']['en'] + ')')
    for claim in wd_info['claims'][p]:
        #if old property value found
        if claim.getTarget() == wd_old_v:
            try:
                #replace with new property value
                claim.changeTarget(wd_new_v, summary='Replaced ' + wd_old_v.title() + ' with ' + wd_new_v.title())
            #this means the new property value is already in the page
            except:
                print(wd_new_v.title() + ' already in properties. Deleting old property instead.')
                #remove old property value
                page.removeClaims(claim, summary='removed invalid property value')

query = property_finder_query(p, old_v)
get_articles(query)
