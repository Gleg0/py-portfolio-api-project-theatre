from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from .models import (
    Actor,
    Genre,
    Play,
    TheatreHall,
    Performance,
    Reservation,
    Ticket,
)

User = get_user_model()


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class PlaySerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    actor_ids = serializers.PrimaryKeyRelatedField(
        queryset=Actor.objects.all(),
        many=True,
        write_only=True,
        required=False,
    )
    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model = Play
        fields = (
            "id",
            "title",
            "description",
            "actors",
            "genres",
            "actor_ids",
            "genre_ids",
        )

    def create(self, validated_data):
        actor_ids = validated_data.pop("actor_ids", [])
        genre_ids = validated_data.pop("genre_ids", [])
        play = Play.objects.create(**validated_data)
        if actor_ids:
            play.actors.set(actor_ids)
        if genre_ids:
            play.genres.set(genre_ids)
        return play

    def update(self, instance, validated_data):
        actor_ids = validated_data.pop("actor_ids", None)
        genre_ids = validated_data.pop("genre_ids", None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        if actor_ids is not None:
            instance.actors.set(actor_ids)
        if genre_ids is not None:
            instance.genres.set(genre_ids)
        return instance


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row")


class PerformanceSerializer(serializers.ModelSerializer):
    play = PlaySerializer(read_only=True)
    play_id = serializers.PrimaryKeyRelatedField(
        queryset=Play.objects.all(), write_only=True, source="play"
    )
    theatre_hall = TheatreHallSerializer(read_only=True)
    theatre_hall_id = serializers.PrimaryKeyRelatedField(
        queryset=TheatreHall.objects.all(),
        write_only=True,
        source="theatre_hall",
    )

    class Meta:
        model = Performance
        fields = (
            "id",
            "play",
            "play_id",
            "theatre_hall",
            "theatre_hall_id",
            "show_time",
        )


class TicketSerializer(serializers.ModelSerializer):
    performance = PerformanceSerializer(read_only=True)
    performance_id = serializers.PrimaryKeyRelatedField(
        queryset=Performance.objects.all(),
        write_only=True,
        source="performance",
    )
    reservation = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "performance",
            "performance_id",
            "reservation",
        )

    def validate(self, data):
        performance = data.get("performance")
        row = data.get("row")
        seat = data.get("seat")

        if performance is None or row is None or seat is None:
            return data

        hall = performance.theatre_hall
        if row < 1 or seat < 1:
            raise serializers.ValidationError(
                "Row and seat must be positive integers."
            )
        if row > hall.rows or seat > hall.seats_in_row:
            raise serializers.ValidationError(
                f"Seat out of bounds for hall "
                f"'{hall.name}' (rows={hall.rows}, "
                f"seats_in_row={hall.seats_in_row})."
            )
        qs = Ticket.objects.filter(performance=performance, row=row, seat=seat)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "This seat is already taken for the performance."
            )
        return data


class TicketCreateNestedSerializer(serializers.ModelSerializer):
    performance = serializers.PrimaryKeyRelatedField(
        queryset=Performance.objects.all()
    )

    class Meta:
        model = Ticket
        fields = ("row", "seat", "performance")


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketCreateNestedSerializer(many=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "user", "tickets")
        read_only_fields = ("id", "created_at", "user")

    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets", [])
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if user is None or not user.is_authenticated:
            raise serializers.ValidationError(
                "Authentication required to create reservation."
            )

        with transaction.atomic():
            reservation = Reservation.objects.create(
                user=user, **validated_data
            )
            for tdata in tickets_data:
                performance = tdata["performance"]  # instance
                row = tdata["row"]
                seat = tdata["seat"]

                hall = performance.theatre_hall
                if (
                    row < 1
                    or seat < 1
                    or row > hall.rows
                    or seat > hall.seats_in_row
                ):
                    raise serializers.ValidationError(
                        f"Invalid seat {row}-{seat} for hall '{hall.name}'."
                    )
                if Ticket.objects.filter(
                    performance=performance, row=row, seat=seat
                ).exists():
                    raise serializers.ValidationError(
                        f"Seat "
                        f"{row}-{seat} "
                        f"is already taken for this performance."
                    )
                Ticket.objects.create(
                    performance=performance,
                    row=row,
                    seat=seat,
                    reservation=reservation,
                )
        return reservation
