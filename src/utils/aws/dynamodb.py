# -*- coding: utf-8 -*-
from utils.logging import get_logger
from boto3.session import Session
from boto3.dynamodb.conditions import Key

logger = get_logger()


class DynamoDB:

    def __init__(self, profile, region_name, table_name, key_name):
        session = Session(profile_name=profile)
        self.dynamodb = session.resource('dynamodb', region_name=region_name)
        self.table = self.dynamodb.Table(table_name)
        self.key_name = key_name

    def query(self, value):
        """
        queryを実行する
        :param value:
        :return:
        """
        try:
            response = self.table.query(
                KeyConditionExpression=Key(self.key_name).eq(value)
            )
            logger.info(f"dynamodb query success. response:${response}")
            return response
        except Exception as e:
            logger.error(f"dynamodb query failure. ${e}")
            raise e

    def put_item(self, item):
        """
        put_itemを実行する
        :param item:
        :return:
        """
        try:
            response = self.table.put_item(
                Item=item,
                ReturnValues="ALL_OLD"
            )
            logger.info(f"dynamodb put_item success. response:${response}")
            return response
        except Exception as e:
            logger.error(f"dynamodb put_item failure. ${e}")
            raise e

    def scan(self, prefix=None, suffix=None):
        """
        scanを実行する
        :param prefix:
        :param suffix:
        :return:
        """

        def _filter(s, prefix=None, suffix=None):
            if prefix and suffix:
                return s.startswith(prefix) and s.endswith(suffix)
            if prefix:
                return s.startswith(prefix)
            if suffix:
                return s.endswith(suffix)

            return True

        try:
            lst = self.table.scan().get("Items", [])
            logger.info(f"dynamodb scan success. response:${lst}")

            # 条件があればフィルタ
            lst = [row for row in lst if _filter(row[self.key_name], prefix, suffix)]
            # キーでソートして返す
            lst.sort(key=lambda x: x[self.key_name])
            return lst
        except Exception as e:
            logger.error(f"dynamodb scan failure. ${e}")
            raise e
