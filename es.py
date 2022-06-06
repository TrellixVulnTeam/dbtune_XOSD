import json
import ssl

from elasticsearch import Elasticsearch
from elasticsearch.connection import create_ssl_context

ssl_context = create_ssl_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

es = Elasticsearch(hosts=[{'host': "192.168.113.150", 'port': 30007}], scheme="http",
                   # to ensure that it does not use the default value `True`
                   verify_certs=False,
                   ssl_context=ssl_context,
                   http_auth=('elastic', 'CqcYug75J65513u5WVO3u7Wv'),
                   timeout=60)

# es = Elasticsearch(hosts="https://192.168.113.150:30037", http_auth=('elastic', 'E1jxc8id2ON3jC3U3tM159d8'))
print(es.info())

query_json = {
    "from": 0,
    "size": 20,
    "query": {
        "match_all": {}
    }
}

query = es.search(index='dblog-*', body=query_json)
print(query)

results = query['hits']['hits']  # es查询出的结果第一页
print("es查询结果：\n{results}\n".format(results=results))

# total = query['hits']['total']  # es查询出的结果总量
# print("es查询出的结果第一页：\n{total}\n".format(total=total))

print(results[0]['_source'])

for result in results:
    context = result['_source']['Context']
    strs = context.split(',')
    print(len(strs))

    for str in strs:
        print("str===>:", str)
    # print("Level: 【{Level}】 Context: 【{Context}】\n".format(Level=result['_source']['Level'],
    #                                                        Context=result['_source']['Context']))

# query = es.search(index='dblog-*', body={"query": {"match_all": {}}}, scroll='5m', size=100)
# results = query['hits']['hits']  # es查询出的结果第一页
# total = query['hits']['total']['value']  # es查询出的结果总量
# scroll_id = query['_scroll_id']  # 游标用于输出es查询出的所有结果
#
# for i in range(0, int(total / 100) + 1):
#     # scroll参数必须指定否则会报错
#     query_scroll = es.scroll(scroll_id=scroll_id, scroll='5m')['hits']['hits']
#     results += query_scroll
#
# print(len(results))

# 将 JSON 对象转换为 Python 字典
# data2 = json.loads(query)
# print("data2['name']: ", data2['name'])
# print("data2['url']: ", data2['url'])


