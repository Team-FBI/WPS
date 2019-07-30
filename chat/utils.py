async def parse_querystring(byte_querystring):
    result = dict()
    if not byte_querystring:
        return result
    querystring = byte_querystring.decode('utf-8')
    queries = querystring.split('&')
    for query in queries:
        query = query.split('=')
        result[query[0]] = query[1]
    return result

