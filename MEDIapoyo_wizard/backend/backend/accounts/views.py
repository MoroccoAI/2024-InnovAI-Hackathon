import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from .models import CustomUser
from rest_framework_simplejwt.exceptions import InvalidToken

# Set up logging
logger = logging.getLogger(__name__)

class CreateUserView(APIView):
    def post(self, request):
        # Récupérer les données du formulaire envoyées
        username = request.data.get('username')
        email = request.data.get('email')

        # Vérifier si l'utilisateur existe déjà
        if CustomUser.objects.filter(username=username).exists():
            return Response({"detail": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        if CustomUser.objects.filter(email=email).exists():
            return Response({"detail": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Si l'utilisateur n'existe pas, on continue avec la création
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():  # Si les données sont valides
            serializer.save()
            return Response({"detail": "User created successfully"}, status=status.HTTP_201_CREATED)

        # Si les données sont invalides, on renvoie les erreurs
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    def post(self, request):
        # Récupérer les données du formulaire
        username = request.data.get("username")
        password = request.data.get("password")

        # Vérifier si les données sont présentes
        if not username or not password:
            return Response(
                {"detail": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Authentifier l'utilisateur
        user = authenticate(username=username, password=password)

        if user is not None:
            # Créer un jeton JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response(
                {
                    "access_token": access_token,
                    "refresh_token": str(refresh),
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            logger.error("Pas de jeton trouvé dans l'en-tête Authorization.")
            return Response({"detail": "Jeton manquant."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Extraire le jeton Bearer
            token = auth_header.split(' ')[1]
            refresh_token = RefreshToken(token)
            
            # Blacklister le jeton
            refresh_token.blacklist()

            # Répondre à la déconnexion
            return Response({"detail": "Déconnexion réussie."}, status=status.HTTP_200_OK)
        except InvalidToken:
            # Si le jeton est invalide
            logger.error("Jeton invalide lors de la tentative de déconnexion.")
            return Response({"detail": "Jeton invalide."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Gérer toute autre exception
            logger.error(f"Erreur lors de la déconnexion: {str(e)}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
