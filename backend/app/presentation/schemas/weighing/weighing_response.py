from .weighing_base import WeighingBaseSchema

class WeighingResponseSchema(WeighingBaseSchema):
    id: int

    class Config:
        from_attributes = True








































