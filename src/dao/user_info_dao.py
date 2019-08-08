import yaml
from utils.logging import get_logger
from utils.aws.dynamodb import DynamoDB

logger = get_logger()
TABLE_NAME = 'user_info'
KEY = 'user_id'


class UserInfoDao:
    dynamodb = None

    def __init__(self, profile, region_name):
        self.dynamodb = DynamoDB(profile=profile, region_name=region_name, table_name=TABLE_NAME, key_name=KEY)

    def query(self, value):
        """
        environmentテーブルからキーの値を指定してレコードを取得します。
        :param value:
        :return:
        """
        return self.dynamodb.query(value)

    def put_item(self):
        """
        environmentテーブルへデータを投入します。
        データはdata/environment/put_data.yamlとして、対象ディレクトリに配置してください。
        :return: dynamo_response
        """
        with open(f"data/{TABLE_NAME}/put_data.yaml", "r") as f:
            put_data = yaml.load(f)
        return self.dynamodb.put_item(put_data)

    def scan(self, prefix=None, suffix=None):
        """
        environmentテーブルに入っているレコードを全取得します。
        :param prefix:
        :param suffix:
        :return:
        """
        return self.dynamodb.scan(prefix, suffix)
