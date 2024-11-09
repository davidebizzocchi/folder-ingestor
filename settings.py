from cat.mad_hatter.decorators import plugin
from pydantic import BaseModel, field_validator

class MySettings(BaseModel):
    directory: str = "myfiles"
    deep_search: bool = True

@plugin
def settings_model():
    return MySettings
