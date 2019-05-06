from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import *
from random import randrange

CHARSET = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'
LENGTH = 12
MAX_TRIES = 32

class UserAdmin(SummernoteModelAdmin):
    list_display = ['name', 'is_staff','is_educator','is_active']
    search_fields = ('name',)
    readonly_fields = ('unique_referral_code',)

    # def get_form(self, request, obj=None, **kwargs):
    #     self.exclude = []
    #     if not request.user.is_superuser:
    #         self.exclude.append('password')
    #         self.exclude.append('is_superuser')
    #         self.exclude.append('is_university_staff')
    #         self.exclude.append('is_ucet_staff')
    #         self.exclude.append('is_faculty')
    #         self.exclude.append('is_staff')
    #         self.exclude.append('user_permissions')
    #         self.exclude.append('groups')
    #         self.exclude.append('position')
    #         self.exclude.append('last_login')
    #         self.exclude.append('role')
    #     return super(UserAdmin, self).get_form(request, obj, **kwargs)


    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.id)

    def save_model(self, request, obj, form, change):
        loop_num = 0
        unique = False
        while not unique:
            if loop_num < MAX_TRIES:
                new_code = ''
                for i in range(LENGTH):
                    new_code += CHARSET[randrange(0, len(CHARSET))]
                if not User.objects.filter(unique_referral_code=new_code):
                    obj.unique_referral_code = new_code
                    unique = True
                loop_num += 1
            else:
                raise ValueError("Couldn't generate a unique code.")
        obj.save()

admin.site.register(User, UserAdmin)