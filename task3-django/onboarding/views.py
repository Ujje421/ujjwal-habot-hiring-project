from rest_framework import generics, status
from rest_framework.response import Response
from .models import StudentOnboarding
from .serializers import StudentOnboardingSerializer

class StudentOnboardingCreateView(generics.CreateAPIView):
    queryset = StudentOnboarding.objects.all()
    serializer_class = StudentOnboardingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                {
                    "message": "Student onboarding record created successfully.",
                    "status": serializer.data.get('dcyn_clearance_status'),
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        return Response(
            {
                "message": "Validation failed based on strict DCYN rules.",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
