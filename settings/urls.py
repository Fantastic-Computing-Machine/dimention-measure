from django.urls import path


from settings.views import TermsAndConditions, deleteSelectedTnC
# from settings.views import add_terms_heading, add_terms_content, TermsAndConditions

urlpatterns = [
    # path("add_terms_heading/", add_terms_heading, name="add_terms_heading"),
    # path("add_terms_content/", add_terms_content, name="add_terms_content"),
    path("terms_and_conditions/", TermsAndConditions.as_view(),
         name="terms_and_conditions"),
    # url for delete selected TNC
    path("delete_selected_TnC/", deleteSelectedTnC, name="delete_selected_TnC"),

]
