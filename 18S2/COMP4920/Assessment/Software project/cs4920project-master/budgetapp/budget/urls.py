from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name = 'register'),
    path('features/', views.features, name = 'features'),
    path('registerconfirm/', views.register, name = 'registerconfirm'),
    path('test/', views.test, name = 'test'),
    path('overview/', views.overview, name = 'overview'),
    path('transactions/', views.transactions, name = 'transactions'),
    path('budget/', views.budget, name = 'budget'),
    path('history/', views.history, name = 'history'),
    path('settings/', views.settings, name = 'settings'),
    path('edittransaction/', views.edit_transaction, name='edit_transaction'),
    path('deletetransaction/', views.delete_transaction, name='delete_transaction'),
    path('recurring/', views.recurring, name='recurring'),
    path('download/', views.download, name='download'),
    path('credits/', views.credits, name='credits'),
    path('receiptupload/', views.receipt_upload, name='receipt_upload'),
    path('confirm=<token>/', views.confirm, name='confirm'),
    path('deletemyaccountpls/', views.delete, name='delete'),
    path('confirm_message/', views.confirm_message, name='confirm_message'),
    path('delete_recurring/', views.delete_recurring, name='delete_recurring'),
]