import formencode
from formencode.validators import Int,String,Number,FieldStorageUploadConverter
from formencode.schema import Schema
from formencode import Invalid

class ValidateGraphGenerateForm(Schema):
    allow_extra_fields = True
    title = String(if_missing="")
    graph_type = String(if_missing="binary")
    graph_height = Int(if_missing=1)
    graph_width =Int(if_missing=1)
    canvas_height = Int(if_missing=8)
    canvas_width = Int(if_missing=6)
    minv = Number(if_missing=None)
    maxv = Number(if_missing=None)
    canvas_width = Int()
    canvas_height = Int()
    splitnum = Int()
    file = FieldStorageUploadConverter(not_empty=True)
