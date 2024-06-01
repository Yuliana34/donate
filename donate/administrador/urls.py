from django.urls import path
from .views import index,  causas , donado #donar_boton,
#from .blockchain import Blockchain, registrar_nodo

urlpatterns = [
    path('',index, name='admin-index' ),
    path('donado',donado, name='admin-donado'),
     #path('donar',donar, name='admin-donar' ),   
    #path('donar',donar, name='admin-donar' ),
    path('causas',causas, name='admin-causas' ),
]