import sys
import pywikibot
from pywikibot import pagegenerators

p = sys.argv[1]
old_v = sys.argv[2]
new_v = sys.argv[3]
print("Replacing " + p + " = " + old_v + " with " + new_v)
wd_connect = pywikibot.Site('wikidata', 'wikidata')
wd = wd_connect.data_repository()
wd_old_v = pywikibot.ItemPage(wd, old_v)
wd_new_v = pywikibot.ItemPage(wd, new_v)

def replace_wikidata(wd_item, p, v):
    target = pywikibot.ItemPage(wd, v)
    claim = pywikibot.Claim(wd, p)
    claim.setTarget(target)


def property_finder_query(p, v):
    query = 'SELECT distinct ?item WHERE {?item wdt:' + p + ' wd:' + v + '.} LIMIT 10'
    return query

def get_articles(query):
    generator = pagegenerators.WikidataSPARQLPageGenerator(query, site=wd)
    for page in generator:
        replace_property(page)

def replace_property(page):
    wd_info = page.get()
    print('Replacing property in: ' + page.title() + ' (' + wd_info['labels']['en'] + ')')
    for claim in wd_info['claims'][p]:
        if claim.getTarget() == wd_old_v:
            try:
                claim.changeTarget(wd_new_v, summary='Replaced ' + wd_old_v.title() + ' with ' + wd_new_v.title())
            except:
                print(wd_new_v.title() + ' already in properties. Deleting old property instead.')
                page.removeClaims(claim, summary='removed invalid property value')
query = property_finder_query(p, old_v)
get_articles(query)
