\# 1a4.com API Endpoint Interceptor



Reverse-engineered GraphQL client that extracts complete product data from 1a4.com by directly calling their internal API endpoints.



\## Usage

```bash

python poc.py

```



Edit the URL in the script to scrape different products.



\## Output



Saves all product data to `product\_content.json` including:

\- Product details

\- Lab results (COA)

\- Organization info

\- Facility data



\## Requirements

```bash

pip install requests pyyaml

```



\## How it works



1\. Decodes base64-encoded product URLs

2\. Extracts internal BL (Business Logic) strings

3\. Queries GraphQL endpoint directly with decoded identifiers

4\. Parses YAML responses into structured JSON



\## Example

```python

data = scrape("HTTPS://1A4.COM/13TX7BMRTPRSUWN88TMRRO")

```


