from rest_framework.decorators import api_view
from rest_framework.response import Response

from Stat.models import Service, Stat
from Stat.serializers import ServiceSerializer, StatSerializer


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
        for service in request.data:
            service_instance = Service.objects.get(id=int(service['id']))
            service_serializer = ServiceSerializer(instance=service_instance, data=service)
            # save 
            if service_serializer.is_valid():
                service_serializer.save()

        stat = Stat.objects.get(id=stat_pk)
        services = Service.objects.filter(stat=stat)
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
        tasks = Stat.objects.all()
        serializer = StatSerializer(tasks, many=True)
    
    return Response(serializer.data)