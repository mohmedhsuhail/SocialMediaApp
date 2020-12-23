from django.contrib import admin
from . import models
# Register your models here.
class GroupMemberInline(admin.StackedInline):
	model = models.GroupMember

class GroupAdmin(admin.ModelAdmin):
	inlines = [GroupMemberInline,]
	
admin.site.register(models.Group,GroupAdmin)
admin.site.register(models.GroupMember)