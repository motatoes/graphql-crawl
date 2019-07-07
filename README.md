# graphql-crawl

![https://i.imgur.com/MnogXnR.png](https://i.imgur.com/MnogXnR.png)

Try it on digital ocean: [http://128.199.35.101:4000/](http://128.199.35.101:4000/)

This project consists of three main services. It is a broad crawler that crawls pages for a single domain starting from the root domain
and spreads by following all internal links. It will fetch the title, raw content after stripping tags, and some meta tags information:

1. A mongodb service `db`
2. A crawler worker using python and scrapy `crawler`
3. A `graphql` service which uses node and apollo

# Installing the project

To run the project locally, simply clone the repository and then start the services with dockercompose:

```
docker-compose up
```

Now you can invoke the services from another tab:

```
docker-compose exec crawler scrapy crawl generic -a start="http://example.com"
```

You can pass the domain to crawl using the `start` argument. The default domain is `bbc.co.uk`.

The crawler will start crawling pages for this domain and store them in the mongodb collection. It will include any metadata which is found
and also the root domain, which can be used for filtering the results.

# graphql schema

```
  # Comments in GraphQL are defined with the hash (#) symbol.

  type Page {
    url: String!,
    domain: String!,
    title: String,
    og_type: String,
    og_site_name: String,
    og_image: String,
    og_title: String,
    og_url: String,
    raw_text: String
  }

  # The "Query" type is the root of all GraphQL queries.
  # (A "Mutation" type will be covered later on.)
  # You can filter using the domain article (example: "bbc.co.uk")
  
  type Query {
    pages(domain: String, limit: Int, offset: Int): [Page]
  }
```
**Note:** The results are paginated and only the first 10 matches are returned for each query. You can pass a `limit` (upto 100) and an `offset` parameter to retrieve more results.

# Future Improvements

- Index the `domain` field in the mongodb collection
- add more filtering options to the graphql schema
- use frontera to make the crawler distributed and efficient for large-scale crawls
- Use it behind a distributed proxy to avoid rate limiting by sites with bot protection
