resource "yandex_iam_service_account" "sa-processing-people-faces-photo" {
  name = var.sa_processing_people_faces_photo
}

resource "yandex_iam_service_account_static_access_key" "sa-processing-people-faces-photo-static-key" {
  service_account_id = yandex_iam_service_account.sa-processing-people-faces-photo.id
}

resource "yandex_resourcemanager_folder_iam_member" "sa-processing-people-faces-photo-function-invoker-iam" {
  folder_id = var.folder_id
  role      = "functions.functionInvoker"
  member    = "serviceAccount:${yandex_iam_service_account.sa-processing-people-faces-photo.id}"
}

resource "yandex_resourcemanager_folder_iam_member" "sa-processing-people-faces-photo-storage-uploader-iam" {
  folder_id = var.folder_id
  role      = "storage.uploader"
  member    = "serviceAccount:${yandex_iam_service_account.sa-processing-people-faces-photo.id}"
}

resource "yandex_resourcemanager_folder_iam_member" "sa-processing-people-faces-photo-ymq-admin-iam" {
  folder_id = var.folder_id
  role      = "ymq.admin"
  member    = "serviceAccount:${yandex_iam_service_account.sa-processing-people-faces-photo.id}"
}
