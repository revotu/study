# -*- encoding:utf-8 -*-

import json
import MySQLdb

with open('exam_list.json') as f:
    exams = json.load(f)

conn = MySQLdb.connect(
    host = 'rm-uf68040g28501oyn1rw.mysql.rds.aliyuncs.com',
    port=3306,
    user='sigma',
    passwd='sigmaLOVE2017',
    db='sigma_centauri_new'
)
cursor = conn.cursor()


for exam in exams:
    print(exam)
    cursor.execute('SELECT id FROM sigma_exercise_ob_exercise WHERE uid = "%s"' % exam)
    exercise_id = cursor.fetchone()[0]
    print(exercise_id)
    cursor.execute('SELECT `value` FROM sigma_exercise_re_exercisemeta WHERE exercise_id = %s AND `key` = "total_score"' % exercise_id)
    total_score = cursor.fetchone()[0]
    print(total_score)
    table = 'sigma_exercise_ob_answersheetitem_%s' % exam[0]
    cursor.execute('SELECT u.number, SUM(final_score) AS score FROM %s i JOIN sigma_account_us_user u ON i.student_id = u.id WHERE exercise_id = %s AND question_type <> 8 GROUP BY student_id' % (table, exercise_id))
    data = cursor.fetchall()
    # print(data)

    map_data = {"%s" % d[0]: {'score_exclude_writting': "%s" % d[1], 'exam_total_score': "%s" % total_score} for d in data}

    # print(map_data)
    with open('%s.json' % exam, 'w') as f:
        json.dump(map_data, f)

cursor.close()
conn.close()
