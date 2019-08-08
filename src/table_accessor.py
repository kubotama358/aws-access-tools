import os
import click
import yaml
import json
import openpyxl as px
from openpyxl.utils import column_index_from_string
from dao.environment_dao import EnvironmentDao
from dao.user_info_dao import UserInfoDao
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


@main.command(help='key指定でenvironmentテーブルからデータを取得する。')
@click.option('--profile_name', '-p', help='credentials', required=True)
@click.option('--region_name', '-r', help='region', default="ap-northeast-1")
@click.option('--value', '-v', help='value')
def get_environment(profile_name, region_name, value):
    logger.info("environmentテーブルからデータを取得します。")
    dao = EnvironmentDao(profile=profile_name, region_name=region_name)
    response = dao.query(value)

    logger.info(f"environmentテーブルからデータを取得します。response:{response}")


@main.command(help='environmentテーブルのデータを更新する。put対象データはdata/${TABLE_ANME}/put_data.yamlに記載して下さい。')
@click.option('--profile_name', '-p', help='credentials', required=True)
@click.option('--region_name', '-r', help='region', default="ap-northeast-1")
def put_environment(profile_name, region_name):
    logger.info("environmentテーブルにデータを投入します。")
    dao = EnvironmentDao(profile=profile_name, region_name=region_name)
    response = dao.put_item()

    logger.info(f"environmentテーブルの更新が完了しました。response:{response}")


if __name__ == "__main__":
    main()
