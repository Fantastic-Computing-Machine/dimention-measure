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
    updateDiscount,
    delete_estimator_item_view,
    project_terms_and_conditions_view,
    select_project_terms_and_conditions_view,
    UpdateProjectTermsAndCondition,
    edit_project_terms_and_conditions_list,
    deleteSelectedProjectTnC,
)
from django.conf import settings


urlpatterns = [
    path("", AllEstimates.as_view(), name="all_estimates"),
    path(
        "<int:pk>/<str:project_name>/details/",
        EstimateDetailView.as_view(),
        name="estimate",
    ),
    path(
        "<int:pk>/<str:project_name>/update_estimate/",
        UpdateEstimateProjectView.as_view(),
        name="update_estimate_project",
    ),
    path(
        "<int:pk>/<int:project_id>/<str:project_name>/update_estimate_item/",
        UpdateEstimateItemView.as_view(),
        name="update_estimate_item",
    ),
    path("folio/", FolioView.as_view(), name="folio"),
    path("folio/<int:pk>/update_room/", UpdateRoomView.as_view(), name="update_room"),
    path(
        "folio/<int:pk>/update_room_item/",
        UpdateRoomItemView.as_view(),
        name="update_room_item",
    ),
    path(
        "folio/<int:pk>/update_room_item_desc/",
        UpdateRoomItemDescriptionView.as_view(),
        name="update_room_item_desc",
    ),
    path(
        "estimate/<int:pk>/<str:project_name>/delete",
        DeleteEstimate,
        name="delete_estimate",
    ),
    path("folio/delete/delete_room", DeleteRoom, name="delete_room"),
    path(
        "folio/delete/delete_room_component",
        DeleteRoomComponent,
        name="delete_room_component",
    ),
    path(
        "folio/delete/delete_component_description",
        DeleteComponentDescription,
        name="delete_component_description",
    ),
    path("folio/add_room", AddRoom, name="add_room"),
    path("folio/add_room_component", AddRoomItem, name="add_room_component"),
    path(
        "folio/add_component_description",
        AddRoomItemDescription,
        name="add_component_description",
    ),
    path(
        "excel/<int:project_id>/<str:project_name>/download/",
        download_estimate_excel_file,
        name="download_estimate_excel_file",
    ),
    path(
        "<int:pk>/<str:project_name>/update_discount/",
        updateDiscount,
        name="update_estimate_discount",
    ),
    # estimate_row_id, project_name
    path(
        "<int:pk>/<int:project_id>/<str:project_name>/delete_estimate_component/",
        delete_estimator_item_view,
        name="delete_estimate_row",
    ),
    path(
        "<int:pk>/<str:project_name>/project_terms_and_conditions/",
        project_terms_and_conditions_view,
        name="project_terms_and_conditions",
    ),
    path(
        "<int:pk>/<str:project_name>/select_project_terms_and_conditions/",
        select_project_terms_and_conditions_view,
        name="select_project_terms_and_conditions",
    ),
    path(
        "tnc/<int:pk>/<str:project_name>/update_terms/",
        UpdateProjectTermsAndCondition.as_view(),
        name="update_project_tnc",
    ),
    path(
        "<int:pk>/<str:project_name>/edit_project_terms_and_conditions_list/",
        edit_project_terms_and_conditions_list,
        name="edit_project_terms_and_conditions_list",
    ),
    # url for delete selected prject TNC
    path(
        "<int:pk>/<str:project_name>/delete_selected_project_TnC/",
        deleteSelectedProjectTnC,
        name="delete_selected_project_TnC",
    ),
]
