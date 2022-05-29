from django.urls import path

from estimator.views import (
    AllEstimates,
    UpdateEstimateProjectView,
    EstimateDetailView,
    UpdateEstimateItemView,
    FolioView,
    UpdateRoomView,
    UpdateRoomItemView,
    UpdateRoomItemDescriptionView,
    DeleteEstimate,
    DeleteRoom,
    DeleteRoomComponent,
    DeleteComponentDescription,
    AddRoom,
    AddRoomItem,
    AddRoomItemDescription,
    download_estimate_excel_file,
)


urlpatterns = [
    path("", AllEstimates.as_view(), name="all_estimates"),

    path("<int:pk>/<str:project_name>/details/",
         EstimateDetailView.as_view(), name="estimate"),

    path("<int:pk>/<str:project_name>/update_estimate/",
         UpdateEstimateProjectView.as_view(), name="update_estimate_project"),

    path("<int:pk>/<int:project_id>/<str:project_name>/update_estimate_item/",
         UpdateEstimateItemView.as_view(), name="update_estimate_item"),

    path("folio/", FolioView.as_view(), name="folio"),

    path("folio/<int:pk>/update_room/",
         UpdateRoomView.as_view(), name="update_room"),

    path("folio/<int:pk>/update_room_item/",
         UpdateRoomItemView.as_view(), name="update_room_item"),

    path("folio/<int:pk>/update_room_item_desc/",
         UpdateRoomItemDescriptionView.as_view(), name="update_room_item_desc"),

    path("estimate/<int:pk>/<str:project_name>/delete",
         DeleteEstimate, name="delete_estimate"),

    path("folio/delete/delete_room", DeleteRoom, name="delete_room"),

    path("folio/delete/delete_room_component",
         DeleteRoomComponent, name="delete_room_component"),

    path("folio/delete/delete_component_description",
         DeleteComponentDescription, name="delete_component_description"),

    path("folio/add_room", AddRoom, name="add_room"),

    path("folio/add_room_component", AddRoomItem, name="add_room_component"),

    path("folio/add_component_description",
         AddRoomItemDescription, name="add_component_description"),

    path("excel/<int:project_id>/<str:project_name>/download/",
         download_estimate_excel_file, name="download_estimate_excel_file"),

]
