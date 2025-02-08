from django.contrib import admin

from contract.models import Contract, Organization, Branch

admin.site.register(Contract)
admin.site.register(Organization)
admin.site.register(Branch)
