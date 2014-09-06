import formencode
from formencode.compound import All
from formencode.validators import Int,String,Email,TimeConverter,OneOf,DateValidator,Number
from formencode.schema import Schema
from formencode.foreach import ForEach
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
