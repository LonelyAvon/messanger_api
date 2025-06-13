import asyncio
from io import BytesIO
from json import dumps
from typing import Annotated, Optional, Union

from fastapi import Depends
from minio import Minio
from minio.error import S3Error

from app.settings import settings


class AsyncMinIOClient:
    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        secure: bool = False,
        public_url: Optional[str] = None,
    ):
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )
        self.public_url = public_url or endpoint
        self.loop = asyncio.get_event_loop()

    async def upload_file(
        self,
        bucket_name: str,
        file_path: str,
        file_data: Union[bytes, BytesIO],
        content_type: str = "application/octet-stream",
    ) -> str:
        """Загружает файл и возвращает публичную ссылку"""
        await self.ensure_bucket_exists(bucket_name)

        if isinstance(file_data, bytes):
            file_data = BytesIO(file_data)

        # Получаем размер данных перед передачей
        file_data.seek(0, 2)  # Перемещаемся в конец файла
        length = file_data.tell()
        file_data.seek(0)  # Возвращаемся в начало

        # Передаем параметры как позиционные аргументы
        await self._run_sync(
            self.client.put_object,
            bucket_name,
            file_path,
            file_data,
            length,  # Позиционный параметр длины
            content_type,  # Позиционный параметр типа содержимого
        )

        return self.get_public_url(bucket_name, file_path)

    async def _run_sync(self, func, *args):
        """Обертка для синхронных вызовов"""
        return await self.loop.run_in_executor(None, lambda: func(*args))

    async def create_bucket(self, bucket_name: str) -> None:
        """Создает бакет и устанавливает публичный доступ"""
        try:
            if not await self._run_sync(self.client.bucket_exists, bucket_name):
                await self._run_sync(self.client.make_bucket, bucket_name)

            # Формируем политику как JSON-строку
            policy = dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": "*",
                            "Action": ["s3:GetObject"],
                            "Resource": [f"arn:aws:s3:::{bucket_name}/*"],
                        }
                    ],
                }
            )

            await self._run_sync(
                self.client.set_bucket_policy,
                bucket_name,
                policy,  # Передаем строку вместо словаря
            )
        except S3Error as e:
            if e.code != "BucketAlreadyOwnedByYou":
                raise
        except Exception as e:
            print(f"Error setting policy: {str(e)}")
            raise

    def get_public_url(self, bucket_name: str, file_path: str) -> str:
        """Генерирует публичную ссылку на файл"""
        return f"{self.public_url}/{bucket_name}/{file_path}"

    async def ensure_bucket_exists(self, bucket_name: str) -> None:
        """Проверяет и создает бакет при необходимости"""
        try:
            if not await self._run_sync(self.client.bucket_exists, bucket_name):
                await self.create_bucket(bucket_name)
        except S3Error as e:
            print(f"Error ensuring bucket exists: {e}")

    async def __aenter__(self):
        """Вызывается при входе в контекст"""
        await self._validate_connection()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Вызывается при выходе из контекста"""
        await self._cleanup_resources()

    async def _validate_connection(self):
        """Проверка подключения к MinIO"""
        try:
            await self._run_sync(self.client.list_buckets)
        except Exception as e:
            raise ConnectionError(f"MinIO connection failed: {str(e)}") from e

    async def _cleanup_resources(self):
        """Очистка ресурсов (можно добавить при необходимости)"""
        pass

    @staticmethod
    async def get_minio():
        async with AsyncMinIOClient(
            f"{settings.MINIO_HOST}:{settings.MINIO_API_PORT}",
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False,
            public_url="http://212.20.53.169:8900",  # Публичный URL для доступа
        ) as client:
            yield client


MinioClient = Annotated[AsyncMinIOClient, Depends(AsyncMinIOClient.get_minio)]
