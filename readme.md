### Installation Requirements
- Access to atomio UI to download the syndication feed file
- Python and the ability to install modules using pip. This will be automatic through the requirements file.
- An input source which is the atom file from the syndication server
- A file path for the output of the process , on Windows this might be C:\data\server-config\out 
  on Mac/Linux it will be /home/user/data/server-config/out or similar where `user` is your account name

### How to create the syndication file
- Log on to atomio ui https://ontoserver.csiro.au/atomio/feeds
- search for the feed name for that server e.g. searching for dev finds `hl7au-dev`
- under `actions` click the `download` button 
- save the syndication file locally, e.g. in the data directory for this app.

### How to install this script (Weirdly have to manually install a few packages also)
   * `pip install -r requirements.txt`
   * `pip install fhirclient fhirpathpy numpy`
   * `virtualenv env`
   * `source env/bin/activate`

### How to run this script
   * `python main.py [-o outfilepath] [-e "https://tx.dev.hl7.org.au/fhir"] [-x xmlfilepath]`

### Regenerating the requirements.txt file
If you change this code and want to regenerate the requirements use this:
   `pip freeze >| requirements.txt`