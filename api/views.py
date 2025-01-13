from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime
	
from firebase_admin import db

class LandingAPI(APIView):
	    
    name = 'Landing API'
    collection_name = 'misdatos'
    def get(self, request):

         # Referencia a la colección
         ref = db.reference(f'{self.collection_name}')
		    
         # get: Obtiene todos los elementos de la colección
         data = ref.get()

         # Devuelve un arreglo JSON
         return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request):
	        
         # Referencia a la colección
         ref = db.reference(f'{self.collection_name}')

         current_time  = datetime.now()
         custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')
         request.data.update({"saved": custom_format })
	        
         # push: Guarda el objeto en la colección
         new_resource = ref.push(request.data)
	        
         # Devuelve el id del objeto guardado
         return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)

class LandingAPIDetail(APIView):
    name = 'Landing Detail API'
    collection_name = 'misdatos'

    def get(self, request, pk):
        """
        Recupera un documento por su clave (pk).
        """
        ref = db.reference(f'{self.collection_name}/{pk}')
        data = ref.get()

        if data is None:
            return Response({"error": "Documento no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Actualiza un documento identificado por su clave (pk).
        """
        # Definir los campos requeridos
        campos_requeridos = {"email", "saved"}

        # Verificar que los datos enviados sean válidos
        if not isinstance(request.data, dict):
            return Response({"error": "El cuerpo de la solicitud debe ser un JSON válido."}, status=status.HTTP_400_BAD_REQUEST)

        campos_faltantes = campos_requeridos - request.data.keys()
        if campos_faltantes:
            return Response(
                {"error": f"Faltan los siguientes campos requeridos: {', '.join(campos_faltantes)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        ref = db.reference(f'{self.collection_name}/{pk}')
        existing_data = ref.get()

        if existing_data is None:
            return Response({"error": "Documento no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Actualizar los datos
        ref.update(request.data)
        return Response({"message": "Documento actualizado exitosamente."}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """
        Elimina un documento identificado por su clave (pk).
        """
        ref = db.reference(f'{self.collection_name}/{pk}')
        existing_data = ref.get()

        if existing_data is None:
            return Response({"error": "Documento no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Eliminar el documento
        ref.delete()
        return Response({"message": "Documento eliminado exitosamente."}, status=status.HTTP_204_NO_CONTENT)
    