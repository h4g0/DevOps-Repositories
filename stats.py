import functools
from tools import repos_filename, repos_code_yml

def get_stats_repos_per_tool(repos):
    
    count_list = get_tools_more_than_one_percent(repos)

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
    
    count_list = get_languages_more_than_one_percent(repos)

    sorted_list = sorted(count_list, key=lambda x: x[1],reverse=True)

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



def get_programming_languages_repos(repos):
    
    count = dict()

    languages = [x[0] for x in get_languages_more_than_one_percent(repos)]

    tools_one_percent = [x[0] for x in get_tools_more_than_one_percent(repos)]

    for repo in repos:
        ##print(repo.get("name"))
        language = repo.get("language",None) or "None"


        if not (language in languages):
            continue
          
      
        tools = repo.get("tools_used") or []


        for tool in tools:
            
            if not (tool in tools_one_percent):
              continue

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
   
    tools = get_tools_more_than_one_percent(repos)

    count = dict()

    for repo in repos:
        tools_repo = repo.get("tools_used", [])

        count_t = count.get(len(tools_repo),0) + 1

        count.update({len(tools_repo): count_t })


    count_list = []

    for key in count:
        count_list.append((key, count.get(key)))
    
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

def get_languages_more_than_one_percent(repos):
    
    count = dict()

    for repo in repos:
        ##print(repo.get("name"))
      language = repo.get("language",None) or "None"

      if language == "None":
          continue
      
      new_count = count.get(language,0) + 1
      count.update({language: new_count})

    one_percent = len(repos) / 100

    count_list = []

    for key in count:
        count_list.append((key,count.get(key,0)))

    count_list = list(filter(lambda x: x[1] > one_percent,count_list))

    return count_list
   

def get_tools_more_than_one_percent(repos):
    
    count = dict()

    for repo in repos:
        ##print(repo.get("name"))
      tools = repo.get("tools_used") or []


      for tool in tools:
          new_count =  count.get(tool,0) + 1
          count.update({tool: new_count})

    one_percent = len(repos) / 100

    count_list = []

    for key in count:
        count_list.append((key,count.get(key,0)))

    count_list = list(filter(lambda x: x[1] > one_percent,count_list))

    return count_list
   

def get_languages_cicd(repos,reposcicd):
   
    languages = [ x[0] for x in get_languages_more_than_one_percent(reposcicd) ]

    count = dict()

    for language in languages:
        count.update({(language, 1) : 0 })
        count.update({(language, 2) : 0 })

    for repo in repos:
        
        tools_repo = repo.get("tools_used", [])

        language = repo.get("language","None")

        if not (language in languages):
          continue

        if(len(tools_repo) == 0):
            count_t = count.get((language,1),0) + 1

            count.update({(language,1): count_t })
        
        else:
            count_t = count.get((language,2),0) + 1

            count.update({(language,2): count_t })
        

    count_list = []

    for key in count:
        count_list.append((key, count.get(key)))
    
    ##filtered_list = filter(lambda x: x[1] > 1000, count_list)

    ##sorted_list = sorted(filtered_list, key=lambda x: x[1],reverse=True)

    values = ",".join(["{" + '"language": "' + str(x[0][0]) + '" , '  + '"cicd": ' + str(x[0][1]) + ' , '  + '"people": ' +  str(x[1]) + "}" for x in count_list])


    template =  '''{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "data": { "values": [
       (values)
    ]},
     "transform": [
      {"calculate": "datum.cicd == 2 ? 'yes' : 'no'", "as": "CI/CD"}
    ],
    "mark": "bar",
    "width": {"step": 17},
    "encoding": {
      "y": {
        "aggregate": "sum", "field": "people",
        "title": "",
        "stack":  "normalize"
      },
      "x": {"field": "language"},
      "color": {
        "field": "CI/CD",
        "scale": {"range": ["#675193", "#ca8861"]}
      }
    }
  }
  '''

    template = template.replace("(values)",values)

    return template


def get_tools_language_cicd(repos):
   
    languages = [ x[0] for x in get_languages_more_than_one_percent(repos) ]

    tools = [ x[0] for x in get_tools_more_than_one_percent(repos) ]

    count = dict()

    for language in languages:
        for tool in tools:
            count.update({(language, tool) : 0 })

    for repo in repos:
        
        tools_repo = repo.get("tools_used", [])

        language = repo.get("language","None")

        if not (language in languages):
          continue

        for tool in tools_repo:
            if not (tool in tools):
                continue
            count_t = count.get((language,tool),0) + 1

            count.update({(language,tool): count_t })
      

    count_list = []

    for key in count:
        count_list.append((key, count.get(key)))
    
    ##filtered_list = filter(lambda x: x[1] > 1000, count_list)

    ##sorted_list = sorted(filtered_list, key=lambda x: x[1],reverse=True)

    values = ",".join(["{" + '"language": "' + str(x[0][0]) + '" , '  + '"tool": "' + str(x[0][1]) + '" , '  + '"people": ' +  str(x[1]) + "}" for x in count_list])


    template =  '''{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "data": { "values": [
       (values)
    ]},
    "mark": "bar",
    "width": {"step": 17},
    "encoding": {
      "y": {
        "aggregate": "sum", "field": "people",
        "title": "",
        "stack":  "normalize"
      },
      "x": {"field": "language"},
      "color": {
        "field": "tool"
      }
      }
    }
  }
  '''

    template = template.replace("(values)",values)

    return template


def get_map_tool_tool(repos):
    
    count = dict()

    tools_one_percent = [x[0] for x in get_tools_more_than_one_percent(repos)]

    for tool1 in tools_one_percent:
        for tool2 in tools_one_percent:
          count.update({(tool1,tool2): 0})

    for repo in repos:
        ##print(repo.get("name"))
       
      
        tools = repo.get("tools_used") or []


        for tool1 in tools:
            
            if not (tool1 in tools_one_percent):
              continue

            for tool2 in tools:
                
              if not (tool2 in tools_one_percent):
                continue
           
              if tool1 == tool2:
                 continue
              
              new_count =  count.get((tool1,tool2),0) + 1
              count.update({(tool1,tool2): new_count})

    count_list = []

    for key in count:
        count_list.append((key,count.get(key,0)))

    sorted_list = sorted(count_list, key=lambda x: x[1],reverse=True)

    def transform_value(x):
      return '{"tool1": "' + x[0][1] + '" , "tool2": "' + x[0][0] + '" , "count": ' + str(x[1]) + '}'

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
      "field": "tool1",
      "type": "nominal"
    },
    "x": {
      "field": "tool2",
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




def get_number_tools_per_year(repos):
   
    
    count = dict()

    for year in range(2012,2024):
        for tools in range(1,14):
            count.update({(year, tools) : 0 })

    def get_year(date):
      datestr = date.get("$date","")

      return int(datestr[0:4])
    
    for repo in repos:
        
        snapchots = repo.get("snapshots",[])
        

        for snapchot in snapchots:
          year = get_year(snapchot["date"])    
          tools_repo = len(snapchot.get("tools", []))

          if(year < 2012 or year > 2023):
             continue
          
          if(tools_repo == 0):
             continue
          
          count_t = count.get((year,tools_repo),0) + 1

          count.update({(year,tools_repo): count_t })
      

    count_list = []

    for key in count:
        count_list.append((key, count.get(key)))
    
    ##filtered_list = filter(lambda x: x[1] > 1000, count_list)

    ##sorted_list = sorted(filtered_list, key=lambda x: x[1],reverse=True)

    values = ",".join(["{" + '"year": "' + str(x[0][0]) + '" , '  + '"tools": "' + str(x[0][1]) + '" , '  + '"people": ' +  str(x[1]) + "}" for x in count_list])


    template =  '''{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "data": { "values": [
       (values)
    ]},
    "mark": "bar",
    "width": {"step": 17},
    "encoding": {
      "y": {
        "aggregate": "sum", "field": "people",
        "title": "",
        "stack":  "normalize"
      },
      "x": {"field": "year"},
      "color": {
        "field": "tools",
        "sort": ["1","2","3","4","5","6","7","8","9","10","11","12","13"],
        "type": "nominal"
      }
      }
    }
  
  '''

    template = template.replace("(values)",values)

    return template



def get_cicd_percent_per_year(repos):
   
    
    count = dict()

    for year in range(2012,2024):
        count.update({(year,"yes") : 0 })
        count.update({(year,"no") : 0 })

    def get_year(date):
      

      return int(date[0:4])
    
    for repo in repos:
        
    
        year = get_year(repo["created_at"])    
        tools_repo = len(repo.get("tools_used", []))

        if(year < 2012 or year > 2023):
            continue
          
        cicd = "yes"

        if tools_repo == 0:
            cicd = "no"
          
        count_t = count.get((year,cicd),0) + 1

        count.update({(year,cicd): count_t })
      

    count_list = []

    for key in count:
        count_list.append((key, count.get(key)))
    
    ##filtered_list = filter(lambda x: x[1] > 1000, count_list)

    ##sorted_list = sorted(filtered_list, key=lambda x: x[1],reverse=True)

    values = ",".join(["{" + '"year": "' + str(x[0][0]) + '" , '  + '"cicd": "' + str(x[0][1]) + '" , '  + '"people": ' +  str(x[1]) + "}" for x in count_list])


    template =  '''{
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "data": { "values": [
       (values)
    ]},
     "transform": [
    {
      "joinaggregate": [{"op": "sum", "field": "people", "as": "total"}],
      "groupby": ["year"]
    },
    {"calculate": "datum.people / datum.total", "as": "fraction"}
  ],
  "encoding": {
    "y": {
      "aggregate": "sum",
      "field": "people",
      "title": "population",
      "stack": "normalize"
    },
    "order": {"field": "cicd", "sort": "descending"},
    "x": {"field": "year", "type": "ordinal"},
    "color": {
      "field": "cicd",
      "type": "nominal",
      "scale": {"range": ["#675193", "#ca8861"]}
    }
  },
  "layer": [
    {"mark": "bar"},
    {
      "mark": {"type": "text", "dx": 20, "dy": 0, "angle": 90},
      "encoding": {
        "color": {"value": "white"},
        "text": {"field": "fraction", "type": "quantitative", "format": ".1%"}
      }
    }
  ]
    }
  
  '''

    template = template.replace("(values)",values)

    return template

def get_language_number_of_tools_distribution(repos):
   
    languages = [x[0] for x in get_languages_more_than_one_percent(repos)]

    count_list = []


    for repo in repos:
        
        tools_repo = len(repo.get("tools_used", []))

        if(tools_repo == 0):
            continue

        language = repo.get("language","None")

        if not (language in languages):
            continue
        

        count_list.append((language, tools_repo))


       
    ##filtered_list = filter(lambda x: x[1] > 1000, count_list)

    ##sorted_list = sorted(filtered_list, key=lambda x: x[1],reverse=True)

    values = ",".join(["{" + '"language": "' + str(x[0]) + '" , '  + '"#tools": ' + str(x[1]) + "}" for x in count_list])


    template =  '''{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "title": "Distribution of Body Mass of Penguins",
  "width": 400,
  "height": 80,
  "data": {
   "values": [
       (values)
    ]
  },
  "mark": "area",
  "transform": [
    {
      "density": "Body Mass (g)",
      "groupby": ["Species"],
      "extent": [2500, 6500]
    }
  ],
  "encoding": {
    "x": {"field": "value", "type": "quantitative", "title": "Body Mass (g)"},
    "y": {"field": "density", "type": "quantitative", "stack": "zero"},
    "row": {"field": "Species"}
  }
}
'''

    template = template.replace("(values)",values)

    return template
