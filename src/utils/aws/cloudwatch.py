from boto3.session import Session
from utils.logging import get_logger

logger = get_logger()


class Cloudwatch:
    def __init__(self, profile):
        session = Session(profile_name=profile)
        self.cloudwatch = session.client('cloudwatch')

    def get_metrics(self, name_space, metric_name, dimensions, start_time, end_time, period, statics):
        """
        指定したメトリクスを取得します。
        :param name_space: ex.)"AWS/DynamoDB"
        :param metric_name: ex.)"ConsumedReadCapacityUnits"
        :param dimensions: ex.)[{
                "Name": "TableName",
                "Value": hoge
            }]
        :param start_time: ex.)1564736128000
        :param end_time: ex.)1564736128000
        :param period: ex.)1800（/seconds）
        :param statics: ex.)["Maximum"]
        :return:
        """
        try:
            response = self.cloudwatch.get_metric_statistics(
                Namespace=name_space,
                MetricName=metric_name,
                Dimensions=dimensions,
                StartTime=start_time,
                EndTime=end_time,
                Period=period,
                Statistics=statics
            )
            logger.info(f"cloudwatch get_metrics success. response:${response}")
            return response
        except Exception as e:
            logger.error(f"cloudwatch get_metrics failed. ${e}")
            raise e
