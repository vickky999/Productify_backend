from django.contrib import admin

from .models import *
from django.db import models  
from django.core.paginator import Paginator
from django.core.cache import cache

# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follower)
admin.site.register(PublicChatRoom)
admin.site.register(PublicChat)
#admin.site.register(Like)
#admin.site.register(Saved)

class PublicChatRoomAdmin(admin.ModelAdmin):
     list_display = ['id','title']
     search_display = ['id','title']
       
     class Meta:
        model = PublicChatRoom

from django.core.paginator import Paginator
from django.core.cache import cache

  
class CachingPaginator(Paginator):
    def _get_count(self):

        if not hasattr(self, "_count"):
            self._count = None

        if self._count is None:
            try:
                key = "adm:{0}:count".format(hash(self.object_list.query.__str__()))
                self._count = cache.get(key, -1)
                if self._count == -1:
                    self._count = super().count
                    cache.set(key, self._count, 3600)

            except:
                self._count = len(self.object_list)
        return self._count

    count = property(_get_count)


  
class PublicChatAdmin(admin.ModelAdmin):
    list_display = ['room','user','timestamp','content']
    list_filter = ['room','user','timestamp',]
    readonly_fields = ['room','user','timestamp','id']

    show_full_result_count=False
    paginator = CachingPaginator

    class Meta :
        model = PublicChat


