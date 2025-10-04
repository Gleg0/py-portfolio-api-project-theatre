from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, permissions

from theatre.models import (
    Actor,
    Genre,
    Play,
    TheatreHall,
    Performance,
    Reservation,
    Ticket,
)
from theatre.serializers import (
    ActorSerializer,
    GenreSerializer,
    PlaySerializer,
    TheatreHallSerializer,
    PerformanceSerializer,
    ReservationSerializer,
    TicketSerializer,
)
from theatre.permissions import IsAdminOrReadOnly

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from theatre.filters import PerformanceFilter, PlayFilter

@extend_schema(tags=["Actors"])
class ActorViewSet(viewsets.ModelViewSet):
    """CRUD for actors"""
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema(tags=["Genres"])
class GenreViewSet(viewsets.ModelViewSet):
    """CRUD for genres"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema(
    tags=["Plays"],
    parameters=[
        OpenApiParameter("title", str, description="Filter by play title"),
        OpenApiParameter("description", str, description="Search by description"),
        OpenApiParameter("actors__last_name", str, description="Search by actor last name"),
    ],
)
class PlayViewSet(viewsets.ModelViewSet):
    """CRUD for plays"""
    queryset = Play.objects.prefetch_related("actors", "genres")
    serializer_class = PlaySerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = PlayFilter
    search_fields = ["title", "description", "actors__last_name"]
    ordering_fields = ["title"]
    ordering = ["title"]


@extend_schema(tags=["Theatre Halls"])
class TheatreHallViewSet(viewsets.ModelViewSet):
    """CRUD for theatre halls"""
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema(
    tags=["Performances"],
    parameters=[
        OpenApiParameter("play__title", str, description="Filter by play title"),
        OpenApiParameter("show_time", str, description="Filter by show time"),
    ],
)
class PerformanceViewSet(viewsets.ModelViewSet):
    """CRUD for performances"""
    queryset = Performance.objects.select_related("play", "theatre_hall").prefetch_related(
        "play__actors", "play__genres"
    )
    serializer_class = PerformanceSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = PerformanceFilter
    search_fields = [
        "play__title",
        "play__description",
        "play__actors__last_name",
    ]
    ordering_fields = ["show_time", "play__title"]
    ordering = ["show_time"]


@extend_schema(tags=["Tickets"])
class TicketViewSet(viewsets.ReadOnlyModelViewSet):
    """View for user tickets"""
    queryset = Ticket.objects.select_related("performance", "reservation", "performance__play")
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]


@extend_schema(tags=["Reservations"])
class ReservationViewSet(viewsets.ModelViewSet):
    """CRUD for reservations"""
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Reservation.objects.filter(user=self.request.user)
            .select_related("user")
            .prefetch_related("tickets__performance__play", "tickets__performance__theatre_hall")
        )
