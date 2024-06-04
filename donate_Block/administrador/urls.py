from django.urls import path
from .views import   causas , donado , donar
#from .blockchain import Blockchain, registrar_nodo
from . import views

urlpatterns = [
    #path('',index, name='admin-index' ),
    path('donado',donado, name='admin-donado'),
    path('causas',views.causas, name='causas' ),

#URLS PARA BLOCKCHAIN
    path('',views.home, name='home' ),
    path('formulario/', views.formulario, name='formulario'),
    path('mine_block/', views.mine_block, name='mine_block'),
    path('get_chain/', views.get_chain, name='get_chain'),
    path('is_valid/', views.is_valid, name='is_valid'),
    path('add_donate_transaction/', views.add_donate_transaction, name='add_donate_transaction'),
    path('connect_node/', views.connect_node, name='connect_node'),
    path('replace_chain/', views.replace_chain, name='replace_chain'),
    path('get_transactions/', views.get_transactions, name='get_transactions'),
    path('empty_transactions/', views.empty_transactions, name='empty_transactions'),
    path('all_transaction/', views.all_transactions, name='all_transactions'),
    path('fetch_record/<str:record_type>/<str:public_key>/', views.fetch_record, name='fetch_record'),

    #path('new_transaction', views.new_transaction, name='new_transaction'),
#URLS PARA BLOCKCHAIN

    path('donar', views.donar, name='donar' ),   
    #path('donar',donar, name='admin-donar' ),
]