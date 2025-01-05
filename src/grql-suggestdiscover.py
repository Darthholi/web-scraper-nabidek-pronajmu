import requests

# Define the GraphQL endpoint
url = "https://www.realingo.cz/graphql"

# Define common root types
root_types = ["Query", "Mutation", "Subscription"]

# Define common field names to guess
common_field_names = ["id", "name", "title", "description", "createdAt", "updatedAt"]

# Function to send a GraphQL query
def send_query(query):
    response = requests.post(url, json={'query': query})
    return response.json()

# Function to check if a field exists
def check_field_exists(type_name, field_name):
    query = f"""
    {{
        {type_name} {{
            {field_name}
        }}
    }}
    """
    result = send_query(query)
    return 'errors' not in result

# Function to guess fields of a type
def guess_fields(type_name):
    guessed_fields = []
    for field_name in common_field_names:
        if check_field_exists(type_name, field_name):
            guessed_fields.append(field_name)
    return guessed_fields

# Recursive function to discover fields
def discover_fields(type_name, discovered_fields):
    fields = guess_fields(type_name)
    for field_name in fields:
        discovered_fields.append(field_name)

# Main function to discover all fields
def main():
    all_fields = {}
    for root_type in root_types:
        all_fields[root_type] = []
        discover_fields(root_type, all_fields[root_type])
    return all_fields

# Run the main function
discovered_fields = main()
print(discovered_fields)
