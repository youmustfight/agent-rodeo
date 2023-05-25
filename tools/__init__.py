from tools.calculate import calculate
from tools.chemistry import convert_smiles_to_selfies, pubchem_get_compound_by_cid, pubchem_get_compound_by_sid, pubchem_search_compounds_by_name
from tools.llms import writing
from tools.serps_search import serps_search
from tools.wikipedia import wikipedia_page_content_retrieval, wikipedia_pages_search


dict_tools = {
    # --- Methods
    'Calculate': {
        'func': calculate,
        'description': 'Runs a calculation for math computation - uses Python eval function so must use math operations. (Example action input: 4 * 7 / 3)',
    },
    # 'Write': {
    #     'func': writing,
    #     'description': ' Writes something given a writing prompt. Provide additional context when possible. Not appropriate for math, good for creative writing. (Example action input: ["Write out what the meaning of life is", "Fact X", "Statistic Y", "Context Z", ...])'
    # },
    # --- Chemistry
    'Get a Chemical Compound by CID': {
        'func': pubchem_get_compound_by_cid,
        'description': 'Fetch a single compound\'s information by CID (PubChem Compound Identification). The input is a single integer.'
    },
    'Get a Chemical Compound by SID': {
        'func': pubchem_get_compound_by_sid,
        'description': 'Fetch a substance information by SID (Substance ID). This example fetches information about a substance with the SID. The input is a single integer. (Example action input: "999999999999")'
    },
    'Search for Chemical Compound CIDs by Name': {
        'func': pubchem_search_compounds_by_name,
        'description': 'Fetch a list of compound CIDs given a proper molecule name, not a property. Cannot take conversational inputs. (Example action input: "Kryptonite")'
    },
    'Convert a Molecule\'s SMILES into SELFIES': {
        'func': convert_smiles_to_selfies,
        'description': 'Translates a SMILES string into its corresponding SELFIES string. Strictly use the SMILES code as input. (Example action input: "c1ccccc1") (Example output: "[Cl][Ag]")'
    },
    # --- Search Content
    'Search Google Results': {
        'func': serps_search,
        'description': 'Search Google for information that occurred after 2021. (Example action input: Who is the current CEO of the Robin Hood Foundation?)',
    },
    'Search Wikipedia Pages': {
        'func': wikipedia_pages_search,
        'description': 'Search to see a list of Wikipedia pages that exist for a topic, person, organization exists before retrieving content. (Example action input: Jurrasic Park cast)',
    },
    'Fetch Wikipedia Page Content': {
        'func': wikipedia_page_content_retrieval,
        'description': 'After performing a Wikipedia pages search, this tool can retrieve content for a given Wikipedia page title (Example action input: President of the United States)',
    }
}