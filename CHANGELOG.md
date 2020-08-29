# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.3] - [Unreleased]
### Added (by [@ybaktir](https://github.com/ybaktir))
- CHANGELOG.md
- nx.draw(G)
- G.nodes
- G.edges
- G.clear() to delete all the data, acts similar to G.delete_all()
- len(G) to display number of nodes
- G.remove_node()

### Changed (by [@ybaktir](https://github.com/ybaktir))
- reorganized the entire file structure to better separate the algorithms files from the graph files.
- changed README.md with new figures, dependencies
- all the $nodeLabel, $relationshipType params changed to $node_label and $relationship_type for better code readibility
- updated G.load_got() to fix constraint errors
- updated G.load_euroads() to fix constraint errors
- updated G.load_twitter() to fix constraint errors
- updated G.add_edge() to enable property assignment
- updated G.add_node() to enable property assignment


### Removed
- No removals

### Known Issues (by [@ybaktir](https://github.com/ybaktir))
- len(G) doesn't return the correct value, uses config restrictions
- after G.load_got() and after nx.draw(G), some of the relationship labels don't show on the visualization

## [0.0.2] - 2020-08-25
### Added (by [@ybaktir](https://github.com/ybaktir))
- G.delete_all()
- G.load_got()
- G.load_euroads()
- G.load_twitter()

### Changed (by [@ybaktir](https://github.com/ybaktir))
- All "apoc" based code is moved to Graph Data Science library aka "gds" since apoc is not supported by neo4j 4.x.
- All {params} syntax moved to $params syntax since {params} no longer supported.
- Updated README.md.
- Updated the examples file.

### Removed (by [@ybaktir](https://github.com/ybaktir))
- Removed functionality of harmonic centrality, average clustering as they are not supported by gds.
- Removed test file as it was hard to maintain the code because of too many changes. The file will back in the future versions.
