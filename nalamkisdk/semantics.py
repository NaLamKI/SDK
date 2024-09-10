from jsonschema import validate
import json

schema_path = "src/sdk/schemas/"

with open(schema_path + "Output Format/" + "KI_Service_GEO_Output.json") as file:
    data_schema = json.load(file)

with open(schema_path + "Self description/" + "Catalog_Entry.json") as file:
    cataloge_schema = json.load(file)

with open(schema_path + "Self description/" + "Dashboard_Template.json") as file:
    dashboard_schema = json.load(file)

def validate_data_semantic(data):
    return(validate(instance= data,schema=data_schema))

def validate_service_cataloge(data):
    return validate(instance=data, schema=cataloge_schema)

def validate_dashboard_template(data):
    return validate(instance=data, schema=dashboard_schema)