from SPARQLWrapper import SPARQLWrapper, JSON
import requests

def fetch_from_wikidata(query_term):
    """
    Fetch structured information from Wikidata using SPARQL.
    """
    endpoint_url = "https://query.wikidata.org/sparql"
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(f"""
        SELECT ?itemLabel ?description WHERE {{
            ?item rdfs:label "{query_term}"@en.
            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
        }}
        LIMIT 1
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    if results["results"]["bindings"]:
        result = results["results"]["bindings"][0]
        return {
            "label": result["itemLabel"]["value"],
            "description": result["description"]["value"] if "description" in result else "No description available."
        }
    return None

def fetch_from_dbpedia(query_term):
    """
    Fetch structured information from DBpedia using its REST API.
    """
    url = f"http://dbpedia.org/data/{query_term.replace(' ', '_')}.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        entity_url = f"http://dbpedia.org/resource/{query_term.replace(' ', '_')}"
        if entity_url in data:
            entity_data = data[entity_url]
            label = entity_data.get("http://www.w3.org/2000/01/rdf-schema#label", [{}])[0].get("value", "No label")
            description = entity_data.get("http://www.w3.org/2000/01/rdf-schema#comment", [{}])[0].get("value", "No description")
            return {"label": label, "description": description}
    return None

def fetch_from_conceptnet(query_term):
    """
    Fetch structured information from ConceptNet API.
    """
    url = f"http://api.conceptnet.io/c/en/{query_term.lower().replace(' ', '_')}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        edges = data.get("edges", [])
        if edges:
            related_terms = [edge["end"]["label"] for edge in edges if "label" in edge["end"]]
            return {"label": query_term, "related_terms": related_terms}
    return None
