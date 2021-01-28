import logging
import os
import base64
import boto3
from images import Images


class S3Functionality:
    def __init__(self, aws_access_key_id, aws_secret_access_key):
        self.s3_resource = boto3.resource("s3",
                                          aws_access_key_id=aws_access_key_id,
                                          aws_secret_access_key=aws_secret_access_key)

    def write_data_to_s3(self, image: str, bucket: str, key: str) -> dict:
        try:
            print(f"bucketname {bucket} key {key}")
            return self.s3_resource.Object(bucket, f'{key}').put(Body=image)
        except Exception as e:
            logging.error(e)
            return {"error": e}

    def get_data_from_s3(self, bucket: str, key: str) -> dict:
        content_object = self.s3_resource.Object(bucket, key)
        file_content = content_object.get()['Body'].read().decode('utf-8')
        return file_content

    def delete_image_from_s3(self, file_name):
        res = self.s3_resource.Object("priya", file_name).delete()
        return res


s3_operations = S3Functionality(aws_access_key_id="pijrewhfue",aws_secret_access_key="aeijdueafbr")


def delete_images(file_name):
    if Images.objects(name=file_name):
        res = s3_operations.delete_image_from_s3(file_name)
        if res['ResponseMetadata']['HTTPStatusCode'] // 100 == 2:
            Images.objects(name=file_name).delete()


def upload_image(file_url: str) -> dict:
    try:
        os.path.isfile(file_url)
        logging.info("file exists")
        with open(file_url, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            file_name = file_url[file_url.rindex('/') + 1:] if file_url.rindex('/') else file_url
            res = s3_operations.write_data_to_s3(encoded_string, 'priya', file_name)
            print(f"res {res}")
            if res['ResponseMetadata']['HTTPStatusCode'] // 100 == 2:
                Images(id=Images.objects().count() + 1,
                       name=file_name).save()
        return {"message": "document stored"}
    except FileNotFoundError:
        logging.error(f"file not found {file_url}")
        return {"error": f"file not found,checking at {os.getcwd()}"}


def download_image(file_name: str):
    if Images.objects(name=file_name):
        data = base64.b64decode(
        s3_operations.get_data_from_s3("priya", "/Users/priyal/photobooth/backend/download.jpg"))
        with open("download.jpg", 'wb') as fp:
            fp.write(data)
    else:
        return {"error": f"could not find image {file_name}"}


def get_list_of_all_image_name() -> list:
    image = [i['name'] for i in Images.objects().as_pymongo()]
    return image

