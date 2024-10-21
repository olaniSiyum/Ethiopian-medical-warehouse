from sqlalchemy import Column, Integer, String, TIMESTAMP, Float
from app.database import Base

class MedicalItem(Base):
    __tablename__ = "medical_data_transformed"

    id = Column(Integer, primary_key=True, index=True)
    channel_title = Column(String)
    message_link = Column(String)
    date = Column(TIMESTAMP(timezone=True))
    message = Column(String)
    views = Column(Integer)

class ObjectDetection(Base):
    __tablename__ = "yollo_detections"

    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer)
    name = Column(String)
    confidence = Column(Float)
    yolo_xmin = Column(Float)
    yolo_ymin = Column(Float)
    yolo_xmax = Column(Float)
    yolo_ymax = Column(Float)
