import argparse
import os
import feedparser
import igparser
from fhirclient import client
import fhirclient.models.codesystem as cs
import fhirclient.models.valueset as vs
import fhirclient.models.conceptmap as cm

    
def create_client(endpoint):
    settings = {
        'app_id': 'server_config',
        'api_base': endpoint
    }
    smart = client.FHIRClient(settings=settings)
    return smart


def get_valuesets(args,smart):
    """
      Create a tsv file of ValueSets for import into Confluence from the ontoserver
    """
    outfile = os.path.join(args.outdir,'ValueSets.txt')    
    if os.path.exists(outfile):
        os.remove(outfile)
    vs_dict = igparser.main(args.outdir)    
    endpoint=args.endpoint
    query = smart.prepare()
    if not query:
        print("Server is not ready: {0}".format(endpoint))
        return None
    vs_search=vs.ValueSet.where(struct={})
    vs_list = vs_search.perform_resources(smart.server)
    with open(outfile, "w") as f:
        f.write("ValueSetID\tURL\tName\tstatus\tversion\tFound in FHIR IGs\n")
        for val_set in vs_list:            
            vsurl = val_set.url
            if vsurl in vs_dict:
                for item in vs_dict[vsurl]:
                     itemstr= ",".join(map(str, item))
                f.write(f"{val_set.id}\t{val_set.url}\t{val_set.name}\t{val_set.status}\t{val_set.version}\t{itemstr}\n")
            else:
                f.write(f"{val_set.id}\t{val_set.url}\t{val_set.name}\t{val_set.status}\t{val_set.version}\tNot used\n")
        


def get_codesystems(args,smart):
    """
      Create a tsv file of CodeSystems for import into Confluence from the ontoserver
    """
    outfile = os.path.join(args.outdir,'CodeSystems.txt')
    if os.path.exists(outfile):
        os.remove(outfile)
    endpoint=args.endpoint
    query = smart.prepare()
    if not query:
        print("Server is not ready: {0}".format(endpoint))
        return None
    cs_search=cs.CodeSystem.where(struct={})
    cs_list = cs_search.perform_resources(smart.server)
    with open(outfile, "w") as f:
        f.write("CodeSystemID\tURL\tName\tstatus\tversion\n")
        for code_sys in cs_list:
            f.write(f"{code_sys.id}\t{code_sys.url}\t{code_sys.name}\t{code_sys.status}\t{code_sys.version}\n")
        


def get_conceptmaps(args,smart):
    """
      Create a tsv file of ConceptMaps for import into Confluence from the ontoserver
    """
    outfile = os.path.join(args.outdir,'ConceptMaps.txt')
    if os.path.exists(outfile):
        os.remove(outfile)
    endpoint=args.endpoint
    query = smart.prepare()
    if not query:
        print("Server is not ready: {0}".format(endpoint))
        return None
    cm_search=cm.ConceptMap.where(struct={})
    cm_list = cm_search.perform_resources(smart.server)
    with open(outfile, "w") as f:
        f.write("ConceptMapID\tURL\tName\tstatus\tversion\n")
        for c_map in cm_list:
            f.write(f"{c_map.id}\t{c_map.url}\t{c_map.name}\t{c_map.status}\t{c_map.version}\n")


def get_server_packages(args):
    """
      Create a tsv file for import into Confluence from the atomio syndication file for the server
    """    
    outfile = os.path.join(args.outdir,'UpstreamFeeds.txt')
    if os.path.exists(outfile):
        os.remove(outfile)
    with open(outfile, "w") as f:
        d = feedparser.parse(args.xmlfile)
        f.write(f"Server Endpoint: {args.endpoint}\t Server Name:{d.feed.title}\t Syndication Feed:{d.feed.link}\t Last Updated:{d.feed.updated}\n")
        f.write(f'Number of Entries: {len(d.entries)}\n')
        f.write("Title\tURL\tVersion\tCategory\tDate Updated\tDate Published\tSummary\n")
        for entry in d.entries:
            f.write(f'{entry.title}\t{entry.ncts_contentitemidentifier}\t{entry.ncts_contentitemversion}\t{entry.tags[0].label}\t{entry.updated}\t{entry.published}\n')

### Mainline
homedir=os.environ['HOME']
parser = argparse.ArgumentParser()
parser.add_argument("-o", "--outdir", help="ouput dir for artefacts", default=os.path.join(homedir,"data","server-config","out"))
parser.add_argument("-e", "--endpoint", help="fhir server endpoint", default="https://tx.dev.hl7.org.au/fhir")
parser.add_argument("-x", "--xmlfile", help="atomio syndication file name", default=os.path.join(homedir,"data","server-config","tx.dev.syndication.xml"))
args = parser.parse_args()
outdir = args.outdir
endpoint=args.endpoint
if not os.path.exists(args.outdir):       
    print(f"FATAL error: {args.outdir} not found.")
    exit
print("Started")
smart = create_client(endpoint=endpoint)
# Get info about all the published CodeSystems and ValueSets
print("...CodeSystems")
get_codesystems(args,smart)
print("...ValueSets")
get_valuesets(args,smart)
print("...ConceptMaps")
get_conceptmaps(args,smart)
print("...Server packages")
get_server_packages(args)
print("Finished")



