from django.contrib import admin

from .models import Node, NodeConnection


admin.site.register(Node)
admin.site.register(NodeConnection)