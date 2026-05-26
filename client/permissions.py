#
# class ModerationPermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.groups.filter(name="Модератор").exists()
#
#
# class IsOwner(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user == obj.owner
