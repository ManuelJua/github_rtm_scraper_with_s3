# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import boto3
from datetime import date


class GithubRtmScraperWithS3Pipeline:
    def __init__(self, aws_access_key_id, aws_secret_access_key, bucket_name):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.bucket_name = bucket_name
        self.client = None
        
    @classmethod
    def from_crawler(cls, crawler):
        
        aws_access_key_id = crawler.settings.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = crawler.settings.get('AWS_SECRET_ACCESS_KEY')
        bucket_name = crawler.settings.get('AWS_S3_BUCKET_NAME')

        return cls(aws_access_key_id, aws_secret_access_key, bucket_name)
        

    def open_spider(self, spider):
        self.client = boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )
        
    def close_spider(self,spider):
       self.client.upload_file('prop-{}.csv'.format(date.today()), self.bucket_name,'right_to_move_files/right_to_move-{}.csv'.format(date.today()))
        
    def process_item(self, item, spider):
        return item