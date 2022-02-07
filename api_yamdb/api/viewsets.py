from rest_framework import mixins, viewsets


class CreateListDeleteViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """
    Вьюсет, исключающий PUT/PATCH запросы,
    DETAIL просмотр запрещен.
    """
    pass
