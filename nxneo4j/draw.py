from IPython.display import IFrame

def draw(G, limit=100):
    query = f"""
    MATCH (n)
        WITH n, rand() AS random
        ORDER BY random
        LIMIT {limit}
        OPTIONAL MATCH (n)-[r]->(m)
        RETURN n.{G.identifier_property} AS source_node,
               id(n) AS source_id,
               type(r) as label,
               m.{G.identifier_property} AS target_node,
               id(m) AS target_id
    """

    result = G.driver.session().run(query)
    nodes = []
    edges = []
    for row in result:
        node1 = {'id':row['source_id'],'label':str(row['source_node'])}
        node2 = {'id':row['target_id'],'label':str(row['target_node'])}
        edge  = {'from':row['source_id'],'to':row['target_id'],'label':row['label']}
        if (node1 not in nodes) & (node1['id'] != None):
            nodes.append(node1)
        if (node2 not in nodes) & (node2['id'] != None):
            nodes.append(node2)
        if (edge not in edges) & (edge['to'] != None):
            edges.append(edge)

#
    html = f"""
    <html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>neo4j display</title>

      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.css" type="text/css" />
      <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis-network.min.js"> </script>

      <style type="text/css">
        #mynetwork {{
          width: 100%;
          height: 500px;
        }}
      </style>
    </head>
    <body data-gr-c-s-loaded="true">

    <div id="mynetwork"><div class="vis-network" tabindex="900" style="position: relative; overflow: hidden; touch-action: pan-y; user-select: none; -webkit-user-drag: none; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); width: 100%; height: 100%;"><canvas width="1200" height="800" style="position: relative; touch-action: none; user-select: none; -webkit-user-drag: none; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); width: 100%; height: 100%;"></canvas></div></div>

    <script type="text/javascript">
      // create an array with nodes
      var nodes = new vis.DataSet(
      {nodes}
      );

      // create an array with edges
      var edges = new vis.DataSet(
      {edges}
      );

      // create a network
      var container = document.getElementById('mynetwork');
      var data = {{
        nodes: nodes,
        edges: edges
      }};
      var options = {{
        nodes: {{
          font: {{ color: 'white',size: 14 }},
          color: '#F9A6C1',
          size: 25,
          shape: 'circle',
          widthConstraint: 60
        }},
        edges : {{
          arrows: {{
               to: {{enabled: true, scaleFactor: 0.5}}
           }},
          "color": {{
              "inherit": false
          }},
          font: {{size: 14, align: 'middle'}},
          "smooth": {{
              "enabled": true,
              "type": "dynamic",
          }},
          "length": 200
        }},
        "interaction": {{
            "dragNodes": true,
            "hideEdgesOnDrag": false,
            "hideNodesOnDrag": false
        }},
        "physics": {{
            "enabled": true,
            "stabilization": {{
                "enabled": true,
                "fit": true,

            }}
        }}
        }};
      var network = new vis.Network(container, data, options);
    </script>

    </body></html>
    """
    file = open("vis.html", "w")
    file.write(html)
    file.close()
    return IFrame("vis.html", width="100%", height="500")
