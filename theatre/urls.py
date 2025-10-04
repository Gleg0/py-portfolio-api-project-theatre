from rest_framework.routers import DefaultRouter

from .views import (
    ActorViewSet,
    GenreViewSet,
    PlayViewSet,
    TheatreHallViewSet,
    PerformanceViewSet,
    TicketViewSet,
    ReservationViewSet,
)

router = DefaultRouter()
router.register(r"actors", ActorViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"plays", PlayViewSet)
router.register(r"theatres", TheatreHallViewSet)
router.register(r"performances", PerformanceViewSet)
router.register(r"tickets", TicketViewSet, basename="ticket")
router.register(r"reservations", ReservationViewSet, basename="reservation")

urlpatterns = router.urls
