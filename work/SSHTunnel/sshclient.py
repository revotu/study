# -*- encoding:utf-8 -*-

import MySQLdb
from sshtunnel import SSHTunnelForwarder

with SSHTunnelForwarder(
        ('106.14.161.218', 22),
        ssh_username="root",
        ssh_password="sigmaLOVE2017",
        remote_bind_address=('rm-uf68040g28501oyn1.mysql.rds.aliyuncs.com', 3306)
) as server:
    conn = MySQLdb.connect(
        host = '127.0.0.1',
        port=server.local_bind_port,
        user='sigma',
        passwd='sigmaLOVE2017',
        db='sigma_centauri'
    )
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sigma_account_us_user LIMIT 10 ')
    data = cursor.fetchall()
    print data

    cursor.close()
    conn.close()
