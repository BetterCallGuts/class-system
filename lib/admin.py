from django.contrib import admin

from .models        import Library, LibraryCharges
from Thoth.admin    import final_boss
from django.db.models import Count




class Library_ChargesInlinestacked(admin.StackedInline):
  
  model               = LibraryCharges
  extra               = 0
  verbose_name        = "فاتورة"
  verbose_name_plural = "فواتير المكتبة"
  

class LibraryAdminStyle(admin.ModelAdmin):

  fieldsets = (
    
    ("تفاصيل المكتية ", {
      "fields" : (
        "name",
        "desc"
        
      )
    }),
  )
  list_display = (
    "name",
    "total_lib_charges_this_month",
    "total_lib_charges",
    
    
  )
  inlines = (
    Library_ChargesInlinestacked,
  )
  def get_queryset(self, request):
    # def queryset(self, request): # For Django <1.6
        qs = super(LibraryAdminStyle, self).get_queryset(request)
        
        # qs = super(CustomerAdmin, self).queryset(request) # For Django <1.6
        qs = qs.annotate(Count('librarycharges'))
        
        return qs

  def number_of_orders(self, obj):
      return obj.order__count
  number_of_orders.admin_order_field = 'order__count'

final_boss.register(Library, LibraryAdminStyle)