from rest_framework import mixins, viewsets


class CreateListRetrieveDeleteViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Вьюсет, исключающий PUT/PATCH запросы.
    """
    pass


class CreateUpdateListRetrieveDeleteViewSet(
    CreateListRetrieveDeleteViewSet, mixins.UpdateModelMixin
):
    """
    Вюсет исключающий метод PUT.
    Доступные методы: GET, POST, PATCH, DELETE
    """
    pass