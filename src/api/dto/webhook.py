from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class UserIdentityDTO(BaseModel):
    principal_id: str = Field(..., alias='principalId')


class RequestParametersDTO(BaseModel):
    principal_id: str = Field(..., alias='principalId')
    region: str
    source_ip_address: str = Field(..., alias='sourceIPAddress')


class ResponseElementsDTO(BaseModel):
    content_length: str = Field(..., alias='content-length')
    x_amz_id_2: str = Field(..., alias='x-amz-id-2')
    x_amz_request_id: str = Field(..., alias='x-amz-request-id')
    x_minio_deployment_id: str = Field(..., alias='x-minio-deployment-id')
    x_minio_origin_endpoint: str = Field(..., alias='x-minio-origin-endpoint')


class OwnerIdentityDTO(BaseModel):
    principal_id: str = Field(..., alias='principalId')


class BucketDTO(BaseModel):
    name: str
    owner_identity: OwnerIdentityDTO = Field(..., alias='ownerIdentity')
    arn: str


class UserMetadataDTO(BaseModel):
    content_type: str = Field(..., alias='content-type')


class ObjectDTO(BaseModel):
    key: str
    size: int
    e_tag: str = Field(..., alias='eTag')
    content_type: str = Field(..., alias='contentType')
    user_metadata: UserMetadataDTO = Field(..., alias='userMetadata')
    sequencer: str


class S3DTO(BaseModel):
    s3_schema_version: str = Field(..., alias='s3SchemaVersion')
    configuration_id: str = Field(..., alias='configurationId')
    bucket: BucketDTO
    object: ObjectDTO


class SourceDTO(BaseModel):
    host: str
    port: str
    user_agent: str = Field(..., alias='userAgent')


class RecordDTO(BaseModel):
    event_version: str = Field(..., alias='eventVersion')
    event_source: str = Field(..., alias='eventSource')
    aws_region: str = Field(..., alias='awsRegion')
    event_time: str = Field(..., alias='eventTime')
    event_name: str = Field(..., alias='eventName')
    user_identity: UserIdentityDTO = Field(..., alias='userIdentity')
    request_parameters: RequestParametersDTO = Field(..., alias='requestParameters')
    response_elements: ResponseElementsDTO = Field(..., alias='responseElements')
    s3: S3DTO
    source: SourceDTO


class WebhookRequestDTO(BaseModel):
    event_name: str = Field(..., alias='EventName')
    key: str = Field(..., alias='Key')
    records: List[RecordDTO] = Field(..., alias='Records')
