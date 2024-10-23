from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.db.models import Q

from Stat.models import Service, Stat
from Stat.serializers import ServiceSerializer, StatSerializer

from facilitators.models import Facilitator
from facilitators.serializers import FacilitatorSerializer


@api_view(["GET"])
def apiOverview(request):
    routes = {
        'overview: /api/',
        'Stats(GET, PUT, POST): /api/stats/',
        'Stats detail(POST): /api/stats/<int:pk>/',
    }
    return Response(routes)

@api_view(["GET","POST","PUT","DELETE"])
def stats(request, pk=None):
    # get single stat
    if pk and request.method == "GET":
        task = Stat.objects.get(id=pk)
        serializer = StatSerializer(task, many=False)

    # update stat
    elif pk and request.method == "PUT":
        task = Stat.objects.get(id=pk)
        serializer = StatSerializer(instance=task, data=request.data)

        if serializer.is_valid():
            serializer.save()
            
    # create new stat
    elif not pk and request.method == "POST":
        serializer = StatSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
        
    # get all stats
    elif not pk and request.method == "GET":
        tasks = Stat.objects.all()
        serializer = StatSerializer(tasks, many=True)
    
    return Response(serializer.data)

@api_view(["GET","POST","PUT","DELETE"])
def serviceApiView(request, pk=None, stat_pk=None):
    # get services
    if stat_pk and request.method == "GET":
        stat = Stat.objects.get(id=stat_pk)
        services = Service.objects.filter(stat=stat)
        serializer = ServiceSerializer(services, many=True)

    # update services
    elif stat_pk and request.method == "PUT":
        data = request.data
        services = request.data.get('services')
        message = request.data.get('message')
        firstservice = request.data.get('first')

        if message == 0:
            for service in services:
                service_instance = Service.objects.get(id=int(service['id']))
                service_serializer = ServiceSerializer(instance=service_instance, data=service)
                # save 
                if service_serializer.is_valid():
                    service_serializer.save()
        elif message == 1:
            firstserviceinstance = Service.objects.get(id=int(firstservice['id']))
            service_serializer = ServiceSerializer(instance=firstserviceinstance, data=firstservice)
            # save 
            if service_serializer.is_valid():
                firstserviceinstance = service_serializer.save()
            
            for service in services:
                service_instance = Service.objects.get(id=int(service['id']))
                service_instance.facilitators_available = firstserviceinstance.junior
                

        stat = Stat.objects.get(id=stat_pk)
        services = stat.services.all()
        serializer = ServiceSerializer(services, many=True)

        response = {
            'status': 200,
            'data': serializer.data
        }

        return Response(response)

        # if serializer.is_valid():
        #     serializer.save()
            
    # create new services
    elif stat_pk and request.method == "POST":
        serializer = StatSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
        
    # get all stats
    elif not pk and request.method == "GET":
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
    
    return Response(serializer.data)


class ServiceAPIView(APIView):
    def get(self, request, pk=None):
        stat_id = request.query_params.get('stat_id')
        
        if pk:
            service = get_object_or_404(Service, pk=pk)
            serializer = ServiceSerializer(service)
            return Response(serializer.data)
        elif stat_id:
            services = Service.objects.filter(stat__id=stat_id)
            serializer = ServiceSerializer(services, many=True)
            return Response(serializer.data)
        else:
            services = Service.objects.all()
            serializer = ServiceSerializer(services, many=True)
            return Response(serializer.data)

    def post(self, request):
        if isinstance(request.data, list):
            serializer = ServiceSerializer(data=request.data, many=True)
        else:
            serializer = ServiceSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if pk:
            service = get_object_or_404(Service, pk=pk)
            serializer = ServiceSerializer(service, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            services_data = request.data
            if not isinstance(services_data, list):
                return Response({"error": "Expected a list of services"}, status=status.HTTP_400_BAD_REQUEST)
            
            updated_services = []
            for service_data in services_data:
                service = get_object_or_404(Service, pk=service_data.get('id'))
                serializer = ServiceSerializer(service, data=service_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    updated_services.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(updated_services)

    def delete(self, request, pk=None):
        if pk:
            service = get_object_or_404(Service, pk=pk)
            service.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "A specific service ID (pk) is required for deletion."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET","PUT"])
def facilitatorChecklistView(request, stat_pk=None, service_pk=None):
    if request.method == 'GET' and stat_pk:
        stat = Stat.objects.get(id=stat_pk)
        return_list = []

        for service in stat.services.all():
            fs = service.facilitators_available.all()
            serializer = FacilitatorSerializer(fs, many=True)
            return_list.append({
                'id': service.id,
                'service': service.name,
                'facilitators': serializer.data
            })

    if request.method == 'PUT':
        updated_service:dict = request.data
        service = Service.objects.get(id=updated_service.get('id'))

        facilitators = []
        # first we create a list of the faciltator models received
        for dic in updated_service.get('facilitators'):
            # facilitator match
            fmatch = Facilitator.objects.get(id=dic.get('id'))
            facilitators.append(fmatch)
        
        # clear the facilitators available field
        service.facilitators_available.clear()
        # set the list as the cleared field
        service.facilitators_available.set(facilitators)
        # save the service
        service.save()

        return_list = True


    return Response(return_list)

@api_view(["GET"])
def facilitatorsApiView(request):
    if request.method == 'GET':
        fs = Facilitator.objects.filter(active=True).order_by('name')
        serializer = FacilitatorSerializer(fs, many=True)
    return Response(serializer.data)
