from django.urls import path, include
from django.conf.urls.static import static
from pdf_office import settings
from .views import *


urlpatterns = [
    path('',signIn, name='sign'),
    path('dashboard/',dashboard, name='dashboard'),
    path('tables/',tables, name='tables'),
    path('billings/',billing, name='billings'),
    path('notifications/',notifications, name='notifications'),
    path('profile/',profile, name='profile'),
    path('sign-in/',signIn, name='sign-in'),
    path('sign-up/',signUp, name='sign-up'),

    ## users urls ##
    path('register/', RegisterAPIView.as_view(), name='User-register'),
    path('login/', LoginAPIView.as_view(), name='User-login'),
    path('profile_image_upload/<uuid:user_id>/', ProfileImageView.as_view(), name='User-profile-image'),
    path('forget_password/', ForgetPasswordAPIView.as_view(), name='Forget-password'),
    path('verify_otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('update_email/<uuid:user_id>/', UpdateEmailAPIView.as_view(), name='Update-email'),
    path('update_password/<uuid:user_id>/', UpdatePasswordAPIView.as_view(), name='Update-password'),
    path('change_password/<uuid:user_id>/', ChangePasswordAPIView.as_view(), name='Change-password'),
    path('user/<uuid:user_id>/', GetUserAPIView, name='Get-user'),
    path('users/', GetUsersAPIView, name='Get-users'),

    ## Subscription ##
    path('payment_subscribe/', create_payment, name='payment_subscription'),
    path('payment_subscribe_update/<uuid:id>/', update_payment, name='payment_subscription_update'),
    path('plan/<uuid:plan_id>/', GetPlan, name='Get-plan'),
    path('plans/', GetAllPlans, name='Get-plans'),
    path('payment/<uuid:user_id>/', GetPayment, name='Get-payment'),
    path('payments/', GetAllPayments, name='Get-payments'),


    ## From Pdf ###
    path('pdf_to_word/<uuid:user_id>/', PdfToWord, name='pdf_word'),
    path('pdf_to_excel/<uuid:user_id>/', PdfToExcel, name='pdf_excel'),
    path('pdf_to_jpg/<uuid:user_id>/', PdfToJpg, name='pdf_jpg'),
    path('pdf_to_png/<uuid:user_id>/', PdfToPng, name='pdf_png'),
    path('pdf_to_jpeg/<uuid:user_id>/', PdfToJpeg, name='pdf_jpeg'),
    path('pdf_to_csv/<uuid:user_id>/', PdfToCsv, name='pdf_csv'),
    path('pdf_to_bmp/<uuid:user_id>/', PdfToBmp, name='pdf_jpg'),
    path('pdf_to_ppt/<uuid:user_id>/', PdfToPpt, name='pdf_ppt'),

    ## To Pdf ##
    path('excel_to_pdf/<uuid:user_id>/', ExcelToPdf, name='excel_pdf'),# coming back
    path('csv_to_pdf/<uuid:user_id>/', CsvToPdf, name='csv_pdf'),
    path('image_to_pdf/<uuid:user_id>/', ImageToPdf, name='image_pdf'),
    path('ppt_to_pdf/<uuid:user_id>/', PptToPdf, name='ppt_pdf'),
    path('word_to_pdf/<uuid:user_id>/', WordToPdf, name='word_pdf'),

    ## Edit Pdf  ##
    path('extract_pdf/<uuid:user_id>/', ExtractPdf, name='extract_pdf'),
    path('remove_page/<uuid:user_id>/', RemovePdfPage, name='remove_pdf_page'),
    path('add_page/<uuid:user_id>/', AddPdfPage, name='add_page_to_pdf'),
    # path('reorder_page/<uuid:user_id>/', ReorderPdfPage, name='reorder_pdf_pages'),
    path('repair_pdf/<uuid:user_id>/', RepairPdf, name='repair_pdf'),
    path('rotate_pdf/<uuid:user_id>/', RotatePdf, name='rotate_pdf'),
    path('add_watermark/<uuid:user_id>/', AddWatermark, name='add_watermark_to_pdf'),

    ## Optimize Pdf  ##
    # path('compare_pdf/<uuid:user_id>/', ComparePdf, name='compare_pdf'),
    path('compress_pdf/<uuid:user_id>/', CompressPdf, name='compress_pdf'),
    path('merge_pdf/<uuid:user_id>/', MergePdf, name='merge_pdf'),
    path('split_pdf/<uuid:user_id>/', SplitPdf, name='split_pdf'),

    ## Secure Pdf  ##
    path('protect_pdf/<uuid:user_id>/', ProtectPdf, name='protect_pdf'),
    path('unlock_pdf/<uuid:user_id>/', UnProtectPdf, name='unlock_pdf'),
    path('sign_pdf/<uuid:user_id>/', SignPdf, name='sign_pdf'),
    path('digital_signature/<uuid:user_id>/', Digital_signature, name='digital_signature'),
    path('verify_digital_signature/<uuid:user_id>/', Verify_digital_signature, name='Verify_digital_signature'),
    path('get_digital_digital_signature/',GetALLDigitalSign, name='get_all_digital_signature'),
    # path('check_pdf_sign/<uuid:user_id>/', IsPdfSign, name='check_pdf_sign'),

    ## OCR ## 
    path('ocr_image/<uuid:user_id>/', ocr_image_document, name='ocr_image'),
    path('ocr_identity/<uuid:user_id>/', ocr_identity_document, name='ocr_identity'),

    ## Download ##
    path('file_download/<int:id>/', Downloads, name='download'),
    path('signed_file_download/<int:id>/', DownloadsSignature, name='download'),
    path('getAll/', GetAllFiles, name='getAll'),


    ## API KEY Access ##
    path('create_api_key/<uuid:user_id>/', create_api_key,name='create_api_key'),
    path('get_api_key/<uuid:user_id>/', GetAPIKEY,name='get_api_key'),
    path('get_api_keys/', GetAPIKEYS,name='get_api_keys'),

    ## Contact ##
    path('create_contact/<uuid:user_id>/', ContactCreateView.as_view() ,name='create_contact'),
    path('delete_contact/<uuid:contact_id>/', ContactDeleteView.as_view(),name='delete_contact'),
    path('get_contact/<uuid:contact_id>/', GetContact,name='get_contact'),
    path('get_all_contact/', GetAllContact,name='get_all_contact'),

    path('delete_users/<uuid:id>/', UsersModelDeleteView.as_view(), name='delete_users'),
    path('delete_plans/<uuid:id>/', PlansDeleteView.as_view(), name='delete_plans'),
    path('delete_payments/<uuid:id>/', PaymentsDeleteView.as_view(), name='delete_payments'),
    path('delete_documents/<uuid:id>/', DocumentDeleteView.as_view(), name='delete_documents'),
    path('delete_digital_signatures/<uuid:id>/', DigitalSignatureDeleteView.as_view(), name='delete_digital_signatures'),
    path('delete_api_keys/<uuid:id>/', APIKeyDeleteView.as_view(), name='delete_api_keys'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        # Add other URL patterns here
    ] + urlpatterns