# Incident.io
This directory contains the manifest-only connector for `source-incident`.

Source connector for Incident.io which is an on call, incident response and status pages tool. 
The Incident.io source connector which ingests data from the incident API.
Incident is an on call, status pages and incident response tool.
The source supports a number of API changes. For more information, checkout the website https://incident.io/
  
An API key is required for authentication and using this connector. In order to obtain an API key, you must have a PRO or above account.
Once logged-in, you will find your API key your dashboard settings. You can find more about their API here https://api-docs.incident.io/

## Usage
There are multiple ways to use this connector:
- You can use this connector as any other connector in Airbyte Marketplace.
- You can load this connector in `pyairbyte` using `get_source`!
- You can open this connector in Connector Builder, edit it, and publish to your workspaces.

Please refer to the manifest-only connector documentation for more details.

## Local Development
We recommend you use the Connector Builder to edit this connector.

But, if you want to develop this connector locally, you can use the following steps.

### Environment Setup
You will need `airbyte-ci` installed. You can find the documentation [here](airbyte-ci).

### Build
This will create a dev image (`source-incident:dev`) that you can use to test the connector locally.
```bash
airbyte-ci connectors --name=source-incident build
```

### Test
This will run the acceptance tests for the connector.
```bash
airbyte-ci connectors --name=source-incident test
```
