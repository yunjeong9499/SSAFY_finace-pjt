from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    작성자만 수정/삭제 가능. 나머지는 읽기만 허용.
    """

    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모두 허용 (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # 그 외 요청은 작성자에게만 허용
        return obj.author == request.user
