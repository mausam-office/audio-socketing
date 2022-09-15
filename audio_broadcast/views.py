from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Audio, DeviceStatus
from .serializers import AudioSerializer, DeviceStatusSerializer, DeviceStatusSerializerResponse
from datetime import datetime

format = "%Y-%m-%dT%H:%M:%S"
format_current = "%Y-%m-%d %H:%M:%S"
threshold_minutes = 1  # in minutes

class AudioView(APIView):
    def post(self, request):
        try:
            data = request.data
            print('Try: ', data)
        except:
            data = request.POST
            print('Except: ', data)

        serializer = AudioSerializer(data=data)
        # Device name is not validated as only approved device name appears on list
        # TODO Only allow to post audio data for active devices 
        # As inactive device can't obtain the data So there is no point in sending the data
        if serializer.is_valid():
            serializer.save()
            return Response({"Acknowledge":"Successfully done."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        audios = Audio.objects.all()
        serializer = AudioSerializer(audios, many=True)
        return Response(serializer.data)


class DeviceRegistrationView(APIView):
    def post(self, request):
        try:
            data = request.POST
            print('Try: ', data)
        except:
            data = request.data
            print('Except: ', data)
        serializer = DeviceStatusSerializer(data=data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                record = DeviceStatus.objects.get(device_name=data['device_name'])
            except:
                record = False

            if record:
                print("if maa: ")
                record.is_active = data['is_active']
                record.last_req_time =  datetime.now()
                record.save()
                return Response({'Acknowledge':'Time Updated'},status=status.HTTP_200_OK)
            else:
                print("else maa")
                serializer.save()
                return Response({'Acknowledge':'Registered'},status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class DeviceStatusView(APIView):
    def get(self, request):
        # Filter approved devices 
        devices = DeviceStatus.objects.filter(is_approved=True)
        serializer_devices = DeviceStatusSerializerResponse(devices, many=True)

        #Updating request time
        try:
            for data in serializer_devices.data:
                data = dict(data)

                # split('.')[0] -> removes millisecond part
                last_req_time = data['last_req_time'].split('.')[0]   # In string of ISO format, convert it into  datetime format.
                last_req_time = datetime.strptime(last_req_time, format)
                
                # current = datetime.strptime(datetime.now().strftime(format_current), format_current)

                diff = datetime.strptime(datetime.now().strftime(format_current), format_current) - last_req_time
                diff_minutes = diff.total_seconds()/60  # Calulated the time in minutes
                # print('diff_minutes',diff_minutes)
                
                device_record = DeviceStatus.objects.get(device_name=data['device_name'])
                # print(device_record)
                if diff_minutes > threshold_minutes:
                    device_record.is_active = False
                else:
                    device_record.is_active = True
                device_record.save()
                # print(device_name, last_req_time, current, diff_minutes)
        except:
            pass
        
        devices = DeviceStatus.objects.all()
        serializer_devices = DeviceStatusSerializerResponse(devices, many=True)
        audio_records_count = Audio.objects.filter(is_sent=True).count()

        return Response({'devices': serializer_devices.data, 'num_pending_records':audio_records_count})   

    
class DeviceApprovalView(APIView):
    def get(self, request):
        try:
            device_name = request.GET['device_name']
        except:
            device_name = dict(request.data)['device_name'][0]
        print(request.GET, device_name)
        try:
            device = DeviceStatus.objects.filter(device_name=device_name)
            serializer = DeviceStatusSerializerResponse(device, many=True)
            idx = serializer.data[0]['id']

            device = DeviceStatus.objects.get(id=idx)
            device.is_approved = True
            device.save()
            return Response({'Acknowledge' : 'Approved'})
        except:
            return Response({'Acknowledge' : 'Not Approved'})


class LogBackupAndDeleteView(APIView):
    def get(self, request):
        # Delete the records once the timestamp is 
        audio_records = Audio.objects.filter(is_sent=True)
        serializer = AudioSerializer(audio_records, many=True)

        log_data = {}
        for row in serializer.data:
            device_name = row['device_name']
            if device_name not in log_data:
                log_data[device_name] = []
            log_data[device_name].append(row['created_at'].replace('T', ' '))
            
            # audio_record = Audio.objects.get(id=row['id'])
            # We need to delete the audio records after getting timestamp
            # audio_record.delete()

        response_body = []
        for key, value in log_data.items():
            response_body.append({'device_name':key, 'timestamp':value})
        
        return Response(response_body)
