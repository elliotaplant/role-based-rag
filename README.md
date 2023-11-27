# Role Based RAG

## Description
`role-based-rag` demonstrates the implementation of role-based access control (RBAC) in a LLM vector database. The application manages access to the nodes of the vector database by attaching an allowlist of roles to the metadata of each node. This enables nodes to have an unlimited number of allowed roles. If the application were extended to use "real" data sources, those roles could be sourced from the data source API, such as the GoogleDrive API.

## Limitations

Currently, `llama_index` only supports "exact match" on metadata. As a result, the "intersection" of the user's roles and the node's roles for matching is not supported. However, this could be improved with a minor patch in `llama_index`'s query engine.

## Documents

The `/documents` folder contains documents separated into "engineering", "finance", and "both" folders. The engineering docs are visible only to queries with the `ENGINEERING` role, finance visible only to `FINANCE`, and both visible to queries with either `ENGINEERING` or `FINANCE` roles.

## Example

First, build the index:
```
$ python build_index.py
Index persisted
```
Next, see that querying with the ENGINEERING role cannot query for information that requires the FINANCE role:
```
$ python query_index.py --role ENGINEERING --query "What is the top salary in the Engineering department?"
I'm sorry, but I cannot provide the answer to your query. The given context information does not provide any information about the salaries in the Engineering department.
```
However, the FINANCE role is allowed to access that information:
```
$ python query_index.py --role FINANCE --query "What is the top salary in the Engineering department?"
The top salary in the Engineering department is $130,000.
```
Information that is visible to both ENGINEERING and FINANCE roles can be seen by either:
```
$ python query_index.py --role FINANCE --query "What is the address of our London office?"
The address of our London office is 20 Innovation Street, Tech City, London, EC1V 9AP, United Kingdom.
$ python query_index.py --role ENGINEERING --query "What is the address of our London office?"
The address of our London office is 20 Innovation Street, Tech City, London, EC1V 9AP, United Kingdom.
```

## Code Files

- `build_index.py`: This script is used to build the vector database index. It integrates metadata from the specified roles and directories into the nodes of the index.

- `query_index.py`: This script allows you to query the index by specifying roles and queries as command-line arguments. It retrieves information based on the access control defined by the metadata in the nodes.
