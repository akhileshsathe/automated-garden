from django.shortcuts import render,redirect
from .functions import read_depth
from .forms import PlantForm,WateringOptionsForm
from .models import Plant,Tank,WateringMethod,HumidityData,TemperatureData,LightState
from .models import SoilMoistureData,PumpState,LightState
from django.http import HttpResponse,JsonResponse
import plotly.graph_objects as go
import plotly.graph_objs as go
import plotly.io as pio


def create_plant(request):
    try:
        instance = Plant.objects.latest("id")
        created = True
    except Plant.DoesNotExist:
        instance = Plant()
        created = False
    
    if request.method == 'POST':
        form = PlantForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            if created:return redirect('/settings')
            else:return redirect('/tankDepth')

    else:
        form = PlantForm(instance=instance)

    return render(request, 'create_plant.html', {'form': form, 'created': created})


def tank_depth(request):
    value = 0
    confirmed=False
    try:
        tank= Tank.objects.latest("id")
        created=True
        confirmed=True
    except Tank.DoesNotExist:
        tank = Tank()
        created = False

    if request.method == 'POST':


        if 'confirm' in request.POST:
            value = read_depth()
            confirmed=True
        elif 'reset' in request.POST:

            value = read_depth()
        elif 'save' in request.POST:
            value = read_depth()
            tank.value = value
            tank.save()
            if created:return redirect('/settings')
            else:return redirect('/wateringMethod')
        else:
            value = None
    else:
        value = read_depth()

    return render(request, 'tank_depth.html', {'value': value,'confirmed':confirmed,'created': created})
def watering_method(request):
    try:
        wateringMethod=WateringMethod.latest()
        created=True
    except:
        wateringMethod=WateringMethod()
        created=False
    if request.method == 'POST':
        form = WateringOptionsForm(request.POST)
        if form.is_valid():
            selected_option = form.cleaned_data['watering_options']
            wateringMethod.method = selected_option
            wateringMethod.save()
            if created:return redirect('/settings')
            else:return redirect('/dashboard')          
    else:
        form = WateringOptionsForm()
    return render(request, 'watering_method.html', {'form': form,'created': created})
def index(request):

    try:
        obj = Plant.objects.latest('id')
        return redirect('dashboard')
    except Plant.DoesNotExist:

        return render(request, 'index.html')
def dashboard(request):
    try:

        obj = Plant.objects.get(id=0)

        return redirect('create')

        return render(request, 'index.html')
    except Plant.DoesNotExist:
        return render(request, 'index.html')



def soilgraph(request):

    data = SoilMoistureData.objects.only('value', 'time').order_by('-time')
    values = [entry.value for entry in data]
    timestamps = [entry.time for entry in data]

    fig = go.Figure(data=go.Scatter(x=timestamps, y=values, mode='lines'))


    fig.update_layout(
        xaxis=dict(title='Time'),
        yaxis=dict(title='Moisture'),

        plot_bgcolor='rgba(255, 255, 255, 0.1)',
        paper_bgcolor='rgba(255, 255, 255, 0.1)',
        showlegend=False,
        margin=dict(l=50, r=50, t=50, b=50),
        title=dict(text='Soil Moisture', font=dict(size=20)),
    )


    config = {'displayModeBar': False}
    soilMoisture = pio.to_html(fig, include_plotlyjs=False, full_html=False,config=config)

    
    return [soilMoisture,values[0]]





def humiditygraph(request):

    data = HumidityData.objects.only('value', 'time').order_by('-time')


    values = [entry.value for entry in data]
    timestamps = [entry.time for entry in data]


    fig = go.Figure(data=go.Scatter(x=timestamps, y=values, mode='lines'))

    fig.update_layout(
        xaxis=dict(title='Time'),
        yaxis=dict(title='Humidity'),
        # title='Humidity',
        plot_bgcolor='rgba(255, 255, 255, 0.1)',
        paper_bgcolor='rgba(255, 255, 255, 0.1)',
        showlegend=False,
        margin=dict(l=50, r=50, t=50, b=50),
        title=dict(text='Humidity', font=dict(size=20)),
    )


    config = {'displayModeBar': False}
    humidity = pio.to_html(fig, include_plotlyjs=False, full_html=False,config=config)


    
    return [humidity,values[0]]


def temperaturegraph(request):
    
    data = TemperatureData.objects.only('value', 'time').order_by('-time')

    
    values = [entry.value for entry in data]
    timestamps = [entry.time for entry in data]

   
    fig = go.Figure(data=go.Scatter(x=timestamps, y=values, mode='lines'))

 
    fig.update_layout(
        
                xaxis=dict(
            title='Time',
            tickangle=30  # Set the tickangle to 0 to display labels horizontally
        ),
        yaxis=dict(title='Temperature'),
        # title='Temperature',
        plot_bgcolor='rgba(255, 255, 255, 0.1)',
        paper_bgcolor='rgba(255, 255, 255, 0.1)',
        showlegend=False,
        margin=dict(l=50, r=50, t=50, b=50),
        title=dict(text='Temperature', font=dict(size=20)),
        
    )

    # Convert the plot to an image and return it as the response
    #img_bytes = fig.to_image(format='png')
    config = {'displayModeBar': False}
    temperature = pio.to_html(fig, include_plotlyjs=False, full_html=False,config=config)

    # Pass the plot_div as context to the template for rendering
    
    return [temperature,values[0]]
    # Return the image as the response
    #return HttpResponse(img_bytes, content_type='image/png')

def waterlevel(request):
    scale_percentages = [0, 20, 40, 60, 80, 100]
    tankDepth = Tank.objects.first().value
    percentage = int(read_depth() / tankDepth * 100)

    if percentage >= 101:
        percentage = 100
    remaining = 100 - percentage
    slices = [percentage, remaining]
    labels = [f'{percentage}% Empty', f'{remaining}% Remaining']
    colors = ['#ff9999', '#66b3ff']

    # Create the pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=slices, hole=0.7, marker=dict(colors=colors))])

    # Set aspect ratio to equal to ensure a circular pie chart
    fig.update_layout(
        title='Tank Level',
        showlegend=True,
        plot_bgcolor='rgba(255, 255, 255, 0.1)',
        paper_bgcolor='rgba(255, 255, 255, 0.1)',
        
        # height=400,
        # width=600
    )

    # Convert the plot to an image and return it as the response
    img_bytes = fig.to_image(format='png')

    # Return the image as the response
    return HttpResponse(img_bytes, content_type='image/png')



def waterlevel2(request):
    
    scale_percentages = [0, 20, 40, 60, 80, 100]
    tankDepth = Tank.objects.first().value
    percentage = int(read_depth() / tankDepth * 100)

    if percentage >= 101:
        percentage = 100
    remaining = 100 - percentage
    slices = [percentage, remaining]
    labels = [f'{percentage}% Empty', f'{remaining}% Remaining']
    colors = ['#ff9999', '#66b3ff']

    # Create the pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=slices, hole=0.7, marker=dict(colors=colors))])

    # Set aspect ratio to equal to ensure a circular pie chart
    fig.update_layout(
        # title='Tank Level',
        showlegend=True,
        plot_bgcolor='rgba(255, 255, 255, 0.1)',
        paper_bgcolor='rgba(255, 255, 255, 0.1)',
        margin=dict(l=50, r=50, t=50, b=50),
        title=dict(text='Tank Level', font=dict(size=20))
        # height=400,
        # width=600
    )

    # Convert the plot to a div string
    config = {'displayModeBar': False}
    plot_div = pio.to_html(fig, include_plotlyjs=False, full_html=False,config=config)

    # Pass the plot_div as context to the template for rendering
    # context = {'waterlevel': plot_div}
    x=True if remaining<=20 else False
    return [plot_div, x]
    #return render(request, 'dashboard.html', context)




def dashboard(request):
    water=waterlevel2(request)
    temperature=temperaturegraph(request)
    humidity=humiditygraph(request)
    soilMoisture=soilgraph(request)
    # pump_state = True if .is_on=='On' else False
    context={
            "soilMoisture":soilMoisture[0],
            "soilMValue":soilMoisture[1],
            'waterlevel':water[0],
            'watervalue':water[1],
             "temperature":temperature[0],
             "tempValue":temperature[1],
             "humidity":humidity[0],
             "humValue":humidity[1],
             "pump_state":PumpState.objects.first(),
             "light_state":LightState.objects.first()
             }
    print(context["pump_state"])
    return render(request, 'dashboard.html',context)
def settings(request):

    return render(request, 'settings.html')

#pump_state, created = PumpState.objects.get_or_create(pk=1)

# Change the values of the state attribute
  # Set the state to True (On)
# pump_state.state = False  # Set the state to False (Off)

# # Save the changes

# pump_state.save()
def switch_lights_view(request):
    if request.method == 'POST':
        light_switch = request.POST.get('light_switch', False)
        #light_state, created = LightState.objects.get_or_create(pk=1)
        light_state = LightState.objects.first()
        
        # Change the value of the state attribute
        light_state.state = light_switch  # Set the state to True (On)
        light_state.save()  # Save the changes


    return redirect('dashboard')


def switch_pump(request):
    if request.method == 'POST':
        pump_state = PumpState.objects.first()
        pump_state.is_on = not pump_state.is_on
        pump_state.save()
        return JsonResponse({'is_on': pump_state.is_on})
def switch_light(request):
    if request.method == 'POST':
        light_state = LightState.objects.first()
        light_state.is_on = not light_state.is_on
        light_state.save()
        return JsonResponse({'is_on': light_state.is_on})