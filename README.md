chef-tags-api REST api
======================

Python REST api to fetch node TAGS information directly from CHEF server and return it on JSON format

Requirements
------------

### Python Bottle Framework

Please follow http://bottlepy.org main page on how to install/configure Bottle.

Instalation
-----------

Just run the script with a user with knife execution capabilities

Usage
-----

### Listing all nodes from a given environment:

``` 
http://localhost:9999/api/env_name
```

The response will be a JSON like the following:

``` Python
{
        "env_name": {
                "node1": ["tags_list"],
                "node2": ["tags_list"],
                "node3": ["tags_list"],
                "node4": ["tags_list"]          
        }
}
```

### Listing nodes tags based on a custom query:

We can make use o knife search capabilities and provide more information to filter/narrow down our search:

```
http://localhost:9999/api?env=dev&role=web_server
```

The previous 'query' will search for all nodes on the dev environemnt that have the 'web_server' role set up. The result will be like this one:

``` Python
{
        "node1": [tags_list"],
        "node2": [tags_list"]
}
```

Supported filters:

* env
* role
* zone
* name

Contributing
------------

1. Fork the repository on Github
2. Create a named feature branch (like `add_component_x`)
3. Write your change
4. Write tests for your change (if applicable)
5. Run the tests, ensuring they all pass
6. Submit a Pull Request using Github

License and Authors
-------------------

Authors: Marcus Semblano 
