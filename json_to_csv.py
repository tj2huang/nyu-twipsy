import json
import csv
import os
from dateutil import parser


def split_by_week(folder):
    out_file = None
    writer = None
    start_date = None
    last_date = None
    block_num = 0
    with open('C:/Users/Tom Work/Documents/control-dump.json', 'r') as in_file:
        for i, line in enumerate(in_file):
            if not os.path.exists(folder):
                os.makedirs(folder)
            j = json.loads(line)

            if start_date is None:
                created_at = j['created_at']
                start_date = parser.parse(created_at).day
                last_date = start_date
                start_date -= 7

            if last_date == start_date + 7:
                start_date = last_date
                if out_file:
                    out_file.close()
                block_num += 1
                print(block_num)
                out_file = open(folder + '/tweets_' + str(block_num) + '.csv', 'w', encoding='utf8')
                writer = csv.DictWriter(out_file, fieldnames=['text', 'id', 'created_at'])
                writer.writeheader()
            try:
                text = j['text']
                id = j['id']
                created_at = j['created_at']
                new_date = parser.parse(created_at).day
                if new_date != last_date:
                    print(new_date)
                    last_date = new_date
                writer.writerow({'text': text, 'id': id, 'created_at': created_at})
            except Exception as e:
                print(e)
        out_file.close()


def split_to_csv(folder, size):
    out_file = None
    writer = None
    with open('E:/Data/drinking-dump.json', 'r') as in_file:
        for i, line in enumerate(in_file):
            if not os.path.exists(folder):
                os.makedirs(folder)
            j = json.loads(line)
            if i % size == 0:
                if out_file:
                    out_file.close()
                block_num = str(int(i/size))
                print(block_num)
                out_file = open(folder + '/tweets_' + block_num + '.csv', 'w', encoding='utf8')
                writer = csv.DictWriter(out_file, fieldnames=['text', 'id', '_id', 'created_at'])
                writer.writeheader()
            try:
                text = j['text']
                id = j['id']
                _id = j['_id']['$oid']
                created_at = j['created_at']
                writer.writerow({'text': text, 'id': id, '_id': _id, 'created_at': created_at})
            except Exception as e:
                print(e)
        out_file.close()

if __name__ == '__main__':
    split_to_csv('E:/data/tweets_split', 1000000)