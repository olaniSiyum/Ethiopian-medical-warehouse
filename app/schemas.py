from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MedicalItemBase(BaseModel):
    channel_title: str
    date: datetime
    message: str
    views: int

class TelegramMessage(MedicalItemBase):
    id: int

    class Config:
        orm_mode = True

class ObjectDetectionBase(BaseModel):
    image_id: int
    name: str
    confidence: float
    yolo_xmin: float
    yolo_ymin: float
    yolo_xmax: float
    yolo_ymax: float

class ObjectDetection(ObjectDetectionBase):
    id: int

    class Config:
        orm_mode = True

class TelegramMessageCreate(MedicalItemBase):
    pass

class ObjectDetectionCreate(ObjectDetectionBase):
    pass

class TelegramMessageUpdate(BaseModel):
    message_link: Optional[str] = None
    channel_title: Optional[str] = None
    date: Optional[datetime] = None
    message: Optional[str] = None
    views: Optional[int] = None

class ObjectDetectionUpdate(BaseModel):
    image_id: Optional[int] = None
    name: Optional[str] = None
    confidence: Optional[float] = None
    yolo_xmin: Optional[float] = None
    yolo_ymin: Optional[float] = None
    yolo_xmax: Optional[float] = None
    yolo_ymax: Optional[float] = None
