from re import sub


def retrieve_urls(data_set_list: list) -> list[str]:
    url_list = []
    for data_set in data_set_list:
        theme = data_set["theme"][0]
        distribution = data_set["distribution"][0]
        if theme == "Hospitals":
            for key, value in distribution.items():
                if key == "downloadURL":
                    url_list.append(distribution[key])

    return url_list

# Use regex to transform any phrases/strings to snake case
def snake_case(input:str) -> str:
    input.replace('/', ' ')
    return '_'.join(
        sub('([A-Z][a-z]+)', r' \1',
        sub('([A-Z]+)', r' \1',
        input.replace('-', ' '))).split()).lower()