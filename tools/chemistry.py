import json
from pydash import start_case
import re
import requests
import selfies

def pubchem_get_compound_by_cid(query, history):
    print('[TOOL] pubchem_compound_by_cid', query)
    clean_query = re.sub(r'\D', '', str(query))
    response = requests.get(f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/{clean_query}/JSON')
    data = response.json()
    try:
        trimmed_data = data.get('PC_Compounds')[0].get('props')
        trimmed_data = list(map(lambda data_obj: { 'label': data_obj.get('urn').get('label'), 'value': data_obj.get('value')}, trimmed_data))
        print('[TOOL] pubchem_compound_by_cid -> ', trimmed_data)
        return trimmed_data
    except Exception as err:
        print('[TOOL] pubchem_compound_by_cid -> err', err)
        return data

def pubchem_get_compound_by_sid(query, history):
    print('[TOOL] pubchem_compound_by_sid', query)
    clean_query = re.sub(r'\D', '', str(query))
    response = requests.get(f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/SID/{clean_query}/JSON')
    data = response.json()
    print('[TOOL] pubchem_compound_by_sid -> ', data)
    return data

def pubchem_search_compounds_by_name(query, history):
    print('[TOOL] pubchem_search_compounds_by_name', query)
    response = requests.get(f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{start_case(query)}/CIDs/JSON')
    data = response.json()
    print('[TOOL] pubchem_search_compounds_by_name -> ', data)
    return data

def convert_smiles_to_selfies(query, history):
    print('[TOOL] convert_smiles_to_selfies', query)
    clean_query = query.replace('"', '')
    try:
        data = selfies.encoder(clean_query)
        print('[TOOL] convert_smiles_to_selfies -> ', data)
        return data
    except selfies.EncoderError:
        return f'Error translating SMILES code {clean_query}'
