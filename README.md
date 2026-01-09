# Semantic layer to use business terms and KPI definitions to query your data right (and using correct datasets)

How much hours are lost searching for 'the right data'? And how much time is lost comparing KPI outcomes that 'are the same', but KPI outcomes differ? Or trust lost in data driven decision making?

What is **the value of Data Governance**, if we can't re-use data and it's semantics efficiently?

This is where a **semantic layer** (the concept, not a technology) can come to aid and reduce unclarity and inefficiency. 
> _A semantic layer is a business representation of corporate data that helps end users access data autonomously using common business terms managed through business semantics management. A semantic layer maps complex data into familiar business terms such as product, customer, or revenue to offer a unified, consolidated view of data across the organization._ (Wikipedia)

Usually, these business terms and KPI definitions are hardcoded in a reporting/Business Intelligence solution. But they **cannot cross the boundaries* of that single reportion/BI solution. So what if we would model those business terms and defintions in one system, and consume/share it to reporting systems, analysis tools, LLMs and other AI applications?

Using a data governance relationship models from it's application output, to serve as semantic model data, we could:
* share this mapping and it's semantics to **other applications** from a single place;
* serve this mapping to human users;
* use a **Model Context Protocol (MCP)** server to have a **Large-Language Model (LLM)** answer questions on data in a **database** (e.g. PostgreSQL). 


!["Example of a semantic model"](https://github.com/maartenor/semantic-layer-data-governance/blob/main/human/human%20oriented%20data%20model.png?raw=true)

## Mock Data Governance Application (think: Collibra)

A lightweight Python Flask application that demonstrates a data governance platform (similar to Collibra) for testing and development purposes, with an interactive web UI for visualizing data governance models and a REST API.

See [Data Governance Mock server README.md](./data_governance/server/README.md) for the details and try it out!

## Semantic layer output data
See [data](./data_governance/data) folder.

## Input sample data and an Agent.md for improvment purposes
See [./input_data_governance](./input_data_governance) folder.

## Pro-tip: check out how to serve this
Eager to try and see how to serve this in real life. Check out this Github repo [semantic-layer-data-governance](https://github.com/maartenor/semantic-layer-data-governance). Showing an example how to serve the data of a semantic model to (in that case) an Large Language Model, so it can more efficiently understand available data in a database. 

Especially when table names and columns names are far from logical for humans en LLMs to interpret database content, this adds value. Think is situations where only very technical or very short column names exists. Think ERP database tables.

Adding explanatory semantics, increases the 'knowledge' on the business terms needed technical data. This in term reduces the needed LLM capacity (and costs) due to the reducing the amount of prompts/steps and/or database queries/results an LLM needs - hence tokens - to reach an response.