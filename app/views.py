import json
import pymysql.cursors
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


# from django.views.decorators.csrf import csrf_exempt
# Create your views here.


# 连接数据库
def connectToMySQL():
    connect = pymysql.Connect(
        host='',
        port=3306,
        user='',
        passwd='',
        db='mydb',
        charset='utf8'
    )
    return connect


def runSQL(sql):
    connect = connectToMySQL()
    cursor = connect.cursor()  # 执行完毕返回的结果集默认以元组显示
    # 事务处理

    data = None
    co = None
    success = 1
    # msg = ""
    try:

        cursor.execute(sql)  # 储蓄增加1000

        fetch = cursor.fetchall()
        # print(fetch)

        if fetch:
            co = [*zip(*cursor.description)][0]
            data = [{k: v for k, v in zip(co, fetch[i])} for i in range(cursor.rowcount)]

    except Exception as e:
        connect.rollback()  # 事务回滚
        success = 0
        msg = "事务处理失败" + str(e)
    else:
        connect.commit()  # 事务提交
        msg = "事务处理成功" + str(cursor.rowcount)
    finally:
        # 关闭连接
        cursor.close()
        connect.close()
    return data, success, msg


@csrf_exempt
def query_fw(request):
    # return HttpResponse(request)
    if request.method == 'POST':
        # print(request.body)
        res = json.loads(request.body.decode("utf-8"))
        if res['xianlu_mingcheng']:
            res['xianlu_mingcheng'] = res['xianlu_mingcheng'][0]
        # print(res)

        base_sql = "SELECT siji_id, siji_xingming, siji_xingbie,  xianlu_mingcheng " \
                   "FROM mydb.siji " \
                   "WHERE 1=1 "
        for k, v in res.items():
            if not v:
                continue
            base_sql += " AND " + str(k) + "='" + str(v) + "' "
        base_sql += ";"

        # print(base_sql)

        data, success, msg = runSQL(base_sql)
        # print("data", json.dumps(data))

        if success:
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponse(msg)


@csrf_exempt
def query_td(request):
    # return HttpResponse(request)
    if request.method == 'POST':
        # print(request.body)
        res = json.loads(request.body.decode("utf-8"))

        # print(res)

        base_sql = "SELECT siji_id, siji_xingming, siji_xingbie,  xianlu_mingcheng " \
                   "FROM mydb.siji " \
                   "WHERE 1=1 "
        for k, v in res.items():
            if not v:
                continue
            base_sql += " AND " + str(k) + "='" + str(v) + "' "
        base_sql += ";"

        # print(base_sql)

        data, success, msg = runSQL(base_sql)
        # print("data", json.dumps(data))

        if success:
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponse(msg)


@csrf_exempt
def query_cdwz(request):
    # return HttpResponse(request)
    if request.method == 'POST':
        # print(request.body)
        res = json.loads(request.body.decode("utf-8"))

        data, _, _ = runSQL("SELECT chedui_id FROM mydb.chedui WHERE chedui_id='{}';".format(res['chedui_id']))
        if not data:
            # 不存在的chuidui_id
            return HttpResponse("iderror")

        data, success, msg = runSQL("select shijian, zhandian, weizhang "
                                    "from mydb.weizhangjilu where exists "
                                    "(select * from mydb.siji where exists "
                                    "(select * from mydb.xianlu "
                                    "where xianlu_mingcheng = siji.xianlu_mingcheng and chedui_id = {})"
                                    " and siji_id = weizhangjilu.siji_id);".format(res['chedui_id']))
        if data:
            for item in data:
                item['shijian'] = str(item['shijian'])

        if success:
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponse(msg)


@csrf_exempt
def query_cdwz_e(request):
    # return HttpResponse(request)
    if request.method == 'GET':
        # print(request.body)

        data, success, msg = runSQL("select weizhang, count(weizhang), chedui_id "
                                    "from mydb.weizhangjilu, mydb.siji, mydb.xianlu "
                                    "where weizhangjilu.siji_id = siji.siji_id "
                                    "and siji.xianlu_mingcheng = xianlu.xianlu_mingcheng "
                                    "group by weizhang, xianlu.chedui_id order by weizhang, xianlu.chedui_id;")

        # print('len_e', len(data))

        # print("data", json.dumps(data))

        if success:
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponse(msg)


@csrf_exempt
def query_sjwz(request):
    # return HttpResponse(request)
    if request.method == 'POST':
        # print(request.body)
        res = json.loads(request.body.decode("utf-8"))

        data, _, _ = runSQL("SELECT siji_id FROM mydb.siji WHERE siji_id='{}';".format(res['siji_id']))
        if not data:
            # 不存在的id
            return HttpResponse("iderror")

        data, success, msg = runSQL("SELECT zhandian, shijian, weizhang " \
                                    "FROM mydb.weizhangjilu " \
                                    "WHERE siji_id={};".format(res['siji_id']))
        if data:
            for item in data:
                item['shijian'] = str(item['shijian'])

        if success:
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponse(msg)


@csrf_exempt
def query_sjwz_e(request):
    # return HttpResponse(request)
    if request.method == 'POST':
        # print(request.body)
        res = json.loads(request.body.decode("utf-8"))
        # print(res)

        data, success, msg = runSQL(
            "select weizhang, count(weizhang) from mydb.weizhangjilu group by weizhang, siji_id having siji_id = '{}';".format(
                res["siji_id"]))

        # print('len_e', len(data))

        # print("data", json.dumps(data))

        if success:
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponse(msg)


@csrf_exempt
def insert_sj(request):
    # res = json.loads(request.body.decode("utf-8"))
    # print(res)
    # return HttpResponse(request)
    if request.method == 'POST':
        # print(request.body)
        res = json.loads(request.body.decode("utf-8"))
        # print(res)

        res['xianlu_mingcheng'] = res['xianlu_mingcheng'][0]

        data, _, _ = runSQL("SELECT siji_id FROM mydb.siji WHERE siji_id='{}';".format(res['siji_id']))
        if data:
            return HttpResponse("iderror")

        data, _, _ = runSQL("SELECT xianlu_mingcheng FROM mydb.xianlu WHERE xianlu_mingcheng='{}';"
                            .format(res['xianlu_mingcheng']))
        if not data:
            return HttpResponse("xianluerror")

        _, success, msg = runSQL("INSERT INTO mydb.siji(siji_ID, siji_xingming, siji_xingbie, xianlu_mingcheng) "
                                 "VALUES('{}', '{}', '{}', '{}');"
                                 .format(res['siji_id'], res['siji_xingming'], res['siji_xingbie'],
                                         res['xianlu_mingcheng'])
                                 )

        if success:
            return HttpResponse("OK")
        else:
            return HttpResponse(msg)


@csrf_exempt
def insert_wz(request):
    # res = json.loads(request.body.decode("utf-8"))
    # print(res['shijian1'], res['shijian2'])
    # return HttpResponse("截击机")

    # res = json.loads(request.body.decode("utf-8"))
    # print(res)
    # return HttpResponse("截击机")

    if request.method == 'POST':
        # print(request.body)
        res = json.loads(request.body.decode("utf-8"))
        # print(res)

        data, _, _ = runSQL("SELECT siji_id FROM mydb.siji WHERE siji_id='{}';".format(res['siji_id']))
        if not data:
            # 不存在的工号
            return HttpResponse("iderror")

        data, _, _ = runSQL("SELECT chepaihao FROM mydb.qiche WHERE chepaihao='{}';"
                            .format(res['chepaihao']))
        if not data:
            # 不存在的车牌号
            return HttpResponse("chepaihaoerror")

        res['shijian'] = res['shijian1'][0:10] + '-' + res['shijian2'][11:-5]
        _, success, msg = runSQL("INSERT INTO mydb.weizhangjilu(siji_id, zhandian, chepaihao, weizhang, shijian) "
                                 "VALUES('{}','{}','{}','{}','{}');"
                                 .format(res['siji_id'], res['xianluzhandian'][1], res['chepaihao'], res['weizhang'],
                                         res['shijian']))

        if success:
            return HttpResponse("OK")
        else:
            return HttpResponse(msg)


@csrf_exempt
def insert_qc(request):
    # res = json.loads(request.body.decode("utf-8"))
    # print(res['shijian1'], res['shijian2'])
    # return HttpResponse("截击机")
    if request.method == 'POST':
        # print(request.body)
        res = json.loads(request.body.decode("utf-8"))
        # print(res)
        res['xianlu_mingcheng'] = res['xianlu_mingcheng'][0]
        data, _, _ = runSQL(
            "SELECT chepaihao FROM mydb.qiche WHERE chepaihao='{}';".format(res['chepaihao']))
        if data:
            # 已存在的车牌号
            return HttpResponse("cpherror")

        _, success, msg = runSQL("INSERT INTO mydb.qiche(xianlu_mingcheng, chepaihao, zuoshu) "
                                 "VALUES('{}', '{}', {});"
                                 .format(res['xianlu_mingcheng'], res['chepaihao'], res['zuoshu']))
        if success:
            return HttpResponse("OK")
        else:
            # print(msg)
            return HttpResponse(msg)


@csrf_exempt
def insert_wz_xianlu(request):
    if request.method == 'GET':
        # print(request.body)
        # res = json.loads(request.body.decode("utf-8"))
        # print(res)

        data, success, msg = runSQL("SELECT xianlu_mingcheng FROM mydb.xianlu;")
        data = [{'value': data[i]['xianlu_mingcheng'], 'label': data[i]['xianlu_mingcheng'], 'leaf': False} for i in
                range(len(data))]

        if success:
            return HttpResponse(json.dumps(data))
        else:
            # print(msg)
            return HttpResponse(msg)


@csrf_exempt
def insert_sj_xianlu(request):
    if request.method == 'GET':
        # print(request.body)
        # res = json.loads(request.body.decode("utf-8"))
        # print(res)

        data, success, msg = runSQL("SELECT xianlu_mingcheng FROM mydb.xianlu;")
        data = [{'value': data[i]['xianlu_mingcheng'], 'label': data[i]['xianlu_mingcheng'], 'leaf': True} for i in
                range(len(data))]

        if success:
            return HttpResponse(json.dumps(data))
        else:
            # print(msg)
            return HttpResponse(msg)


@csrf_exempt
def insert_wz_zhandian(request):
    # return HttpResponse(request)
    if request.method == 'POST':
        # print(request.body)
        xianlu = str(request.body.decode("utf-8"))
        # print(xianlu)

        data, success, msg = runSQL("SELECT zhandian_mingcheng FROM mydb.zhandian_xianlu where xianlu_mingcheng='{}';"
                                    .format(xianlu))

        data = [{'value': data[i]['zhandian_mingcheng'], 'label': data[i]['zhandian_mingcheng'], 'leaf': True} for i in
                range(len(data))]

        # print(data)

        if success:
            return HttpResponse(json.dumps(data))
        else:
            # print(msg)
            return HttpResponse(msg)

# if __name__ == '__main__':
