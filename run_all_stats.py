import os
import json
from stats import (
    get_cicd_percent_per_year,
    get_language_number_of_tools_distribution,
    get_languages_cicd,
    get_languages_cicd_morethanone,
    get_languages_more_than_one_percent,
    get_map_tool_tool,
    get_number_of_tools_distribution,
    get_number_tools_per_year,
    get_programming_languages,
    get_programming_languages_all,
    get_programming_languages_repos,
    get_programming_languages_repos_normalized,
    get_stats_repos_per_tool,
    get_tools_language_cicd,
    get_tools_more_than_one_percent,
    migrations_programming_language,
    migrations_programming_languages_to_from,
    migrations_tools,
    migrations_tools_time_to_fall,
    migrations_travis,
    percentage_tools_2019_2023
)

def run_all_stats_and_save(dataset, stats_folder):
    """
    Run all statistics functions with the given dataset and save results to files.
    
    Args:
        dataset: The input dataset to pass to each statistics function
        stats_folder: Folder path where result files will be stored
    """
    # Create the stats folder if it doesn't exist
    os.makedirs(stats_folder, exist_ok=True)
    
    # Dictionary of all functions to execute
    functions = {
        "get_cicd_percent_per_year": get_cicd_percent_per_year,
        "get_language_number_of_tools_distribution": get_language_number_of_tools_distribution,
        #"get_languages_cicd": get_languages_cicd,
        #"get_languages_cicd_morethanone": get_languages_cicd_morethanone,
        "get_languages_more_than_one_percent": get_languages_more_than_one_percent,
        "get_map_tool_tool": get_map_tool_tool,
        "get_number_of_tools_distribution": get_number_of_tools_distribution,
        "get_number_tools_per_year": get_number_tools_per_year,
        "get_programming_languages": get_programming_languages,
        #"get_programming_languages_all": get_programming_languages_all,
        "get_programming_languages_repos": get_programming_languages_repos,
        "get_programming_languages_repos_normalized": get_programming_languages_repos_normalized,
        "get_stats_repos_per_tool": get_stats_repos_per_tool,
        "get_tools_language_cicd": get_tools_language_cicd,
        "get_tools_more_than_one_percent": get_tools_more_than_one_percent,
        #"migrations_programming_language": migrations_programming_language,
        #"migrations_programming_languages_to_from": migrations_programming_languages_to_from,
        #"migrations_tools": migrations_tools,
        #"migrations_tools_time_to_fall": migrations_tools_time_to_fall,
        #"migrations_travis": migrations_travis,
        #"percentage_tools_2019_2023": percentage_tools_2019_2023
    }
    
    # Execute each function and save results
    for func_name, func in functions.items():
        try:
            result = func(dataset)
            
            # Save the result to a file
            output_path = os.path.join(stats_folder, f"{func_name}.json")
            with open(output_path, 'w') as f:
                json.dump(result, f, indent=2)
                
            print(f"Successfully saved result of {func_name} to {output_path}")
            
        except Exception as e:
            print(f"Error executing {func_name}: {str(e)}")
