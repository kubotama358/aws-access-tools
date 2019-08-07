import os
import click
import yaml
import json
import openpyxl as px
from openpyxl.utils import column_index_from_string
from utils.logging import get_logger
from utils.aws import dynamodb

logger = get_logger()

CONFIG_DIR = 'config'
TABLE_CONFIG_NAME = 'table_config.yaml'


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        logger.info(ctx.get_help())


@main.command(help='message-resourceデータを挿入する')
@click.option('--profile_name', '-p', help='credentials', required=True)
@click.option('--region_name', '-r', help='region', default="ap-northeast-1")
@click.option('--table_name', '-t', help='table_name', required=True)
def push_table_data(profile_name, region_name, table_name):
    config = _get_table_config()
    _dynamodb = dynamodb.DynamoDB(
        profile=profile_name,
        region_name=region_name,
        table_name=table_name,
        key_name=config['key_name']
    )

    _dynamodb.put_item()

    message_resources = _read('message_resources', f"{domain}.yaml")

    for data in message_resources:
        logger.info(data)
        _dynamodb.put_item(data)


def _get_table_config():
    logger.info('設定ファイルを読み込みます。')
    file = f"{CONFIG_DIR}/{TABLE_CONFIG_NAME}.yaml"
    with open(file, 'r') as f:
        config = yaml.load(f)
    return config


if __name__ == "__main__":
    main()
