from django.http import Http404
from django.views.generic import ListView, DetailView, View, UpdateView
from django.shortcuts import render
from django.core.paginator import Paginator
from users import mixins as user_mixins
from . import models, forms

# from django.core import paginator
# from django_countries import countries


# homeview 방법 3: class view 사용하기
class HomeView(ListView):

    """HomeView Definition"""

    model = models.Room
    paginate_by = 10
    ordering = "created"
    paginate_orphans = 5
    page_kwarg = "page"
    context_object_name = "rooms"  # object_list : the list of objects

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     now = timezone.now()
    #     context["now"] = now
    #     return context


class RoomDetail(DetailView):

    """RoomDetail Definition"""

    model = models.Room
    pk_url_kwarg = "pk"


# def room_detail(request, pk):
#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, "rooms/detail.html", context={"room": room})
#     except models.Room.DoesNotExist:
#         # return redirect(reverse("core:home"))
#         raise Http404()


class SearchView(View):
    def get(self, request):

        # roomdetail 방법 2
        country = request.GET.get("country")
        if country:

            form = forms.SearchForm(request.GET)
            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price
                if guests is not None:
                    filter_args["guests__gte"] = guests
                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms
                if beds is not None:
                    filter_args["beds__gte"] = beds
                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book:
                    filter_args["instant_book"] = True
                if superhost:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity
                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by("created")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form.as_p(), "rooms": rooms}
                )

        else:
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form.as_p()})


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = {
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    }

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404
        return room


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Room
    template_name = "room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404
        return room


# roomdetail 방법 1
# def search(request):
# selected_city = request.GET.get("city", "Anywhere")
# selected_city = str.capitalize(selected_city)
# selected_country = request.GET.get("country", "KR")
# selected_room_type = int(request.GET.get("room_type", 0))
# price = int(request.GET.get("price", 0))
# guests = int(request.GET.get("guests", 0))
# bedrooms = int(request.GET.get("bedrooms", 0))
# beds = int(request.GET.get("beds", 0))
# baths = int(request.GET.get("baths", 0))
# instant = bool(request.GET.get("instant", False))
# superhost = bool(request.GET.get("superhost", False))
# selected_amenities = request.GET.getlist("amenities", [])
# selected_facilities = request.GET.getlist("facilities", [])

# form = {
#     "selected_city": selected_city,
#     "selected_country": selected_country,
#     "selected_room_type": selected_room_type,
#     "price": price,
#     "guests": guests,
#     "bedrooms": bedrooms,
#     "beds": beds,
#     "baths": baths,
#     "instant": instant,
#     "superhost": superhost,
#     "selected_amenities": selected_amenities,
#     "selected_facilities": selected_facilities,
# }

# room_types = models.RoomType.objects.all()
# amenities = models.Amenity.objects.all()
# facilities = models.Facility.objects.all()

# choices = {
#     "countries": countries,
#     "room_types": room_types,
#     "amenities": amenities,
#     "facilities": facilities,
# }

# filter_args = {}

# if selected_city != "Anywhere":
#     filter_args["city__startswith"] = selected_city

# filter_args["country"] = selected_country

# if selected_room_type != 0:
#     filter_args["room_type__pk__exact"] = selected_room_type

# if price != 0:
#     filter_args["price__lte"] = price
# if guests != 0:
#     filter_args["guests__gte"] = guests
# if bedrooms != 0:
#     filter_args["bedrooms__gte"] = bedrooms
# if beds != 0:
#     filter_args["beds__gte"] = beds
# if baths != 0:
#     filter_args["baths__gte"] = baths

# if instant:
#     filter_args["instant_book"] = True
# if superhost:
#     filter_args["host__superhost"] = True

# if len(selected_amenities) > 0:
#     for selected_amenity in selected_amenities:
#         filter_args["amenities__pk"] = int(selected_amenity)
# if len(selected_facilities) > 0:
#     for selected_facility in selected_facilities:
#         filter_args["facilities__pk"] = int(selected_facility)

# rooms = models.Room.objects.filter(**filter_args)

# return render(
#     request,
#     "rooms/search.html",
#     context={**form, **choices, "rooms": rooms},
# )


# from math import ceil
# from django.shortcuts import render, redirect
# from django.core.paginator import EmptyPage, Paginator
# from . import models


# def all_rooms(requests):

#     # homeview 방법2: django의 도움을 받기
#     page = requests.GET.get("page", 1)
#     room_list = models.Room.objects.all()
#     paginator = Paginator(room_list, 10, orphans=5)
#     try:
#         pages = paginator.page(page)
#         return render(requests, "rooms/home.html", {"pages": pages})
#     except EmptyPage:
#         pages = paginator.page(1)
#         return redirect("/")

#     # homeview 방법 1: 수동적인 방법
#     # page = int(page or 1)
#     # page_size = 10
#     # limit = page * page_size
#     # offset = limit - page_size
#     # all_rooms = models.Room.objects.all()[offset:limit]
#     # page_count = ceil(models.Room.objects.count() / page_size)
#     # return render(
#     #     requests,
#     #     "rooms/home.html",
#     #     context={
#     #         "rooms": all_rooms,
#     #         "page": page,
#     #         "page_count": page_count,
#     #         "page_range": range(1, page_count + 1),
#     #     },
#     # )
