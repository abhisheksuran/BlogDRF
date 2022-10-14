"""My custom mixins"""

from rest_framework import mixins

class RUDMixi(mixins.DestroyModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):

    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.destroy(request, *args, **kwargs)
