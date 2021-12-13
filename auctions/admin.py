from django.contrib import admin
from auctions.models import User, AuctionListing, Comment, Category, Bid, Watchlist

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(AuctionListing)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Watchlist)