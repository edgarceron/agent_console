"""Contains the serializers for the users module"""
from rest_framework import serializers
from .models import DatosPersonales

class DatosPersonalesSerializer(serializers.ModelSerializer):
    """Serializer for users model"""
    class Meta:
        model = DatosPersonales
        fields = [
            'id','nombres', 'primer_apellido', 'segundo_apellido', 
            'fecha_nacimiento', 'tipo_documento', 'identificacion', 
            'telefono', 'email', 'direccion', 'departamento', 'barrio', 
            'municipio', 'tipo_servicio']

    def create(self, validated_data):
        user_obj = DatosPersonales(**validated_data)
        user_obj.save()
        return user_obj

    def update(self, instance, validated_data):
        instance.nombres = validated_data["nombres"]
        instance.primer_apellido = validated_data["primer_apellido"]
        instance.segundo_apellido = validated_data["segundo_apellido"]
        instance.fecha_nacimiento = validated_data["fecha_nacimiento"]
        instance.tipo_documento = validated_data["tipo_documento"]
        instance.identificacion = validated_data["identificacion"]
        instance.telefono = validated_data["telefono"]
        instance.email = validated_data["email"]
        instance.direccion = validated_data["direccion"]
        instance.departamento = validated_data["departamento"]
        instance.barrio = validated_data["barrio"]
        instance.municipio = validated_data["municipio"]
        instance.tipo_servicio = validated_data["tipo_servicio"]
        instance.save()
        return instance
