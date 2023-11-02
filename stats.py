import functools
from tools import repos_filename, repos_code_yml

def get_stats_repos_per_tool(repos):
    
    count = dict()


    for (tool,_) in repos_filename:
        count.update({tool: 0})
    
    for (tool,_) in repos_code_yml:
        count.update({tool: 0})

    for repo in repos:
        ##print(repo.get("name"))
        tools = repo.get("tools_used") or []


        for tool in tools:
            new_count =  count.get(tool,0) + 1
            count.update({tool: new_count})

    count_list = []

    for key in count:
        count_list.append((key,count.get(key,0)))

    filtered_list = filter(lambda x: x[1] > 0, count_list)

    sorted_list = sorted(filtered_list, key=lambda x: x[1])

    values = ",".join(["{" + '"tool": "' + x[0] + '" , '  + '"count": ' + str(x[1]) + "}" for x in sorted_list])


    template =  '''{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "description": "A simple bar chart with embedded data.", 
  "data": {
    "values": [(values)]
  },
 "params": [
    {
      "name": "highlight",
      "select": {"type": "point", "on": "pointerover"}
    },
    {"name": "select", "select": "point"}
  ],
  "mark": {
    "type": "bar",
    "fill": "#4C78A8",
    "stroke": "black",
    "cursor": "pointer"
  },
  "encoding": {
    "x": {"field": "tool", "type": "ordinal"},
    "y": {"field": "count", "scale": {"type": "log", "base": 10}, "type": "quantitative"},
    "fillOpacity": {
      "condition": {"param": "select", "value": 1},
      "value": 0.3
    },
    "strokeWidth": {
      "condition": [
        {
          "param": "select",
          "empty": false,
          "value": 2
        },
        {
          "param": "highlight",
          "empty": false,
          "value": 1
        }
      ],
      "value": 0
    }
  },
  "config": {
    "scale": {
      "bandPaddingInner": 0.2
    }
  }
}'''

    template = template.replace("(values)",values)

    return template

def get_programming_languages(repos):
    
    count = dict()

    for repo in repos:
        ##print(repo.get("name"))
        language = repo.get("language",None) or "None"

        new_count = count.get(language,0) + 1
        count.update({language: new_count})

    count_list = []

    for key in count:
        count_list.append((key,count.get(key,0)))

    filtered_list = filter(lambda x: x[1] > 1000, count_list)

    sorted_list = sorted(filtered_list, key=lambda x: x[1],reverse=True)

    values = ",".join(["{" + '"tool": "' + x[0] + '" , '  + '"count": ' + str(x[1]) + "}" for x in sorted_list])


    template =  '''{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "description": "A bar chart with highlighting on hover and selecting on click. (Inspired by Tableau's interaction style.)",
  "data": {
    "values": [
      (values)
    ]
  },
  "params": [
    {
      "name": "highlight",
      "select": {"type": "point", "on": "pointerover"}
    },
    {"name": "select", "select": "point"}
  ],
  "mark": {
    "type": "bar",
    "fill": "#4C78A8",
    "stroke": "black",
    "cursor": "pointer"
  },
  "encoding": {
    "x": {"field": "tool", "type": "ordinal", "sort": "-y"},
    "y": {"field": "count", "scale": {"type": "log", "base": 10}, "type": "quantitative"},
    "fillOpacity": {
      "condition": {"param": "select", "value": 1},
      "value": 0.3
    },
    "strokeWidth": {
      "condition": [
        {
          "param": "select",
          "empty": false,
          "value": 2
        },
        {
          "param": "highlight",
          "empty": false,
          "value": 1
        }
      ],
      "value": 0
    }
  },
  "config": {
    "scale": {
      "bandPaddingInner": 0.2
    }
  }
}'''

    template = template.replace("(values)",values)

    return template



def get_programming_languages_repos(repos,languages):
    
    count = dict()

    for (tool,_) in repos_filename:
        for language in languages:
          count.update({(tool,language): 0})
    
    for (tool,_) in repos_code_yml:
        for language in languages:
          count.update({(tool,language): 0})

    for repo in repos:
        ##print(repo.get("name"))
        language = repo.get("language",None) or "None"


        if not (language in languages):
            continue
         
        tools = repo.get("tools_used") or []


        for tool in tools:
            new_count =  count.get((tool,language),0) + 1
            count.update({(tool,language): new_count})

    count_list = []

    for key in count:
        count_list.append((key,count.get(key,0)))

    sorted_list = sorted(count_list, key=lambda x: x[1],reverse=True)

    def transform_value(x):
      return '{"language": "' + x[0][1] + '" , "tool": "' + x[0][0] + '" , "count": ' + str(x[1]) + '}'

    values = ",\n".join([transform_value(x) for x in sorted_list])


    template =  '''{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "data": {
    "values": [
      (values)
    ]
  },
  "params": [{"name": "highlight", "select": "point"}],
  "mark": {"type": "rect", "strokeWidth": 2},
  "encoding": {
    "y": {
      "field": "language",
      "type": "nominal"
    },
    "x": {
      "field": "tool",
      "type": "nominal"
    },
    "fill": {
      "field": "count",
      "type": "quantitative"
    },
    "stroke": {
      "condition": {
        "param": "highlight",
        "empty": false,
        "value": "black"
      },
      "value": null
    },
    "opacity": {
      "condition": {"param": "highlight", "value": 1},
      "value": 0.5
    },
    "order": {"condition": {"param": "highlight", "value": 1}, "value": 0}
  },
  "config": {
    "scale": {
      "bandPaddingInner": 0,
      "bandPaddingOuter": 0
    },
    "view": {"step": 40},
    "range": {
      "ramp": {
        "scheme": "yellowgreenblue"
      }
    },
    "axis": {
      "domain": false
    }
  }
}
'''

    template = template.replace("(values)",values)

    return template


def get_programming_languages_all(repos):
  languages = list(set(map(lambda x: x["language"] or "None" , repos)))
  
  count = dict()

  for repo in repos:
      ##print(repo.get("name"))
      language = repo.get("language",None) or "None"

      new_count = count.get(language,0) + 1
      count.update({language: new_count})
  
  languages = list(sorted(languages, key=lambda x: count.get(x,0),reverse=True))[0:10]

  print(len(languages))

  return get_programming_languages_repos(repos,languages)

def get_number_of_tools_distribution(repos):
    
    count = dict()

    for repo in repos:
        ##print(repo.get("name"))
        tools = len(repo.get("tools_used",[]) or [])

        new_count = count.get(tools,0) + 1
        count.update({tools: new_count})

    count_list = []

    for key in count:
        count_list.append((key,count.get(key,0)))

    ##filtered_list = filter(lambda x: x[1] > 1000, count_list)

    ##sorted_list = sorted(filtered_list, key=lambda x: x[1],reverse=True)

    values = ",".join(["{" + '"number of tools": "' + str(x[0]) + '" , '  + '"count": ' + str(x[1]) + "}" for x in count_list])


    template =  '''{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "description": "A bar chart with highlighting on hover and selecting on click. (Inspired by Tableau's interaction style.)",
  "data": {
    "values": [
      (values)
    ]
  },
  "params": [
    {
      "name": "highlight",
      "select": {"type": "point", "on": "pointerover"}
    },
    {"name": "select", "select": "point"}
  ],
  "mark": {
    "type": "bar",
    "fill": "#4C78A8",
    "stroke": "black",
    "cursor": "pointer"
  },
  "encoding": {
    "x": {"field": "number of tools", "type": "ordinal", "sort": "-y"},
    "y": {"field": "count", "scale": {"type": "log", "base": 10}, "type": "quantitative"},
    "fillOpacity": {
      "condition": {"param": "select", "value": 1},
      "value": 0.3
    },
    "strokeWidth": {
      "condition": [
        {
          "param": "select",
          "empty": false,
          "value": 2
        },
        {
          "param": "highlight",
          "empty": false,
          "value": 1
        }
      ],
      "value": 0
    }
  },
  "config": {
    "scale": {
      "bandPaddingInner": 0.2
    }
  }
}'''

    template = template.replace("(values)",values)

    return template

