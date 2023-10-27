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

    sorted_list = sorted(count_list, key=lambda x: x[1])

    values = ",".join(["{" + '"a": "' + x[0] + '" , '  + '"b": ' + str(x[1]) + "}" for x in sorted_list])


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
    "x": {"field": "a", "type": "ordinal"},
    "y": {"field": "b", "scale": {"type": "log", "base": 10}, "type": "quantitative"},
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

def get_programming_languages(repos,max_lang=100):
    
    count = dict()

    for repo in repos:
        ##print(repo.get("name"))
        language = repo.get("language",None) or "None"

        new_count = count.get(language,0) + 1
        count.update({language: new_count})

    count_list = []

    for key in count:
        count_list.append((key,count.get(key,0)))

    sorted_list = sorted(count_list, key=lambda x: x[1],reverse=True)

    if( max_lang < len(sorted_list)):
        remainig = functools.reduce(lambda a,b: a + b[1],sorted_list[max_lang:],0)

        sorted_list = sorted_list[0: max_lang]

        sorted_list.append(("Other",remainig))

    values = ",".join(["{" + '"category": "' + x[0] + '" , '  + '"value": ' + str(x[1]) + "}" for x in sorted_list])


    template =  '''{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "description": "Pie Chart with percentage_tooltip",
  "data": {
    "values": [ (values) ]
  },
  "mark": {"type": "arc", "tooltip": true},
"width": 500,
  "height": 500,
  "encoding": {
    "theta": {"field": "value", "type": "quantitative", "stack": "normalize"},
    "color": {"field": "category", "type": "nominal"}
  }
}'''

    template = template.replace("(values)",values)

    return template



def get_programming_languages_repos(repos):
    
    count = dict()

    languages = map(lambda x: x["language"] or "None" , repos)

    for (tool,_) in repos_filename:
        for language in languages:
          count.update({(tool,language): 0})
    
    for (tool,_) in repos_code_yml:
        for language in languages:
          count.update({(tool,language): 0})

    for repo in repos:
        ##print(repo.get("name"))
        language = repo.get("language",None) or "None"


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